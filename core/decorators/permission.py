from core.utils.index import decodeJWT, decodePermissionToken, response


def permission(permission, role=None):
    def decorator(fun):
        def wrapper(*args, **kwargs):
            try:
                authorized = False
                token = decodeJWT(args[1])
                is_admin = token['roles'].count('admin')
                superAdmin = token['is_superuser']
                permissions = decodePermissionToken(token['permissions'])['permissions']

                if role and token['roles'].count(role) == 0 and is_admin == 0 and superAdmin == 0:
                    return response({'error': 'You don\'t have the role to do this'}, status=401)

                for p in permission:
                    if p in permissions:
                        authorized = True
                        break

                if (authorized == False and is_admin == 0 and superAdmin == 0):
                    return response({'error': 'You don\'t have the permission to do this'}, status=401)

                return fun(*args, **kwargs)
            except Exception as e:
                return response({'error': 'authentication token not provided'}, status=401)
        return wrapper
    return decorator
