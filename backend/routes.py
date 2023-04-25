from fastapi import FastAPI, status, HTTPException
from backend.validators import userValidator, loginValidator
from backend.models import User

users_db = []

app = FastAPI()

@app.get("/")
async def home():
    return "welcome"

@app.get("/users")
async def users():
    return users_db

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: userValidator):
    user = User(**request.dict())
    user.set_password(request.password)
    users_db.append(user)
    return user

@app.post("/login", status_code=status.HTTP_200_OK)
async def login(request: loginValidator):
    for user in users_db:
        if request.username in [user.email, user.username]:
            if user.check_password(request.password):
                return user
            raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect Password")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)