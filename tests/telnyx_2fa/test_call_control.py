import asyncio

import pytest
from asynctest import MagicMock, CoroutineMock, patch
from telnyx.aio import Event

from telnyx_2fa.call_control import Leg, CallControlSession, TwoFactorAuthCC


def get_session():
    return TwoFactorAuthCC('00', 'abc')
class MockCall(MagicMock):
    """A mock Call object"""
    @classmethod
    def construct_from(cls, *args, **kwargs):
        return cls()

def test_leg_contruct_from():
    with patch('telnyx_2fa.call_control.Call', MockCall):
        leg = Leg.construct_from(None)
        assert isinstance(leg, Leg)


def test_leg_wait_for_event():
    with patch('telnyx_2fa.call_control.Call', MockCall):
        leg = Leg.construct_from(None)
        f = leg.wait_for_event('test')
        assert isinstance(f, asyncio.Future)
        assert len(leg._waiting['test']) == 1
    

@pytest.mark.asyncio
async def test_leg_gather():
     with patch('telnyx_2fa.call_control.Call', MockCall):
        leg = Leg.construct_from(None)
     f = asyncio.Future()
     f.set_result(None)
     leg.gather_using_speak.return_value = f
     f2 = leg.wait_gather_using_speak()
     t = asyncio.ensure_future(f2)
     await asyncio.sleep(0.1)
     leg._waiting['call.gather.ended'][0].set_result({'digits': '1', 'status': 'success'})
     await asyncio.sleep(0.1)
     digits, status = t.result()
     assert digits == '1'
     assert status == 'success'


def test_create_update_leg():
    session = CallControlSession()
    event = Event.construct_from({'call_leg_id': 'A'}, None)
    leg = session.create_update_leg(event)
    assert leg.call_leg_id == 'A'
    event = Event.construct_from({'call_leg_id': 'A',
                                  'bar': 2}, None)
    leg = session.create_update_leg(event)
    assert leg.call_leg_id == 'A'
    assert leg.bar == 2


@pytest.mark.asyncio
async def test_handle_incoming_call():
    leg = Leg.construct_from({'call_leg_id': 'A',
                              'direction': 'incoming'}, None)
    sess = get_session()
    r = await sess.on_call_initiated(event=None, leg=leg)
    assert r.status == 400


@pytest.mark.asyncio
async def test_call_initiated():
    leg = Leg.construct_from({'call_leg_id': 'A',
                              'direction': 'outgoing'}, None)
    sess = get_session()
    r = await sess.on_call_initiated(event=None, leg=leg)
    assert r.status == 202
    assert sess.state == 'CALL_INITIATED'


@pytest.mark.parametrize('token,customer_input,status,expected',
                         [('11', '112', 'valid', False),
                          ('11', '11', 'valid', True),
                          ('11', '', 'invalid', False),
                          ('11', '1', 'invalid', False),
                          ('11', '12', 'valid', False)])
@pytest.mark.asyncio
async def test_call_answered(token, customer_input, status, expected):
    leg = Leg.construct_from({'call_leg_id': 'A',
                              'direction': 'outgoing'}, None)
    f = asyncio.Future()
    f.set_result((customer_input, status))
    leg.wait_gather_using_speak = CoroutineMock(return_value=f)
    sess = TwoFactorAuthCC(token, 'ABC')
    await sess.on_call_answered(None, leg)
    result = await sess.result
    assert result == expected
