import jwt
from config import Settings
from datetime import timezone, datetime, timedelta
from .schemas import Token, BaseUser
from passlib.context import CryptContext
import random


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_CONFIG = Settings().auth_jwt


def sign_JWT(user: BaseUser):
    now = datetime.now(
            tz=timezone.utc
    )
    exp = now + timedelta(weeks=2)
    payload = {
        'sub': user.username,
        'user_id': str(user.user_id),
        'created_at': now.timestamp(),
        'exp': exp.timestamp()
        }
    token = jwt.encode(
        payload=payload,
        algorithm=JWT_CONFIG.algorithm,
        key=JWT_CONFIG.secret
    )
    return Token(token=token)


def decode_JWT(token: Token) -> BaseUser:
    decode_token = jwt.decode(
        token.token,
        JWT_CONFIG.secret,
        algorithms=[JWT_CONFIG.algorithm]
    )
    return BaseUser(
        username=decode_token['sub'],
     user_id=decode_token['user_id']
     )\
     if decode_token['exp'] > datetime.now().timestamp() else None


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)