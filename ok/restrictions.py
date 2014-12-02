import re
import json

class Rule():
    def __init__(self, func):
        self.func = func

    def applies(self, *args, **kwargs):
        return self.func(*args, **kwargs)


class RestrictionsManager():
    def __init__(self):
        self.func_map = {}

    def register(self, takes_extra_param=False):
        def func_wrapper(func):
            func_name = func.__name__
            f = self.func_map.get(func_name)
            if f is not None and f["function"] != func:
                raise KeyError(
                    "%s: restriction already registered" % func_name
                    )
            self.func_map[func_name] = {
                "function": func,
                "takes_extra_param": takes_extra_param
                }
            return func
        return func_wrapper

    def get(self, name):
        func = self.func_map[name]["function"]
        return Rule(func)

    def forget(self, name):
        try:
            del self.func_map[name]
        except KeyError:
            pass

    def all(self):
        return dict([(key, self.func_map[key]["function"].__doc__) for key
                     in self.func_map])


restrictions_manager = RestrictionsManager()


# Now we register restrictions
@restrictions_manager.register()
def unrestricted(groupname, http_scheme, http_netloc, http_path,
                 http_query, http_fragment, http_username, http_password,
                 http_hostname, http_port, http_method, http_data,
                 restriction_params):
    """
    Unconditional access
    """
    return True


@restrictions_manager.register(takes_extra_param=True)
def http_methods(groupname, http_scheme, http_netloc, http_path,
                 http_query, http_fragment, http_username, http_password,
                 http_hostname, http_port, http_method, http_data,
                 restriction_params):
    """
    Restricts the http methods.

    Expected parameter: a list (ex: ["GET", "POST"])
    """
    allowed_methods = restriction_params

    return http_method in allowed_methods


@restrictions_manager.register(takes_extra_param=True)
def host_match(groupname, http_scheme, http_netloc, http_path,
                 http_query, http_fragment, http_username, http_password,
                 http_hostname, http_port, http_method, http_data,
                 restriction_params):
    """
    Restricts the host name.

    Expected parameter: a string, interpreted as a regex (ex: "example.com")
    """
    host_pattern = restriction_params

    return re.match(host_pattern, http_hostname)


@restrictions_manager.register(takes_extra_param=True)
def ports(groupname, http_scheme, http_netloc, http_path,
                 http_query, http_fragment, http_username, http_password,
                 http_hostname, http_port, http_method, http_data,
                 restriction_params):
    """
    Restricts the port.

    Expected parameter: a list of integers (ex: [80, 443])
    """
    allowed_ports = restriction_params

    if http_port is None:
        http_port = 80

    if http_port is None and http_scheme == "https":
        http_port = 443

    return http_port in allowed_ports


@restrictions_manager.register(takes_extra_param=True)
def schemes(groupname, http_scheme, http_netloc, http_path,
                 http_query, http_fragment, http_username, http_password,
                 http_hostname, http_port, http_method, http_data,
                 restriction_params):
    """
    Restricts the scheme.

    Expected parameter: a list of schemes (ex: [])
    """
    allowed_schemes = restriction_params

    if http_scheme is None:
        http_scheme = "http"

    return http_scheme in allowed_schemes
