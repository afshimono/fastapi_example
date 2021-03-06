from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, Response, status
from core.exceptions import AuthError, DeleteError, NotFound, InsertError

from core.schemas.schema import UserCreate, UserSignUp, UserUpdate
from core.service import UserService
from core.models.database import postgres_repo
from auth import get_logged_credentials, jwt_token_handler, check_logged_is_admin, check_logged_own_or_is_admin

user_service = UserService(repo=postgres_repo)


def get_user_service() -> UserService:
    return user_service


router = APIRouter(prefix="/v1/users",
                   tags=["users"],
                   responses={
                       404: {
                           "description": "Not found"
                       }
                   })


@router.post("/login")
async def login(cred: UserSignUp, user_service: UserService = Depends(get_user_service)):
    try:
        if user := user_service.verify_pwd(cred.password, cred.email):
            payload = {
                "email": user.email,
                "is_admin": user.is_admin,
                "user_id": user.id
            }
            token = jwt_token_handler.create_access_token(data=payload)
            return {"access_token": token, "type": "bearer"}
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    except AuthError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e)) from e


@router.post("/signup")
async def signup(user: UserSignUp, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.create_user(UserCreate(is_admin=False, **user.dict()))
    except InsertError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.post("/")
async def create_user(user: UserCreate, logged_user: Dict = Depends(get_logged_credentials), user_service: UserService = Depends(get_user_service)):
    check_logged_is_admin(logged_user)
    try:
        return user_service.create_user(user)
    except InsertError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)) from e


@router.get("/")
async def list_users(logged_user: Dict = Depends(get_logged_credentials), user_service: UserService = Depends(get_user_service)):
    check_logged_is_admin(logged_user)
    return user_service.list_users()


@router.put("/")
async def update_user(user: UserUpdate, logged_user: Dict = Depends(get_logged_credentials), user_service: UserService = Depends(get_user_service)):
    check_logged_is_admin(logged_user)
    try:
        user_service.update_user(user)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{user_id}")
async def delete_user(user_id: int, logged_user: Dict = Depends(get_logged_credentials), user_service: UserService = Depends(get_user_service)):
    check_logged_own_or_is_admin(logged_user, user_id)
    try:
        user_service.delete_user(user_id=user_id)
    except DeleteError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)
