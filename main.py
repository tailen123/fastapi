from fastapi import FastAPI
from router.router_order import router as router_order
from router.router_login import router as router_log
from router.router_message import router as router_message
from router.router_result import router as router_result
import uvicorn

app = FastAPI()

# 添加订单相关路由分组
app.include_router(router_order, prefix="/orders", tags=["orders"])
app.include_router(router_log, prefix="/login", tags=["login"])
app.include_router(router_message, prefix="/message", tags=["message"])
app.include_router(router_result, prefix="/results", tags=["results"])

# 添加用户相关路由分组


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8000)
