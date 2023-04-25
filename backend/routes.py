from fastapi import FastAPI, status, HTTPException
from backend.validators import userValidator, loginValidator
from backend.models import User
from backend import db

app = FastAPI()

@app.get("/")
async def home():
    return "welcome"

@app.get("/users")
async def users():
    return db.query(User).all()

@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: userValidator):
    user = User(**request.dict())
    user.set_password(request.password)
    db.add(user)
    db.commit()
    return user

@app.post("/login", status_code=status.HTTP_200_OK)
async def login(request: loginValidator):
    user = db.query(User).filter(
        (User.email == request.username) | (User.username == request.username)
        ).first()
    if user:
        if user.check_password(request.password):
            return user
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect Password")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)