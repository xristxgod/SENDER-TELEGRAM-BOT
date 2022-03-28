import fastapi
from src.swagger import router

app = fastapi.FastAPI(
    title=f"BotUserCheck",
    description="Service for getting information about users",
    version="1.0.0",
)

app.include_router(router)
