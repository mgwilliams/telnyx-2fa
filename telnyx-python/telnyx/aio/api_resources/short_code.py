from telnyx.aio.api_resources.abstract import ListableAPIResource, UpdateableAPIResource


class ShortCode(ListableAPIResource, UpdateableAPIResource):
    OBJECT_NAME = "short_code"
