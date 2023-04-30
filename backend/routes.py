from fastapi import Depends, FastAPI, status, HTTPException
from sqlalchemy import Update
from backend import db
from backend.validators import UserValidator, LoginValidator, TaskValidator
from backend.models import User, Task
from backend.functions import generate_token, create_payload
from backend.dependencies import PermissionsChecker

app = FastAPI()


@app.get("/")
async def home():
    return "welcome"


@app.get("/users")
async def users(_: User = Depends(PermissionsChecker("view-user"))):
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
async def delete_user(user_id: int, _:User = Depends(PermissionsChecker("delete-user"))):
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        db.delete(user)
        db.commit()
    raise HTTPException(status.HTTP_404_NOT_FOUND)


@app.post("/create_task", status_code=status.HTTP_201_CREATED)
async def create_task(request: TaskValidator, user: User = Depends(PermissionsChecker("create-task"))):
    if request.department != user.department and user.position != 'chairman':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to be from the same department as the task to create it")
    task = Task(**request.dict())
    task.owner = user
    db.add(task)
    db.commit()
    return


@app.get("/tasks")
async def get_tasks(_: User = Depends(PermissionsChecker("view-task"))):
    return db.query(Task).all()

         
@app.put("/modify_task", status_code=status.HTTP_204_NO_CONTENT)
async def modify_task(request: TaskValidator, user: User = Depends(PermissionsChecker("modify-task"))):
    task = db.query(Task).filter((Task.date_created == request.date_created) & (Task.owner == user)).first()
    if task:
        if task.owner == user:
            if request.department == user.department or user.position == "chairman":
                task.update(**request.dict())
                db.commit()
                return
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to change the department of the task")
    raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You must be the owner of the task to modify it")


@app.delete('/delete_task/{task_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, user: User = Depends(PermissionsChecker("delete-task"))):
    task = db.query(Task).filter_by(id=task_id).first()
    if task:
        if task.owner == user or user.position == "chairman":
            db.delete(task)
            db.commit()
            return
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='you do not have permission to delete this task')
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="task not found")

