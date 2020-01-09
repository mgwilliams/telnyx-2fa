import asyncio
from collections import defaultdict

import telnyx
from aiohttp import web
from telnyx.aio import Call

from telnyx_2fa import settings


class HangupException(Exception):
    pass


class Leg:
    def __init__(self, call=None):
        self._waiting = defaultdict(list)
        if call:
            self.call = call
        else:
            self.call = None

    @classmethod
    def construct_from(cls, *args, **kwargs):
        call = Call.construct_from(*args, **kwargs)
        return cls(call)

    def __getattr__(self, attr):
        return getattr(self.call, attr)

    def wait_for_event(self, event_type):
        f = asyncio.Future()
        self._waiting[event_type].append(f)
        return f

    async def wait_gather_using_speak(self, *args, **kwargs):
        await self.gather_using_speak(*args, **kwargs)
        try:
            e = await self.wait_for_event('call.gather.ended')
        except HangupException:
            return None, None
        return e.get('digits'), e.get('status')

    async def wait_speak(self, *args, **kwargs):
        await self.speak(*args, **kwargs)
        e = await self.wait_for_event('call.speak.ended')


class CallControlSession:
    def __init__(self, api_key=None):
        self.api_key = api_key or telnyx.api_key
        self.__legs = {}

    def create_update_leg(self, event):
        """
        Add or update a leg for this Call.
        """

        leg = self.__legs.get(event.call_leg_id)
        if leg is None:
            leg = Leg.construct_from(event, self.api_key)
            self.__legs[leg.call_leg_id] = leg
        else:
            leg.call.refresh_from(event)
        return leg

    def handle_event(self, event_type, event):
        """
        Process an incoming webhook event. First, check for waiting futures
        invoking the appropriate callbacks if no futures are waiting and
        a callback exists.
        """

        leg = self.create_update_leg(event)

        waiting = leg._waiting.get(event_type)
        if waiting:
            while True:
                try:
                    f = waiting.pop()
                    f.set_result(event)
                except IndexError:
                    break
        else:
            f = getattr(self, f"on_{event_type.replace('.', '_')}",
                        getattr(self, 'on_unknown', None))
            if f:
                asyncio.ensure_future(f(event, leg))
            else:
                raise Exception(f'no callback: {event}')

    async def on_call_hangup(self, event, leg):
        for _, futures in self._waiting:
            for f in futures:
                f.set_exception(HangupException())


class TwoFactorAuthCC(CallControlSession):
    state = None

    def __init__(self, token, uuid, language=None,
                 *args, **kwargs):
        super(TwoFactorAuthCC, self).__init__(*args, **kwargs)
        self.token = token
        self.language = language or settings.DEFAULT_LANGUAGE
        self.uuid = uuid
        self.result = asyncio.Future()

    async def on_call_initiated(self, event, leg):
        if leg.direction == 'incoming':
            return web.json_response(
                {'error': 'incoming calls not supported'}, status=400)
        self.state = 'CALL_INITIATED'
        return web.json_response(status=202)

    async def on_call_answered(self, event, leg):
        self.state = 'CALL_ANSWERED'
        v = f'VOICE_PROMPT_{self.language.upper().replace("-","_")}'
        text = settings.get(v, settings.DEFAULT_VOICE_PROMPT)

        user_input, status = await \
            leg.wait_gather_using_speak(payload=text,
                                        language=self.language,
                                        voice=settings.VOICE,
                                        minimum_digits=len(self.token),
                                        maximum_digits=len(self.token),
                                        maximum_tries=settings.VOICE_REPEAT_PROMPT,
                                        timeout_millis=settings.VOICE_TIMEOUT*1000)

        success = status == 'valid' and user_input == self.token

        if success:
            text = settings.get(f'VOICE_SUCCESS_{self.language.upper().replace("-","_")}',
                                settings.DEFAULT_VOICE_SUCCESS)
        else:
            text = settings.get(f'VOICE_FAILURE_{self.language.upper().replace("-","_")}',
                                settings.DEFAULT_VOICE_FAILURE)
        await leg.wait_speak(payload=text, language=self.language,
                             voice=settings.VOICE)
        asyncio.ensure_future(leg.hangup())
        self.result.set_result(success)

    async def on_unknown(self, event, leg):
        # ignore unknown events
        pass
