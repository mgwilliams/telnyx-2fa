from telnyx.aio.api_resources.abstract.createable_api_resource import (
    CreateableAPIResource,
)
from telnyx.aio.api_resources.abstract.meta import ResourceMeta
from telnyx.api_resources.call import BaseCall


class Call(CreateableAPIResource, BaseCall, metaclass=ResourceMeta):
    pass
