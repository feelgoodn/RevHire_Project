from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from .token import ALGORITHM, SECRET_KEY
from .database import  get_db
from fastapi import Depends,HTTPException, status
from typing import Annotated
from .schemas import TokenData, UserRoleEnum
from .models import User


oauth2_schema = OAuth2PasswordBearer(tokenUrl="login")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_current_user(
    token: Annotated[str, Depends(oauth2_schema)],
    db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        role: UserRoleEnum = UserRoleEnum(payload.get("role"))

        if username is None:
            raise credentials_exception

        token_data = TokenData(username=username, role=role)
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == token_data.username).first()

    if user is None:
        raise credentials_exception

    return User(
        id=user.id,
        username=user.username,
        email=user.email,
        role=user.role,
        phone_number=user.phone_number
    )

