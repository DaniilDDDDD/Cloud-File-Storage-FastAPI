from fastapi_users.authentication import JWTAuthentication

SECRET = 'GFO_)$+_FB)$+%)JIOG(IGJ+(*$KGFG($*JDFKG$@ITGF_@W$'

auth_backends = []

jwt_authentication = JWTAuthentication(secret=SECRET, lifetime_seconds=(3600 * 12))

auth_backends.append(jwt_authentication)
