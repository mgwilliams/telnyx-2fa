from telnyx.aio.api_resources.abstract import (
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
)


class APIKey(CreateableAPIResource, ListableAPIResource, DeletableAPIResource):
    OBJECT_NAME = "api_key"
