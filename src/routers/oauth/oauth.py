from fastapi.exceptions import HTTPException
from typing_extensions import Annotated
from .jwt_func import decodeToken, createToken
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from fastapi import Depends, status, APIRouter
from query import login
from models import Token, UserLogin, UserName

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(
    tags=["Oauth"]
)

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credencials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Not valid credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = decodeToken(token)
    if not payload:
        raise credencials_exception
    return UserName(**payload)


@router.get("/validate")
async def validate(
    current_user: Annotated[UserName, Depends(get_current_user)],
):
    return current_user

@router.post("/token")
async def auth(data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    user = await login(UserLogin(username=data.username,password=data.password))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = createToken(dict(user))
    return Token(access_token=token, token_type="bearer")
