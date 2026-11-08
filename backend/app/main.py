from fastapi import FastAPI

app = FastAPI(
    title="Campus Voice API",
    description="Backend API for the Campus Voice system",
    version="1.0.0"
)
@app.get("/")
def root():
    return {"message": "Welcome to Campus Voice API"}