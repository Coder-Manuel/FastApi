import time

import jwt
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from app.config import AppConfig as config
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.api.v1.endpoints.models import *

JWT_KEY = config.SECRET_KEY
ALGORITHM = config.ALGORITHM


def generate_JWT(user: str) -> str:
    payload = {
        "user": user,
        "exp": time.time() + 600
    }
    token = jwt.encode(payload, key=JWT_KEY, algorithm=ALGORITHM)
    return token


def decode_JWT(token: str) -> dict:
    # noinspection PyBroadException
    try:
        decoded_token = jwt.decode(token, key=JWT_KEY, algorithms=[ALGORITHM])
        if decoded_token["exp"] >= time.time():
            return decoded_token
        else:
            return {}
    except:
        return {}


def verify_JWT(token: str) -> bool:
    # noinspection PyBroadException
    try:
        payload = decode_JWT(token)
        return True if payload else False
    except:
        return False


class JWTAuthorize(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTAuthorize, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        # try:
        credentials: HTTPAuthorizationCredentials = await super(JWTAuthorize, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                return ForbiddenResponse(detail="Invalid authentication scheme")
            if not verify_JWT(credentials.credentials):
                raise HTTPException(detail="Invalid code", status_code=403)
        else:
            return JSONResponse(content=ForbiddenResponse(detail="Authorization code missing").dict(), status_code=403)
    # except HTTPException as e:
    #     if e.detail == "Not authenticated":
    #         print("No Code")
    #         return JSONResponse(content=ForbiddenResponse(detail="Authorization code missing").dict(),
    #                             status_code=403)
