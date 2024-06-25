from django.http import HttpResponse

def attach_token_to_cookie(cookie_name, token, response):
    """
    Attach a token to a cookie in the response.
    :param cookie_name: The name of the cookie.
    :param token: The token value to attach to the cookie.
    :param response: The HTTP response object.
    """
    # Determine if the environment is production
    is_production = True if os.environ.get('NODE_ENV') == 'production' else False
    
    # Create the cookie
    response.set_cookie(
        key=cookie_name,
        value=token,
        httponly=True,
        secure=is_production,  # Set secure flag only in production
        max_age=24 * 60 * 60,  # Max age of the cookie in seconds (24 hours)
        samesite='Strict'  # Optional, adds SameSite attribute to the cookie
    )

    print('Cookie set - https only? - ', is_production)
