from telnyx import util
from telnyx.aio.api_resources.abstract import (
    CreateableAPIResource,
    nested_resource_class_methods,
)


@nested_resource_class_methods(
    "alphanumeric_sender_id", path="alphanumeric_sender_id", operations=["create"]
)
class Message(CreateableAPIResource):
    OBJECT_NAME = "message"

    @classmethod
    async def send_from_alphanumeric_sender_id(cls, **params):
        params = util.rewrite_reserved_words(params)
        return await Message.create_alphanumeric_sender_id(None, **params)
