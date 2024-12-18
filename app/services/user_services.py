from typing import List

from fastapi import HTTPException
from security import get_password_hash
from schemas.user_schema import User as userSchema, UserCreate, UserUpdate
from config.prsma_config import prisma
from prisma.errors import UniqueViolationError


class UserService:

    # get all users
    async def get_users(self) -> List[userSchema]:
        users = await prisma.user.find_many()
        return [userSchema(**user.model_dump()) for user in users]

    # get a single user by id
    async def get_user(self, id: int) -> userSchema:
        user = await prisma.user.find_unique(where={"id": id})
        if not user:
            return None
        return userSchema(**user.model_dump())

    # get a single user by email
    async def get_user_by_email(self, email: str) -> userSchema:
        user = await prisma.user.find_unique(where={"email": email})
        if not user:
            return None
        return userSchema(**user.model_dump())

    #  create a new user


    async def create_user(self, user: UserCreate) -> userSchema:
        try:
            user = await prisma.user.create(data=user.model_dump())
            # hash the password
            user.password = get_password_hash(user.password)
            await prisma.user.update(
                where={"id": user.id}, data={"password": user.password}
            )
            return userSchema(**user.model_dump())
        except UniqueViolationError as e:
            if e.code == "P2002":  # Unique constraint failed
                raise HTTPException(status_code=400, detail="Email already taken")
            raise

    # update a user
    async def update_user(self, id: int, user: UserUpdate) -> userSchema:
        user = await prisma.user.update(where={"id": id}, data=user.model_dump())
        # hash the password
        user.password = get_password_hash(user.password)
        await prisma.user.update(
            where={"id": user.id}, data={"password": user.password}
        )

        return userSchema(**user.model_dump())

    # delete a user
    async def delete_user(self, id: int) -> userSchema:
        user = await prisma.user.delete(where={"id": id})
        return userSchema(**user.model_dump())
