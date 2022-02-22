from fastapi import APIRouter

from core.schemas.schema import UserCreateOrUpdate, UserBase

router = APIRouter(prefix="/users",
                   tags=["users"],
                   responses={
                       404: {
                           "description": "Not found"
                       }
                   })


@router.post("/login")
async def login():
    return {"access_token": "xyz"}


@router.post("/")
async def create_user(user: UserCreateOrUpdate):
    return {"email": "test@test.com"}


@router.patch("/")
async def change_password(user: UserCreateOrUpdate):
    return {"email": "test@test.com"}


@router.delete("/{user_id}")
async def delete_user(user_id: int):
    return {"email": "test@test.com"}
