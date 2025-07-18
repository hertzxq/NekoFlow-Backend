import uvicorn
from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext
from authx import AuthX, AuthXConfig, RequestToken
from services.anime_router import anime_router
from database.models import init_db, UsersModel, engine
from database.shema import UsersShema, LoginShema
from core.config import SECRET_KEY
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(anime_router)

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


# Настройка аутентификации и хэширования
config = AuthXConfig(
    JWT_ALGORITHM="HS256",
    JWT_SECRET_KEY=SECRET_KEY,
    JWT_TOKEN_LOCATION=["headers"],
)

auth = AuthX(config=config)
auth.handle_errors(app)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_session():
    async with AsyncSession(engine) as session:
        yield session


@app.post("/users")
async def create_user(user: UsersShema, session: AsyncSession = Depends(get_session)):
    try:
        if len(user.username) <= 5:
            raise HTTPException(
                status_code=400,
                detail="Username must be longer than 6 characters"
            )

        elif len(user.password) <= 5:
            raise HTTPException(
                status_code=400,
                detail="Password must be longer than 6 characters"
            )

        existing_user = await session.execute(
            text("SELECT 1 FROM users WHERE username = :username OR email = :email"),
            {"username": user.username, "email": user.email}
        )
        if existing_user.scalar() is not None:
            raise HTTPException(
                status_code=400,
                detail="Username or email already exists"
            )

        hashed_password = pwd_context.hash(user.password)

        users_data = UsersModel(username=user.username, email=user.email, password=hashed_password)
        session.add(users_data)
        await session.commit()
        await session.refresh(users_data)

        return {"success": True, "id": users_data.id, "username": users_data.username}

    except HTTPException as e:
        raise e
    except Exception as e:
        await session.rollback()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.post("/login")
async def login(user_data: LoginShema, session: AsyncSession = Depends(get_session)):
    try:
        result = await session.execute(select(UsersModel).where(UsersModel.username == user_data.username))
        user = result.scalars().first()

        if not user:
            logger.warning("User not found")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Неверный username или пароль"}
            )

        if not user.password or len(user.password) < 60 or not user.password.startswith("$2b$"):
            logger.error(f"Invalid password hash for user {user.username}: {user.password}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail={"message": "Internal server error: invalid password hash"}
            )

        is_valid = pwd_context.verify(user_data.password, user.password)

        if not is_valid:
            logger.warning("Password verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"message": "Неверный username или пароль"}
            )

        token = auth.create_access_token(uid=user.username)
        return {"access_token": token, "token_type": "bearer"}

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={"message": "Internal server error"}
        )


@app.get("/protected", dependencies=[Depends(auth.get_token_from_request)])
def get_protected(token: RequestToken = Depends()):
    try:
        auth.verify_token(token=token)
        return {"message": "Hello world !"}
    except Exception as e:
        raise HTTPException(status_code=401, detail={"message": str(e)})


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)