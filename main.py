import uvicorn
from fastapi import FastAPI
from services.anime_router import anime_router
from core.router import router
from fastapi.middleware.cors import CORSMiddleware
from database.models import init_db
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app):
    await init_db()

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(anime_router)
app.include_router(router)


origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "if you see this, it's working ;)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
