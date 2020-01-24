from telnyx.aio.telnyx_object import TelnyxObject
from telnyx.api_resources.abstract import APIResource as BaseAPIResource


class APIResource(TelnyxObject, BaseAPIResource):
    @classmethod
    async def retrieve(cls, id, api_key=None, **params):
        instance = cls(id, api_key, **params)
        await instance.refresh()
        return instance

    async def refresh(self):
        await self.refresh_from(self.request("get", self.instance_url()))
        return self
