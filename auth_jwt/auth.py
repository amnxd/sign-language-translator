from fastapi.params import Query
from fastapi import FastAPI, Depends, APIRouter
from pydantic import BaseModel

from .jwtsign import sign, decode, signup, signin, SignUpSchema, SignInSchema
from .jwtvalidate import Bearer

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


class TokenRequest(BaseModel):
    user_id: str


# @app.post("/secure")
# def secure_route(token: str = Depends(Bearer())):
#     return token

# @app.post("/generate-token")
# def generate_token(request: TokenRequest):
#     token = sign(request.user_id)
#     return token


@router.post("/signup")
def sign_up(request: SignUpSchema):
    token = signup(request.name, request.email, request.password)
    return token


@router.post("/signin")
def sign_in(request: SignInSchema):
    token = signin(request.email, request.password)
    return token


@router.post("/authtest")
def authtest(token: str = Query(...)):
    decoded_token = decode(token)
    return decoded_token