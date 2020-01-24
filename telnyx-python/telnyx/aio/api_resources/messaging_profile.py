from telnyx.aio.api_resources.abstract import (
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
    nested_resource_class_methods,
)


@nested_resource_class_methods("phone_number", operations=["list"])
@nested_resource_class_methods("short_code", operations=["list"])
@nested_resource_class_methods("alphanumeric_sender_id", operations=["list"])
class MessagingProfile(
    CreateableAPIResource,
    DeletableAPIResource,
    ListableAPIResource,
    UpdateableAPIResource,
):
    OBJECT_NAME = "messaging_profile"

    async def phone_numbers(self):
        return await MessagingProfile.list_phone_numbers(self.id)

    async def short_codes(self):
        return await MessagingProfile.list_short_codes(self.id)

    async def alphanumeric_sender_ids(self):
        return await MessagingProfile.list_alphanumeric_sender_ids(self.id)
