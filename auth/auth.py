import json
import os
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen

from typing import List

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
API_AUDIENCE = os.getenv('AUTH0_AUDIENCE')
ALGORITHMS = ['RS256']

# AuthError Exception
'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Validate the Authorization header value
def get_token_auth_header():
    auth: str = request.headers.get('Authorization', None)

    if not auth:
        raise AuthError({
            'code': 'no_auth_header',
            'description': 'Authorisation Header Required'
        }, 401)

    # The expected Authorisation Header value is "Bearer base64tokenstringvalue"
    # Split and validate the the Authorisation Header
    # Checks to perform are
    # 1. There are two parts the string delimited by a space
    # 2. The first part of the string must start with the word bearer
    auth_parts: List[str] = auth.split()

    # 1. Test part count
    if len(auth_parts) != 2:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'The header provided has an invalid structure'
        }, 401)

    # 2. The Authorisation header must start with "Bearer"
    if auth_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorisation Header must start with "Bearer"'
        }, 401)

    return auth_parts[1]


# helper function to determine is the verified jwt contains the nominated permission
def check_permissions(permission: str, payload: dict):

    permissions: list = payload.get('permissions', None)
    if not permissions:
        raise AuthError({
            'code': 'no_permissions',
            'description': 'There are no permissions granted'
        }, 400)

    if permission not in permissions:
        raise AuthError({
            'code': 'unauthorised',
            'description': 'The required permission has not been granted'
        }, 401)

    return True


# helper function to decode the jwt
def verify_decode_jwt(token: str):
    # get the public key set
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # read the token header
    unverified_header: dict = jwt.get_unverified_header(token)

    # check the key id is in the header
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_token_header',
            'description': 'The Authorisation token has an invalid header'
        }, 401)

    # Get the public key needed to verify the token
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # With the public key set, verify the token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        # Raise an error if the token has expired
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
            }, 401)

        # Raise an error if the token has a claims error
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. ' +
                               'Please, check the audience and issuer.'
            }, 401)

        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)

        finally:
            pass

    else:
        # If the public key cannot be found in the key set, raised an error
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
        }, 400)


# Authentication and authorisation decorator function
def requires_auth(permission: str = ''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)
        return wrapper
    return requires_auth_decorator
