import asyncio
import json

import pytest
from asynctest import patch, Mock, MagicMock, CoroutineMock

import telnyx_2fa.app
from telnyx_2fa.app import Telnyx2FApp, RequestHandler


class MockSettings:
    SMS_TOKEN_DIGITS = 4
    BASE_URL = 'foo/'
    VOICE_TOKEN_DIGITS = 2
    DEFAULT_LANGUAGE = 'en-US'
    DEFAULT_SMS_MESSAGE = 'test'
    SMS_ANI = '18005551212'
    
    @staticmethod
    def get(attr, default):
        return default


class MockCall(MagicMock):
    call_session_id = 'ABC'
    call_leg_id = 'ABC'
    #create = CoroutineMock(return_value=MockCall())
    
    @classmethod
    async def create(cls, *args, **kwargs):
        return cls()

@pytest.mark.asyncio
async def test_voice_2fa():
    with patch('telnyx_2fa.app.Call', MockCall):
        mock_cc = Mock
        mock_cc.result = asyncio.Future()
        mock_cc.result.set_result(True)
        with patch('telnyx_2fa.app.TwoFactorAuthCC', mock_cc):
            app = Telnyx2FApp()
            r = await app.voice_2fa('15055551212', '11')
    assert r
        

@pytest.mark.parametrize('ltype,expected',
                         [('mobile', True),
                          ('foo', False)])
@pytest.mark.asyncio
async def test_is_mobile(ltype, expected):
    client = Mock()
    #f = asyncio.Future()
    #f.set_result((f'{{"carrier": {{"type": "{ltype}"}}}}', 200, None))
    #client.request.return_value = f
    client.request = CoroutineMock(return_value=(
        f'{{"carrier": {{"type": "{ltype}"}}}}', 200, None))
    handler = RequestHandler(client=client)
    assert (await handler.is_mobile('15055551212')) == expected

@pytest.mark.asyncio
@patch('telnyx_2fa.app.settings', MockSettings)
async def test_handle_2fa():
    handler = RequestHandler()
    handler.is_mobile = CoroutineMock(return_value=True)
    request = Mock()
    request.query = {'to': '+15055551212'}
    r = await handler.handle_2fa(request)
    response = json.loads(r.text)
    sms = response['sms']
    assert len(sms['token']) == MockSettings.SMS_TOKEN_DIGITS
    assert sms['url'] == f'foo/2fa/sms?to=%2B15055551212&token={sms["token"]}&language=en-US'

    voice = response['voice']
    assert len(voice['token']) == MockSettings.VOICE_TOKEN_DIGITS
    assert voice['url'] == f'foo/2fa/voice?to=%2B15055551212&token={voice["token"]}&language=en-US'

@pytest.mark.asyncio
@patch('telnyx_2fa.app.settings', MockSettings)
async def test_handle_voice():
    handler = RequestHandler()
    request = Mock()
    mock_telnyx = Mock()
    mock_telnyx.voice_2fa = CoroutineMock(return_value=True)
    request.app = {'telnyx': mock_telnyx}
    request.query = {'to': '+15055551212', 'token': '22'}

    mock_web = Mock()
    mock_response = Mock()
    mock_response.prepare = CoroutineMock()
    mock_response.write = CoroutineMock()
    mock_response.write_eof = CoroutineMock()
    mock_web.StreamResponse.return_value = mock_response
    with patch('telnyx_2fa.app.web', mock_web):
        r = await handler.handle_voice(request)
    writes = mock_response.write.call_args_list
    assert json.loads(writes[0][0][0])['status'] == 'waiting'
    assert json.loads(writes[1][0][0])['status'] == 'success'


@pytest.mark.asyncio
@patch('telnyx_2fa.app.settings', MockSettings)
async def test_handle_sms():
    handler = RequestHandler()
    request = Mock()
    request.query = {'to': '+15055551212', 'token': '2222'}
    mock_message = Mock()
    mock_message.create = CoroutineMock()
    with patch('telnyx_2fa.app.Message', mock_message):
        r = await handler.handle_sms(request)
    response = json.loads(r.text)
    assert response['status'] == 'ok'
