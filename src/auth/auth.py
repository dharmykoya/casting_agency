import json
from flask import request, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

AUTH0_DOMAIN = 'damikoya.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'castingagency'

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


'''
Helper function that verifies authorization
header and returns token without the bearer string
'''


def get_token_auth_header():
    auth_token = request.headers.get('Authorization', None)
    if not auth_token:
        raise AuthError({
            'message': 'No Authorization header provided.'
        }, 401)
    segmented_token = auth_token.split()
    if segmented_token[0].lower() != 'bearer':
        raise AuthError({
            'message': 'Malformed token".'
        }, 401)
    elif len(segmented_token) == 1:
        raise AuthError({
            'message': 'Malformed token".'
        }, 401)
    elif len(segmented_token) > 2:
        raise AuthError({
            'message': 'Malformed token".'
        }, 401)
    token = segmented_token[1]
    return token


'''
Helper function that checks if there's a permissions
list in the decoded token payload and verifies that
the user can perform said action
'''


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)

    if permission not in payload['permissions']:
        abort(401)
    return True


'''
Helper function that verifies that the token is actually
a valid token and decodes it
'''


def verify_decode_jwt(token):
    jsonurl = urlopen(f'https://damikoya.auth0.com/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://damikoya.auth0.com/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)


'''
the authorization decorator that uses the previous helper functions
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator