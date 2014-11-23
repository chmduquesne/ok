class ConditionHandler():
    def __init__(self):
        self.func_map = {}

    def register(self, name, description):
        def func_wrapper(func):
            self.func_map[name] = {"function": func, "description":
                    description}
            return func
        return func_wrapper

    def get(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("Condition " + str(name) + " is unknown.")
        return func

    def all_conditions(self):
        return dict(((key, self.func_map[key]["description"]) for key in
            self.func_map))

condition_handler = ConditionHandler()
