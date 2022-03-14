#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import os
from flask import request, _request_ctx_stack, abort
from functools import wraps
from jose import jwt
from urllib.request import urlopen

#----------------------------------------------------------------------------#
# Settings
#----------------------------------------------------------------------------#

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')

#----------------------------------------------------------------------------#
# AuthError Exception
#----------------------------------------------------------------------------#

'''
A standardized way to communicate auth failure modes
'''
class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

#----------------------------------------------------------------------------#
# Auth Header
#----------------------------------------------------------------------------#

'''
get_token_auth_header() method:

- gets the header from the request
- raises an AuthError if no header is present
- attempts to split bearer and the token
- raises an AuthError if the header is malformed
- returns the token part of the header
'''

def get_token_auth_header():
    """
    Obtains the Access Token from the Authorization Header
    """
    auth = request.headers.get('Authorization', None)
    if not auth:
        raise AuthError({
            'code': 'authorization_header_missing',
            'description': 'Authorization header is expected.'
        }, 401)
    
    # Splits the auth string into a list using space as separator
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    
    # check that number of items in parts list is equal to 1
    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)
    
    # check that number of items in parts list is greater than 2
    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)
    
    token = parts[1]
    return token

#----------------------------------------------------------------------------#
# Check Permissions
#----------------------------------------------------------------------------#

'''
check_permissions(permission, payload) method:

- permission: string permission (i.e. 'post:movies')
- payload: decoded jwt payload
- raises an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
- raises an AuthError if the requested permission string is not in the payload permissions array
- returns true otherwise
'''

def check_permissions(permission, payload):
    # print("I am payload: ", payload)
    # print("I am permission: ", permission)
    # print("I am payload['permissions']", payload['permissions'])
    
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT.'
        }, 400)
    
    if permission not in payload['permissions']:
        abort(403)
        # raise AuthError({
        #     'code': 'unauthorized',
        #     'description': 'Permission not found.'
        #     }, 403)
    return True

#----------------------------------------------------------------------------#
# Verify JWT
#----------------------------------------------------------------------------#

'''
verify_decode_jwt(token) method:

- token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload
'''
def verify_decode_jwt(token):
    """
    jwks is a public set of json web keys and acts as the public key 
    in this case. The private key is held and used to generate and sign
    the jwt by Auth0
    """
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
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
                issuer='https://' + AUTH0_DOMAIN + '/'
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
                'description': 'Incorrect claims. Please, check the audience and issuer.'
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


#----------------------------------------------------------------------------#
# Verify JWT
#----------------------------------------------------------------------------#

'''
@requires_auth(permission) decorator method:

- permission: string permission (i.e. 'post:movie')

    it should use the get_token_auth_header method to get the token
    it should use the verify_decode_jwt method to decode the jwt
    it should use the check_permissions method validate claims and check the requested permission
    return the decorator which passes the decoded payload to the decorated method
'''
def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except:
                abort(401)
            
            check_permissions(permission, payload)
            
            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator