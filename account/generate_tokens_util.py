import jwt
import os

def create_access_token(user, tutor=False):
    """
    Create an access token.
    :param user: The user object.
    :param tutor: A boolean indicating if the user is a tutor.
    :return: The access token.
    """
    user_role = 'tutor' if tutor else 'user'
    payload = {'user': user, 'role': user_role}
    access_token_secret = os.environ.get('SECRET_KEY')
    access_token_expiration = int(os.environ.get('ACCESS_TOKEN_LIFETIME'))
    return jwt.encode(payload, access_token_secret, algorithm='HS256', expiresIn=access_token_expiration)

def create_access_token_admin(admin):
    """
    Create an access token for admin.
    :param admin: The admin object.
    :return: The access token.
    """
    payload = {'role': 'admin'}
    access_token_secret = os.environ.get('SECRET_KEY')
    access_token_expiration = int(os.environ.get('ACCESS_TOKEN_LIFETIME'))
    return jwt.encode(payload, access_token_secret, algorithm='HS256', expiresIn=access_token_expiration)

def create_refresh_token(user):
    """
    Create a refresh token.
    :param user: The user object.
    :return: The refresh token.
    """
    payload = {'user': user}
    refresh_token_secret = os.environ.get('SECRET_KEY')
    refresh_token_expiration = int(os.environ.get('REFRESH_TOKEN_LIFETIME'))
    return jwt.encode(payload, refresh_token_secret, algorithm='HS256', expiresIn=refresh_token_expiration)
