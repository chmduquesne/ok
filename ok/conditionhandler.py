class ConditionEngine():
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

    def validates(self, name=None):
        func = self.func_map.get(name, None)
        if func is None:
            raise Exception("Condition " + str(name) + " is unknown.")
        return func

    def all_conditions(self):
        return dict([(key, self.func_map[key]["function"].__doc__) for key
            in self.func_map])

condition_engine = ConditionEngine()
