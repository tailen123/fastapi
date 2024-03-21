from functools import wraps

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL 数据库连接信息
MYSQL_USERNAME = "root"
MYSQL_PASSWORD = "12345678"
MYSQL_HOST = "localhost"
MYSQL_DB = "order_database"

SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{MYSQL_USERNAME}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def atomicity(commit=False):
    def wrapper(func):
        @wraps(func)
        async def decorator(*args, **kwargs):
            db = kwargs.get("db")
            if not db:
                kwargs["db"] = get_db()
            else:
                r = await func(*args, **kwargs)
            return r

        return decorator

    return wrapper
