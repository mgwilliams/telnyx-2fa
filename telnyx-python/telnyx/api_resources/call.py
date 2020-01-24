from telnyx.api_resources.abstract import CreateableAPIResource
from telnyx.api_resources.abstract.meta import Action, ResourceMeta
from telnyx.six import with_metaclass


class BaseCall:
    OBJECT_NAME = "call"

    reject = Action("reject")
    answer = Action("answer")
    hangup = Action("hangup")
    bridge = Action("bridge")
    speak = Action("speak")
    fork_start = Action("fork_start")
    fork_stop = Action("fork_stop")
    gather_using_audio = Action("gather_using_audio")
    gather_using_speak = Action("gather_using_speak")
    playback_start = Action("playback_start")
    playback_stop = Action("playback_stop")
    record_start = Action("record_start")
    record_stop = Action("record_stop")
    send_dtmf = Action("send_dtmf")
    transfer = Action("transfer")


class Call(with_metaclass(ResourceMeta, CreateableAPIResource, BaseCall)):
    pass
