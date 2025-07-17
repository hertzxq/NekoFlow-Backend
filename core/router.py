from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import UsersModel, engine
from database.shema import UsersShema


router = APIRouter(
    tags=["Router"],
)

async def get_session():
    async with AsyncSession as session:
        yield session


@router.post("/users")
async def create_user(user: UsersShema, session: AsyncSession = Depends(get_session)):
    try:
        users_data = UsersModel(username=user.username, password=user.password)
        session.add(users_data)
        await session.commit()
        return {"success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))