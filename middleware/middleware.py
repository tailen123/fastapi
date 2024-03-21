import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Request, Security
from fastapi.security.api_key import APIKeyHeader

import jwt

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"

api_key_header = APIKeyHeader(name="X-Token", auto_error=True)


async def auth_check(request: Request, token: str = Security(api_key_header)):
    try:
        token: str = request.headers["x-token"]
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")

        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        request.state.user = username

    # TODO: 这三种错误是不是应该分不同的逻辑处理？
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError as e:
        error_message = f"invalid Token : str{e}"
        raise HTTPException(status_code=401, detail=error_message)
    except jwt.PyJWTError as e:
        error_message = f"Token decoding  error: str{e}"
        raise HTTPException(status_code=401, detail=error_message)
    # response = await call_next(request)
    # return response
