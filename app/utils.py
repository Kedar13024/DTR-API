from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["argon2"] , deprecated = "auto")

def hashed_pass(password :str):
    return  pwd_context.hash(password)

def verify_pass(password : str , hashedPassword : str):
    return pwd_context.verify(password , hashedPassword)