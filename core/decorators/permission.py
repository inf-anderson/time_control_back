from core.utils.index import decodeJWT, decodePermissionToken, response


def permission(permission, role=None):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            try:
                token = decodeJWT(args[1])
                is_admin = token['roles'].count('admin')
                permissions = decodePermissionToken(
                    token['permissions'])['permissions']

                if role and token['roles'].count(role) == 0 and is_admin == 0:
                    return response({'error': 'You don\'t have the role to do this'}, status=401)

                if (permissions.count(permission) == 0):
                    return response({'error': 'You don\'t have the permission to do this'}, status=401)

                return fun(*args, **kwargs)
            except Exception as e:
                return response({'error': 'authentication token not provided'}, status=401)
        return wrapper
    return decorator
