from telnyx.aio.api_requestor import APIRequestor
from telnyx.aio.util import convert_to_telnyx_object
from telnyx.telnyx_object import TelnyxObject as BaseTelnyxObject


class TelnyxObject(BaseTelnyxObject):
    async def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params
        requestor = APIRequestor(key=self.api_key, api_base=self.api_base())
        response, api_key = await requestor.request(method, url, params, headers)

        return convert_to_telnyx_object(response, api_key)
