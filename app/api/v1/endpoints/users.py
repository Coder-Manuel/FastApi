from fastapi import APIRouter, Depends

from app.api.v1.endpoints.models import *
import app.api.v1.functions.auth as auth

router = APIRouter()

users = []


@router.get("/", name="Gets all the users", dependencies=[Depends(auth.JWTAuthorize())], response_model=GetUsersResponse)
def get_users():
    user = User(id="west8r778r", name="Emmanuel Bonke", username="manuel", mobile="0712422524", estate="London",
                home_fellowship="London")
    response = GetUsersResponse(data=[user, user, user, user, user])
    return response


@router.post("/login", name="Login user", response_model=UserLoginResponse)
def login(usr: UserLogin):
    token = auth.generate_JWT(usr.username)
    users.append(usr)
    return UserLoginResponse(access_token=token)


@router.post("/create", name="Create single user", response_model=CreateUserResponse)
def create_user(usr: UserRegister):
    user = User(id="klaxons123456", name=usr.name, username=usr.username, mobile=usr.mobile, estate=usr.estate,
                home_fellowship=usr.home_fellowship)
    response = CreateUserResponse(data=user)
    return response
