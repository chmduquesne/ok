class PermissionHandler():
    def __init__(self):
        self.func_map = {}

    def register(self, name, description):
        def func_wrapper(func):
            self.func_map[name] = {"function": func, "description":
                    description}
            return func
        return func_wrapper

    def permission_checker(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("Permission " + str(name) + " is unknown.")
        return func

    def all_permissions(self):
        return dict(((key, self.func_map[key]["description"]) for key in
            self.func_map))

permission_handler = PermissionHandler()
