from telnyx.aio.api_resources.abstract import (
    CreateableAPIResource,
    ListableAPIResource,
    nested_resource_class_methods,
)


@nested_resource_class_methods("extend", path="actions/extend", operations=["create"])
class NumberReservation(CreateableAPIResource, ListableAPIResource):
    OBJECT_NAME = "number_reservation"

    async def extend(self, **params):
        return await NumberReservation.create_extend(self.id, **params)
