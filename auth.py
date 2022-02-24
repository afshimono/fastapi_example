import bcrypt
import jwt
import datetime as dt
import hmac
import hashlib
from typing import Optional, Dict

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Request, HTTPException, status

from settings import env_vars


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if not credentials:
            raise HTTPException(
                status_code=403, detail="Invalid authorization code.")
        if credentials.scheme != "Bearer":
            raise HTTPException(
                status_code=403, detail="Invalid authentication scheme.")
        payload = self.verify_jwt(credentials.credentials)
        if not payload:
            raise HTTPException(
                status_code=403, detail="Invalid token or expired token.")
        return payload

    def verify_jwt(self, jwtoken: str) -> Optional[Dict]:
        try:
            payload = jwt_token_handler.decode_access_token(jwtoken)
        except:
            payload = None
        return payload


class JWTTokenHandler:
    def __init__(self, secret: str) -> None:
        self.algorithm = "HS256"
        self.secret = secret

    def create_access_token(self, *, data: dict, expires_delta: dt.timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = dt.datetime.utcnow() + expires_delta
        else:
            expire = dt.datetime.utcnow() + dt.timedelta(minutes=120)
        to_encode["exp"] = expire
        return jwt.encode(to_encode, self.secret, algorithm=self.algorithm)

    def decode_access_token(self, token):
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, self.secret,
                                 algorithms=[self.algorithm])
        except jwt.PyJWTError as e:
            raise credentials_exception from e
        return payload


jwt_token_handler = JWTTokenHandler(env_vars.jwt_secret)


def hash_pwd(pwd: str, salt: str, pepper: str) -> str:
    peppered = hmac.new(pepper.encode('utf-8'),
                        pwd.encode('utf-8'), hashlib.sha256).hexdigest()
    salted = bcrypt.hashpw(peppered.encode('utf-8'), salt.encode('utf-8'))
    return salted.decode('utf-8')


def check_logged_own_or_is_admin(logged_user: Dict, user_id: int) -> None:
    if logged_user["user_id"] != user_id and not logged_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")


def check_logged_is_admin(logged_user: Dict) -> None:
    if not logged_user["is_admin"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized.")


async def get_logged_credentials(request: Request) -> Dict:
    bearer = JWTBearer()
    return await bearer(request)
