from telnyx.aio import api_requestor, util
from telnyx.api_resources.abstract.meta import ResourceMeta as BaseResourceMeta


class ResourceMeta(BaseResourceMeta):
    @staticmethod
    def action_method(cls, action):
        async def f(self, api_key=None, **params):
            url = cls._build_url(self, action)
            requestor = api_requestor.APIRequestor(api_key)
            response, api_key = await requestor.request(action.http_method, url, params)
            return util.convert_to_telnyx_object(response, api_key)

        return f
