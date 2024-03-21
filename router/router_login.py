from fastapi import APIRouter, Depends
from fastapi import FastAPI, Depends, HTTPException, status, Request


import jwt
from passlib.context import CryptContext
from passlib.hash import bcrypt
from datetime import datetime, timedelta

router = APIRouter()

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"


# 验证密码
def verify_password(plain_password, hashed_password):
    return bcrypt.verify(plain_password, hashed_password)


# 获取密码哈希
def get_password_hash(password):
    return bcrypt.hash(password)


# 示例用户模型
fake_users_db = {
    "1": {
        "username": "1",
        "email": "johndoe@example.com",
        "hashed_password": get_password_hash("1"),
    }
}


# JWT令牌创建函数
def create_access_token(data: dict):
    to_encode = data.copy()
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


# JWT令牌解码函数获取用户名进行中间件验证
def decode_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return username
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/token")
async def login(username: str, password: str):
    user = fake_users_db.get(username)
    if not user or not verify_password(password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # expire = datetime.utcnow() + timedelta(minutes=30)
    # expire_str = expire.strftime("%Y-%m-%d %H:%M:%S")
    # token_data = {"sub": username, "exp": expire_str}
    token_data = {"sub": username}
    token = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

