from telnyx import api_requestor, util
from telnyx.six.moves.urllib.parse import quote_plus


class Action:
    base_path = "actions/"
    http_method = "post"

    def __init__(self, action):
        self.action = action

    @property
    def path(self):
        return self.base_path + self.action


class ResourceMeta(type):
    def __new__(cls, name, bases, cls_dict):
        for base in bases:
            for k, v in base.__dict__.items():
                if isinstance(v, Action):
                    cls_dict[k] = cls.action_method(cls, v)
        return type.__new__(cls, name, bases, cls_dict)

    @staticmethod
    def _build_url(obj, action):
        parts = [obj.class_url()]
        if getattr(obj, "call_control_id", None) is not None:
            parts.append(
                quote_plus(obj.call_control_id, safe=util.telnyx_valid_id_parts)
            )
        parts.append(quote_plus(action.path, safe="/"))
        return "/".join(parts)

    @staticmethod
    def action_method(cls, action):
        def f(self, api_key=None, **params):
            url = cls._build_url(self, action)
            requestor = api_requestor.APIRequestor(api_key)
            response, api_key = requestor.request(action.http_method, url, params)
            return util.convert_to_telnyx_object(response, api_key)

        return f
