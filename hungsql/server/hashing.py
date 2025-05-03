from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hash():
    @staticmethod
    def bcrypt(password: str) -> str:
        try:
            return pwd_context.hash(password)
        except Exception as e:
            raise ValueError("Error hashing the password") from e

    @staticmethod
    def verify(hashed_password: str, plain_password: str) -> bool:
        try:
            return pwd_context.verify(plain_password, hashed_password)
        except Exception as e:
            return False
    