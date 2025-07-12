import uvicorn
from fastapi import FastAPI
from services.anime_router import anime_router
app = FastAPI()
app.include_router(anime_router)

@app.get("/")
async def root():
    return {"message": "if you see this, it's working ;)"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
