from fastapi import FastAPI
import uvicorn

from v1.endpoints import users, timezones

app = FastAPI()


app.include_router(users.router)
app.include_router(timezones.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
