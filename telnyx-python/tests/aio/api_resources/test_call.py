from __future__ import absolute_import, division, print_function

import pytest

import telnyx.aio

CALL_CONTROL_ID = "AgDIxmoRX6QMuaIj_uXRXnPAXP0QlNfXczRrZvZakpWxBlpw48KyZQ=="


async def create_dial():
    return await telnyx.aio.Call.create(
        connection_id="1111111111222222223", to="+12223334444", from_="+12223330000"
    )


class TestCall(object):
    @pytest.mark.asyncio
    async def test_is_creatable(self, event_loop, request_mock):
        resource = await create_dial()
        request_mock.assert_requested("post", "/v2/calls")
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_reject(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.reject()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/reject" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_answer(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.answer()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/answer" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_hangup(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.hangup()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/hangup" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_bridge(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.bridge(call_control_id=CALL_CONTROL_ID)
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/bridge" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_fork_start(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.fork_start()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/fork_start" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_fork_stop(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.fork_stop()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/fork_stop" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_gather_using_audio(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.gather_using_audio(audio_url="http://telnyx-audio.url")
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/gather_using_audio" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_gather_using_speak(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.gather_using_speak(
            language="en-US", voice="female", payload="Hello from the other side"
        )
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/gather_using_speak" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_playback_start(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.playback_start(audio_url="http://telnyx-audio.url")
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/playback_start" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_playback_stop(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.playback_stop()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/playback_stop" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_record_start(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.record_start(channels="single", format="mp3")
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/record_start" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_record_stop(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.record_stop()
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/record_stop" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_send_dtmf(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.send_dtmf(digits="1www2WABCDw9")
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/send_dtmf" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_speak(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.speak(
            language="en-US", voice="female", payload="Hello from the other side"
        )
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/speak" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)

    @pytest.mark.asyncio
    async def test_can_call_transfer(self, request_mock):
        resource = await create_dial()
        resource.call_control_id = CALL_CONTROL_ID
        await resource.transfer(to="+11111222222")
        request_mock.assert_requested(
            "post", "/v2/calls/%s/actions/transfer" % CALL_CONTROL_ID
        )
        assert isinstance(resource, telnyx.aio.Call)
