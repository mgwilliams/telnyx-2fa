from telnyx import util
from telnyx.aio import api_requestor
from telnyx.aio.api_resources.abstract.api_resource import APIResource
from telnyx.aio.util import convert_to_telnyx_object


class CreateableAPIResource(APIResource):
    @classmethod
    async def create(cls, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        url = cls.class_url()
        params = util.rewrite_reserved_words(params)
        response, api_key = await requestor.request("post", url, params)

        return convert_to_telnyx_object(response, api_key)
