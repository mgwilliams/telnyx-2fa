import asyncio
import json
import re
from logging import getLogger
from random import randrange
from uuid import uuid4

import telnyx
from aiohttp import web
from telnyx.aio import Call, Message
from telnyx.aio.util import convert_to_telnyx_object

from telnyx_2fa import settings
from telnyx_2fa.call_control import TwoFactorAuthCC


telnyx.api_key = settings.TELNYX_API_KEY
telnyx.default_http_client = telnyx.aio.http_client.TelnyxClient()

e164_re = re.compile('^\\+?[1-9]\\d{1,14}$')
phone_data_url = 'https://api.telnyx.com/v1/phone_number/{tn}'

log = getLogger()


async def _write_json(response, data):
    data = (json.dumps(data) + '\n').encode()
    await response.write(data)


class Telnyx2FApp:
    def __init__(self):
        self.sessions = {}

    def handle_cc_event(self, session_id, event_type, event):
        session = self.sessions.get(session_id)
        if session is None:
            log.error(f'Unknown session: {session_id}')
            raise web.HTTPBadRequest()
        return session.handle_event(event_type, event)

    async def voice_2fa(self, to, token, uuid=None, language=settings.DEFAULT_LANGUAGE):
        call = await Call.create(from_=settings.VOICE_ANI, to=f'{to}',
                                 connection_id=settings.TELNYX_CONNECTION_ID)
        uuid = uuid or str(uuid4())
        sess = self.sessions[call.call_session_id] = \
            TwoFactorAuthCC(token=token,
                            language=language,
                            uuid=uuid)
        sess.create_update_leg(call)
        result = await sess.result
        del self.sessions[call.call_session_id]
        return result


class WebhookHandler:
    def __init__(self, session_class=TwoFactorAuthCC):
        self.session_class = session_class
        self.sessions = {}

    async def handle_event(self, request):
        data = await request.json()
        event_type = data['event_type']
        payload = data['payload']
        event = convert_to_telnyx_object(payload)
        sess_id = payload['call_session_id']
        request.app['telnyx'].handle_cc_event(sess_id, event_type, event)
        return web.json_response({'status': 'ok'})


def request_handler(f):
    """
    decorator for request handlers
    """

    def request_wrapper(self, request):
        api_key = request.headers.get('X-API-Key')
        if api_key != settings.API_KEY:
            raise web.HTTPUnauthorized()
        if 'to' not in request.query or not e164_re.match(request.query['to']):
            raise web.HTTPBadRequest('To parameter must be in e164 format.')
        return f(self, request)
    return request_wrapper


class RequestHandler:
    def __init__(self, client=None):
        self.client = client or telnyx.default_http_client

    async def is_mobile(self, tn):
        data, status, _ = await \
            self.client.request('GET', phone_data_url.format(tn=tn),
                                headers={'Accept': 'application/json'})
        if status != 200:
            raise web.HTTPServerError()
        data = json.loads(data)
        if data['carrier'].get('type') == 'mobile':
            return True
        return False

    @request_handler
    async def handle_2fa(self, request):
        to = request.query['to'].replace('+', '%2B')
        language = request.query.get('language', settings.DEFAULT_LANGUAGE)
        ret = {}
        if await self.is_mobile(to):
            token = ''.join(str(randrange(0, 9)) for i in
                            range(settings.SMS_TOKEN_DIGITS))
            ret['sms'] = {'url': settings.BASE_URL +
                          f'2fa/sms?to={to}&token={token}&language={language}',
                          'token': token}

        token = ''.join(str(randrange(0, 9)) for i in
                        range(settings.VOICE_TOKEN_DIGITS))
        ret['voice'] = {'url': settings.BASE_URL +
                        f'2fa/voice?to={to}&token={token}&language={language}',
                        'token': token}
        return web.json_response(ret)

    @request_handler
    async def handle_voice(self, request):
        to = request.query['to']
        language = request.query.get('language', settings.DEFAULT_LANGUAGE)
        token = request.query.get('token')
        if not token:
            raise web.HTTPBadRequest('Missing token parameter.')

        uuid = str(uuid4())
        response = web.StreamResponse()
        await response.prepare(request)
        await _write_json(response, {'status': 'waiting', 'uuid': uuid})
        

        fut = request.app['telnyx'].voice_2fa(to, token, language=language,
                                              uuid=uuid)
        to_wait = [fut]
        success = False

        while True:
            done, to_wait = await asyncio.wait(to_wait, timeout=15)
            if done:
                success = done.pop().result()
                break
            await _write_json(response, {'status': 'waiting', 'uuid': uuid})

        r = {'status': 'failure', 'uuid': uuid}
        if success:
            r['status'] = 'success'

        await _write_json(response, r)
        await response.write_eof()
        return response

    @request_handler
    async def handle_sms(self, request):
        to = request.query['to']
        language = request.query.get('language', settings.DEFAULT_LANGUAGE)
        token = request.query.get('token')
        if not token:
            raise web.HTTPBadRequest('Missing token parameter.')

        v = f'SMS_MESSAGE_{language.upper().replace("-","_")}'
        text = settings.get(v, settings.DEFAULT_SMS_MESSAGE) + ' ' + token
        await Message.create(from_=settings.SMS_ANI, to=to,
                             text=text)
        return web.json_response({'status': 'ok'})


def main():
    app = web.Application()
    app['telnyx'] = Telnyx2FApp()
    webhooks = app['webhook-handler'] = WebhookHandler()
    requests = app['request-handler'] = RequestHandler()

    app.router.add_route('POST', '/event',
                         webhooks.handle_event, name='event')
    app.router.add_route('GET', '/2fa',
                         requests.handle_2fa, name='_2fa')
    app.router.add_route('GET', '/2fa/voice',
                         requests.handle_voice, name='voice')
    app.router.add_route('GET', '/2fa/sms',
                         requests.handle_sms, name='sms')
    web.run_app(app, host='0.0.0.0', port=settings.PORT)


if __name__ == '__main__':
    main()
