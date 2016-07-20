
def ensure_scope(scopes, check_methods=None):
    if check_methods is None:
        check_methods = ["list", "create"] + ["retrieve", "update", "destroy"]

    def check(request, endpointset):
        if endpointset.requested_method in check_methods:
            if not set(scopes).issubset(set(request.token.scope)):
                return (False, 403, "insufficient_scope")
    return check
