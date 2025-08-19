from fastapi import FastAPI
from auth_jwt.auth import router

app = FastAPI()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "Welcome to the sign-language application!"}
