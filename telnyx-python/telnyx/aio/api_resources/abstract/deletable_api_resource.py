from telnyx.aio.api_resources.abstract.api_resource import APIResource


class DeletableAPIResource(APIResource):
    async def delete(self, **params):
        await self.refresh_from(self.request("delete", self.instance_url(), params))
        return self
