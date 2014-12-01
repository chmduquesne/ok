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
            self.func_map[func.__name__] = {
                    "function": func,
                    "takes_extra_param": takes_extra_param
                    }
            return func
        return func_wrapper

    def get(self, name):
        func = self.func_map[name]["function"]
        return Rule(func)

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
