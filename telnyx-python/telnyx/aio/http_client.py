import textwrap
from asyncio import sleep

from aiohttp import (
    ClientConnectionError,
    ClientError,
    ClientSSLError,
    ServerConnectionError,
    ServerTimeoutError,
)
from aiohttp.client import ClientSession

from telnyx import error, util
from telnyx.http_client import HTTPClient


class TelnyxClient(HTTPClient):
    name = "aiohttp"

    def __init__(self, timeout=80, session=None, verify_ssl_certs=True, **kwargs):
        # since this is a private attribute of HTTPClient we set it here in case
        # the underlying implementation chages
        self._verify_ssl_certs = verify_ssl_certs

        super(TelnyxClient, self).__init__(verify_ssl_certs=verify_ssl_certs, **kwargs)
        self._timeout = timeout
        self._session = session or ClientSession

    async def request_with_retries(self, method, url, headers, post_data=None):
        num_retries = 0

        while True:
            try:
                num_retries += 1
                response = await self.request(method, url, headers, post_data)
                connection_error = None
            except error.APIConnectionError as e:
                connection_error = e
                response = None

            if self._should_retry(response, connection_error, num_retries):
                if connection_error:
                    util.log_info(
                        "Encountered a retryable error %s"
                        % connection_error.user_message
                    )

                sleep_time = self._sleep_time_seconds(num_retries)
                util.log_info(
                    (
                        "Initiating retry %i for request %s %s after "
                        "sleeping %.2f seconds."
                        % (num_retries, method, url, sleep_time)
                    )
                )
                await sleep(sleep_time)
            else:
                if response is not None:
                    return response
                else:
                    raise connection_error

    async def request(self, method, url, headers, post_data=None):
        kwargs = {}
        kwargs["verify_ssl"] = self._verify_ssl_certs
        if self._proxy:
            kwargs["proxies"] = self._proxy

        try:
            async with self._session() as session:
                result = await session.request(
                    method,
                    url,
                    headers=headers,
                    data=post_data,
                    timeout=self._timeout,
                    **kwargs,
                )
            content = await result.text()
            status_code = result.status
        except Exception as e:
            self._handle_request_error(e)
        return content, status_code, result.headers

    def _handle_request_error(self, e):
        # Catch SSL error first as it is a subclass of ClientConnectionError,
        # but we don't want to retry
        if isinstance(e, ClientSSLError):
            msg = (
                "Could not verify Telnyx's SSL certificate.  Please make "
                "sure that your network is not intercepting certificates.  "
                "If this problem persists, let us know at "
                "support@telnyx.com."
            )
            err = f"{type(e).__name__}, {str(e)}"
            should_retry = False
        # Retry only timeout and connect errors; similar to urllib3 Retry
        elif isinstance(
            e, (ServerTimeoutError, ServerConnectionError, ClientConnectionError)
        ):
            msg = (
                "Unexpected error communicating with Telnyx.  "
                "If this problem persists, let us know at "
                "support@telnyx.com."
            )
            err = f"{type(e).__name__}, {str(e)}"
            should_retry = True
        # Catch remaining aiohttp exceptions
        elif isinstance(e, ClientError):
            msg = (
                "Unexpected error communicating with Telnyx.  "
                "If this problem persists, let us know at "
                "support@telnyx.com."
            )
            err = f"{type(e).__name__}, {str(e)}"
            should_retry = False
        else:
            msg = (
                "Unexpected error communicating with Telnyx. "
                "It looks like there's probably a configuration "
                "issue locally.  If this problem persists, let us "
                "know at support@telnyx.com."
            )
            err = f"A(n) {type(e).__name__} was raised"
            if str(e):
                err += f" with error message {str(e)}"
            else:
                err += " with no error message"
            should_retry = False

        msg = textwrap.fill(msg) + f"\n\n(Network error: {err})"
        raise error.APIConnectionError(msg, should_retry=should_retry)

    def close(self):
        self._session.close()
