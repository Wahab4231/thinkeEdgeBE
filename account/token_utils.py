import jwt

def verify_token(token, token_secret):
    try:
        decoded = jwt.decode(token, token_secret, algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        # Token expired
        return None
    except jwt.InvalidTokenError:
        # Invalid token
        return None
