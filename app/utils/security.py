from passlib.context import CryptContext

hash_password = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return hash_password.verify(plain_password, hashed_password)