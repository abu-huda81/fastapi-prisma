from fastapi import APIRouter, Depends, HTTPException, status
from services.user_services import UserService
from schemas.user_schema import UserCreate, UserUpdate, User
from typing import List
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


# Get all users
@router.get("/", response_model=List[User], status_code=status.HTTP_200_OK)
async def get_users(user_service: UserService = Depends()):
    users = await user_service.get_users()
    if not users:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Users not found"
        )
    return users


# Get user by id
@router.get("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user(id: int, user_service: UserService = Depends()):
    user = await user_service.get_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# get user by email
@router.get("/email/{email}", response_model=User, status_code=status.HTTP_200_OK)
async def get_user_by_email(email: str, user_service: UserService = Depends()):
    user = await user_service.get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    return user


# create user
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, user_service: UserService = Depends()):
    user = await user_service.create_user(user)
    logger.info(f"User created: {user}")
    return user


# update user
@router.put("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def update_user(id: int, user: UserUpdate, user_service: UserService = Depends()):
    user = await user_service.update_user(id, user)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info(f"User updated: {user}")
    return user


# delete user
@router.delete("/{id}", response_model=User, status_code=status.HTTP_200_OK)
async def delete_user(id: int, user_service: UserService = Depends()):
    user = await user_service.delete_user(id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )
    logger.info(f"User deleted: {user}")
    return user
