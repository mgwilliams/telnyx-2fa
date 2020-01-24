from urllib.parse import quote_plus

from telnyx import util
from telnyx.aio import api_requestor, util as aioutil
from telnyx.aio.api_resources.abstract.api_resource import APIResource


class UpdateableAPIResource(APIResource):
    @classmethod
    async def _modify(cls, url, api_key=None, **params):
        requestor = api_requestor.APIRequestor(api_key)
        params = util.rewrite_reserved_words(params)
        response, api_key = requestor.request("patch", url, params)
        return aioutil.convert_to_telnyx_object(response, api_key)

    @classmethod
    async def modify(cls, sid, **params):
        url = "%s/%s" % (cls.class_url(), quote_plus(util.utf8(sid)))
        return await cls._modify(url, **params)

    async def save(self):
        updated_params = self.serialize(None)

        if updated_params:
            self.refresh_from(
                await self.request(
                    UpdateableAPIResource.save_method(self),
                    self.instance_url(),
                    updated_params,
                )
            )
        else:
            util.logger.debug("Trying to save already saved object %r", self)
        return self

    @classmethod
    def save_method(cls, instance):
        if instance.id is None:
            return "post"
        else:
            return "patch"
