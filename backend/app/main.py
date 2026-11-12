
from fastapi import FastAPI

from app.api.public import router as public_router

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
