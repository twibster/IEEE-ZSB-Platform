from fastapi import Depends, FastAPI, status, HTTPException
from backend import db
from backend.validators import userValidator, loginValidator
from backend.models import User
from backend.functions import generateToken, create_payload
from backend.dependencies import leaderRequired

app = FastAPI()


@app.get("/")
async def home():
    return "welcome"


@app.get("/users")
async def users(user: User = Depends(leaderRequired)):
    return db.query(User).all()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: userValidator):
    user = db.query(User).filter(
        (User.email == request.username) | (User.username == request.username)
        ).first()
    if user:
        return "user already exists"
    user = User(**request.dict())
    user.set_password(request.password)
    db.add(user)
    db.commit() 
    return generateToken(create_payload(user))


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(request: loginValidator):
    user = db.query(User).filter(
        (User.email == request.username) | (User.username == request.username)
        ).first()
    if user:
        if user.check_password(request.password):
            return generateToken(create_payload(user))
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect Password")
    raise HTTPException(status.HTTP_404_NOT_FOUND)
