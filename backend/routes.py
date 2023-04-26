from fastapi import Depends, FastAPI, status, HTTPException
from backend import db
from backend.validators import UserValidator, LoginValidator, TaskValidator
from backend.models import User, Task
from backend.functions import generate_token, create_payload
from backend.dependencies import RoleChecker

app = FastAPI()


@app.get("/")
async def home():
    return "welcome"


@app.get("/users")
async def users(_: User = Depends(RoleChecker("chairman"))):
    return db.query(User).all()


@app.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: UserValidator):
    user = db.query(User).filter(
        (User.email == request.username) | (User.username == request.username)
        ).first()
    if user:
        return "user already exists"
    user = User(**request.dict())
    user.set_password(request.password)
    db.add(user)
    db.commit()
    return generate_token(create_payload(user))


@app.post("/login", status_code=status.HTTP_200_OK)
async def login(request: LoginValidator):
    user = db.query(User).filter(
        (User.email == request.username) | (User.username == request.username)
        ).first()
    if user:
        if user.check_password(request.password):
            return generate_token(create_payload(user))
        raise HTTPException(status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect Password")
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.delete("/delete_user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: int, _:User = Depends(RoleChecker("chairman"))):
    user = db.query(User).filter_by(id=user_id).first()
    db.delete(user)
    db.commit()
    return


@app.post("/create_task", status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskValidator, user: User = Depends(RoleChecker("leader"))):
    task = Task(**request.dict())
    task.owner = user
    db.add(task)
    db.commit()
    return
