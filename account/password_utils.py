import bcrypt

async def compare_passwords(plain_text_password, hashed_password):
    """
    Compare a plain text password with its hashed version.
    :param plain_text_password: The plain text password to compare.
    :param hashed_password: The hashed password to compare against.
    :return: True if the passwords match, False otherwise.
    """
    return bcrypt.checkpw(plain_text_password.encode('utf-8'), hashed_password.encode('utf-8'))

async def create_hashed_password(plain_text_password):
    """
    Create a hashed password from a plain text password.
    :param plain_text_password: The plain text password to hash.
    :return: The hashed password.
    """
    hashed_password = bcrypt.hashpw(plain_text_password.encode('utf-8'), bcrypt.gensalt())
    return hashed_password.decode('utf-8')
