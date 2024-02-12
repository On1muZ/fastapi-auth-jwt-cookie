from fastapi import FastAPI
import uvicorn
from auth.auth_jwt import router as auth_router


app = FastAPI(title="jwt and cookie auth")

app.include_router(auth_router, tags=['auth'])


if __name__ == "__main__":
    uvicorn.run('main:app', reload=True)