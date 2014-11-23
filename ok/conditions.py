from conditionhandler import condition_handler

@condition_handler.register("admin", "Allows to do anything")
def admin_allows(scheme, netloc, path, query_params, query, hostname,
        port, permission_params):
    return True

@condition_handler.register(
    "path_allowed",
    "Returns true if the path is allowed, false otherwise")
def basic_access_allows(scheme, netloc, path, query_params, query,
        hostname, port, permission_params):
    return True
