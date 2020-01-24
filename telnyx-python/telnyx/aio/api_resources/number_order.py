from telnyx.aio.api_resources.abstract import (
    CreateableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
)


class NumberOrder(CreateableAPIResource, ListableAPIResource, UpdateableAPIResource):
    OBJECT_NAME = "number_order"
