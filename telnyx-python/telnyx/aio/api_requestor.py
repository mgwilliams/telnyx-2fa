import telnyx.aio
from telnyx import util
from telnyx.aio.http_client import TelnyxClient
from telnyx.api_requestor import APIRequestor as BaseAPIRequestor


class APIRequestor(BaseAPIRequestor):
    def __init__(self, key=None, client=None, api_base=None):
        from telnyx import verify_ssl_certs as verify
        from telnyx import proxy

        client = (
            client
            or telnyx.aio.default_http_client
            or TelnyxClient(verify_ssl_certs=verify, proxy=proxy)
        )
        super(APIRequestor, self).__init__(key=key, client=client, api_base=api_base)

    async def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders, my_api_key = await self.request_raw(
            method.lower(), url, params, headers
        )
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp, my_api_key

    async def request_raw(self, method, url, params=None, supplied_headers=None):
        """
        Mechanism for issuing an API call
        """
        abs_url, headers, post_data, my_api_key = self.prepare_raw_request(
            method, url, params=params, supplied_headers=supplied_headers
        )

        rbody, rcode, rheaders = await self._client.request_with_retries(
            method, abs_url, headers, post_data
        )

        util.log_info("Telnyx API response", path=abs_url, response_code=rcode)
        util.log_debug("API response body", body=rbody)

        return rbody, rcode, rheaders, my_api_key
