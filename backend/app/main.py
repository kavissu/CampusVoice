
from fastapi import FastAPI

from app.api.public import router as public_router
from app.api.auth import router as auth_router
from app.api.users import router as users_router

app = FastAPI(
    title="Campus Voice API",
    description="Backend API for the Campus Voice system",
    version="1.0.0"
)

# Register the public API router
app.include_router(
    public_router,
    prefix="/api/v1"
)


@app.get("/")
def root():
    return {"message": "Welcome to Campus Voice API"}


app.include_router(
    auth_router,
    prefix="/api/v1/auth"
)

app.include_router(
    users_router,
    prefix="/api/v1/users",
    tags=["Users"]
)

