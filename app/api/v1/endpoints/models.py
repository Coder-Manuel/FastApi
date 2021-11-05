from pydantic import BaseModel
from typing import List, Any


class User(BaseModel):
    id: str
    name: str
    username: str
    mobile: str
    estate: str
    home_fellowship: str


class UserRegister(BaseModel):
    name: str
    username: str
    password: str
    mobile: str
    estate: str
    home_fellowship: str


class UserLogin(BaseModel):
    username: str
    password: str


class Response(BaseModel):
    status: int = 200
    message: str = "Success"


class UserLoginResponse(Response):
    access_token: str


class ErrorResponse(Response):
    message = "Failed"
    status = 500
    detail: str


class ForbiddenResponse(Response):
    message = "Forbidden"
    status = 403
    detail: str


class UnauthorizedResponse(Response):
    message = "Unauthorized"
    status = 401
    detail: str


class BadRequestResponse(Response):
    message = "Bad Request"
    status = 400
    detail: str


class CreateUserResponse(Response):
    message = "Success"
    status = 201
    data: User


class GetUsersResponse(Response):
    status = 200
    message = "Success"
    data: List[User]
