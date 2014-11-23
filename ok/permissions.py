from permissionhandler import permission_handler

@permission_handler.register("admin", "Allows to do anything")
def admin_allows(scheme, netloc, path, query_params, query, hostname,
        port, permission_params):
    return True

@permission_handler.register("basic_access", "")
def basic_access_allows(scheme, netloc, path, query_params, query,
        hostname, port, permission_params):
    return True
