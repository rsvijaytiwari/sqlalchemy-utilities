from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from models.connection import create_db, get_db
from models.users import User, UserAddress
from utilities.serilizers import ModelSerializer


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    await create_db()
    yield


app = FastAPI(lifespan=lifespan)


class UserAddressSerializer(ModelSerializer):
    fields = ["id", "address_line1", "address_line2"]


class UserSerializer(ModelSerializer):
    fields = ["id", "address"]

    async def get_address(self, item):
        return (await UserAddressSerializer(
            connection=self.connection,
            data=(await self.connection.execute(select(UserAddress).filter(
                UserAddress.user_id == item.id
            ))).scalars().all()
        ).serialize()).data


@app.get("/users")
async def get_user(db: AsyncSession = Depends(get_db)):
    result = (await db.execute(select(User))).scalars().all()
    return (await UserSerializer(connection=db, data=result).serialize()).data
