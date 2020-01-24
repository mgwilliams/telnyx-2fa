from telnyx.aio import api_requestor, util
from telnyx.aio.api_resources.abstract.api_resource import APIResource


class ListableAPIResource(APIResource):
    @classmethod
    async def auto_paging_iter(cls, *args, **params):
        return await cls.list(*args, **params).auto_paging_iter()

    @classmethod
    async def auto_paging_iter_by_token(cls, *args, **params):
        return await cls.list(*args, **params).auto_paging_iter_by_token()

    @classmethod
    async def list(cls, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key, api_base=cls.api_base())
        url = cls.class_url()
        response, api_key = await requestor.request("get", url, params)
        response.data["url"] = url

        telnyx_object = util.convert_to_telnyx_object(response, api_key)
        telnyx_object._retrieve_params = params
        return telnyx_object
