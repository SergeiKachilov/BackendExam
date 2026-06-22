from fastapi import FastAPI
import routers
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(routers.user_router)
app.include_router(routers.product_router)
app.include_router(routers.order_router)
app.include_router(routers.comment_router)