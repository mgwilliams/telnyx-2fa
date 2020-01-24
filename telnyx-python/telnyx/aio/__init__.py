import sys

from telnyx.aio.api_resources import *  # noqa

if sys.version_info < (3, 6):
    raise Exception("Python >= 3.6 required for telnyx.async")


default_http_client = None
