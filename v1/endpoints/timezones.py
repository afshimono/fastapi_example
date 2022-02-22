from fastapi import APIRouter

from core.schemas.schema import TimezoneBase

router = APIRouter(prefix="/timezones",
                   tags=["timezones"],
                   responses={
                       404: {
                           "description": "Not found"
                       }
                   })


@router.get("/")
async def list_timezones():
    pass


@router.post("/")
async def create_timezone(tz: TimezoneBase):
    return {"email": "test@test.com"}


@router.put("/")
async def change_timezone(tz: TimezoneBase):
    return {"email": "test@test.com"}


@router.delete("/{tz_id}")
async def delete_timezone(tz_id: int):
    return {"email": "test@test.com"}
