from telnyx.aio.api_resources.abstract import ListableAPIResource, UpdateableAPIResource


class MessagingPhoneNumber(ListableAPIResource, UpdateableAPIResource):
    OBJECT_NAME = "messaging_phone_number"
