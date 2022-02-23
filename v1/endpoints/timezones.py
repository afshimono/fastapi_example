from typing import Dict

from fastapi import (APIRouter, Depends, Response, status, HTTPException)
from core.exceptions import NotFound

from core.schemas.schema import TimezoneBase, TimezoneCreate, TimezoneUpdate
from core.service import TimezoneService
from core.models.database import postgres_repo
from auth import check_logged_is_admin, JWTBearer, check_logged_own_or_is_admin


router = APIRouter(prefix="/timezones",
                   tags=["timezones"],
                   responses={
                       404: {
                           "description": "Not found"
                       }
                   })

timezone_service = TimezoneService(repo=postgres_repo)


def get_timezone_service():
    return timezone_service


@router.get("/")
async def list_my_timezones(logged_user: Dict = Depends(JWTBearer()), timezone_service: TimezoneService = Depends(get_timezone_service)):
    return timezone_service.list_tz_by_user_id(logged_user["user_id"])


@router.get("/users/{user_id}")
async def list_user_timezones(user_id: int, logged_user: Dict = Depends(JWTBearer()), timezone_service: TimezoneService = Depends(get_timezone_service)):
    check_logged_is_admin(logged_user=logged_user)
    return timezone_service.list_tz_by_user_id(user_id)


@router.post("/")
async def create_my_timezone(tz: TimezoneCreate, logged_user: Dict = Depends(JWTBearer()), timezone_service: TimezoneService = Depends(get_timezone_service)):
    owner_id = logged_user["user_id"] if tz.owner_id is None else tz.owner_id
    check_logged_own_or_is_admin(logged_user=logged_user, user_id=owner_id)
    tz_kwargs = tz.dict()
    tz_kwargs.update({"owner_id": owner_id})
    tz_create = TimezoneCreate(**tz_kwargs)
    return timezone_service.create_tz(tz_create)


@router.put("/")
async def update_my_timezone(tz: TimezoneUpdate, logged_user: Dict = Depends(JWTBearer()), timezone_service: TimezoneService = Depends(get_timezone_service)):
    owner_id = logged_user["user_id"] if tz.owner_id is None else tz.owner_id
    check_logged_own_or_is_admin(logged_user=logged_user, user_id=owner_id)
    try:
        timezone_service.update_tz(tz)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, details=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.delete("/{tz_id}")
async def delete_timezone(tz_id: int, logged_user: Dict = Depends(JWTBearer()), timezone_service: TimezoneService = Depends(get_timezone_service)):
    tz_to_be_deleted = timezone_service.get_tz_by_id(tz_id)
    check_logged_own_or_is_admin(
        logged_user=logged_user, user_id=tz_to_be_deleted.owner_id)
    try:
        timezone_service.delete_tz(tz_id)
    except NotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=str(e)) from e
    return Response(status_code=status.HTTP_204_NO_CONTENT)
