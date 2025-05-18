import os
import re

from dotenv import load_dotenv
from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from .auth_db import get_db, User
from .auth_model import CreateUser, Token

router = APIRouter(prefix="/auth")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

load_dotenv()

@router.post("/user", status_code=status.HTTP_201_CREATED)
async def createUser(user: CreateUser, db: Session = Depends(get_db)):
  validateUsername(user.username, db)
  validatePassword(user.password, db)

  # hash password
  hashedPassword = bcrypt_context.hash(user.password)

  # create user
  newUser = User(username=user.username, hashed_password=hashedPassword)
  db.add(newUser)
  db.commit()
  db.refresh(newUser)

  return status.HTTP_201_CREATED

def validateUsername(username: str, db: Session):
  if len(username) < 5:
    raise HTTPException(status_code=400, detail="Username must be at least 5 characters long")

  if not re.match(r'^[a-zA-Z0-9_]+$', username):
    raise HTTPException(status_code=400, detail="Username can only contain letters, numbers, and underscores")

  # check username is unique
  existingUser = db.query(User).filter(User.username == username).first()
  if existingUser:
    raise HTTPException(status_code=400, detail="Username already exists")

  return True

def validatePassword(password: str, db: Session):
   # Validate password strength
  if len(password) < 8:
    raise HTTPException(status_code=400, detail="Password must be at least 8 characters long")

  if not re.search(r'[A-Z]', password):
    raise HTTPException(status_code=400, detail="Password must contain at least one uppercase letter")

  if not re.search(r'[a-z]', password):
    raise HTTPException(status_code=400, detail="Password must contain at least one lowercase letter")

  if not re.search(r'[0-9]', password):
    raise HTTPException(status_code=400, detail="Password must contain at least one number")

  if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
    raise HTTPException(status_code=400, detail="Password must contain at least one special character")

  return True

def authenticateUser(username: str, password: str, db: Session = Depends(get_db)):
  user = db.query(User).filter(User.username == username).first()
  if not user:
    return False
  if not bcrypt_context.verify(password, user.hashed_password):
    return False
  return True

def createAccessToken(username: str):
  expire = datetime.now(timezone.utc) + timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
  encode = {"sub": username, "exp": expire}
  return jwt.encode(encode, str(os.getenv("AUTH_KEY")), algorithm=os.getenv("ALGORITHM"))

@router.post("/token", response_model=Token)
def loginForAccessToken(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
  user = authenticateUser(form_data.username, form_data.password, db)
  if not user:
    raise HTTPException(status_code=401, detail="Invalid username or password")

  token = createAccessToken(form_data.username)

  return {"access_token": token, "token_type": "Bearer"}


def getCurrentUser(token: Annotated[str, Depends(oauth2_bearer)]):
  try:
    payload = jwt.decode(token, str(os.getenv("AUTH_KEY")), algorithms=[os.getenv("ALGORITHM")])
    username: str = payload.get("sub")
    if not username: # Null or empty
      raise HTTPException(status_code=401, detail="Could not validate credentials")
    return { "username": username }
  except JWTError:
    raise HTTPException(status_code=401, detail="Could not validate credentials")
