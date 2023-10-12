from fastapi import APIRouter

marks = APIRouter()


@marks.get("/")
async def index():
    return {"msg": "Hello World"}