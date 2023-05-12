from fastapi import Depends, FastAPI, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.validators import UserValidator, TaskValidator
from api.const import Positions
from api.db.models import User, Task
from api.functions import create_payload, generate_token, create_token_json
from api.depend import PermissionsChecker, get_db

app = FastAPI()


@app.get("/", tags=["home"])
async def home():
    return RedirectResponse("/docs")


@app.get("/users", tags=["users"])
async def users(
        db: Session = Depends(get_db),
        _: User = Depends(PermissionsChecker("view_user"))):
    return db.query(User).all()


@app.post("/register", tags=["users"], status_code=status.HTTP_201_CREATED)
async def register(
        request: UserValidator,
        db: Session = Depends(get_db)):
    user = User(**request.dict())
    user.set_password(request.password)
    db.add(user)
    db.commit()
    return create_token_json(generate_token(create_payload(user)))


@app.post("/login", tags=["users"], status_code=status.HTTP_200_OK)
async def login(
        form_data: OAuth2PasswordRequestForm = Depends(),
        db: Session = Depends(get_db)):
    user = db.query(User).filter(
        (User.email == form_data.username) | (User.username == form_data.username)
        ).first()
    if user:
        if user.check_password(form_data.password):
            return create_token_json(generate_token(create_payload(user)))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Incorrect Password")
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail='user not found')


@app.delete("/delete_user/{user_id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: int,
        _:User = Depends(PermissionsChecker("delete_user")),
        db: Session = Depends(get_db)):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        db.delete(user)
        db.commit()
        return
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")


@app.put("/modify_user/{user_id}", tags=["users"], status_code=status.HTTP_204_NO_CONTENT)
async def modify_user(
        user_id: int,
        request: UserValidator,
        user: User = Depends(PermissionsChecker("modify_user")),
        db: Session = Depends(get_db)
        ):
    to_modify = db.query(User).filter_by(id=user_id).first()
    if to_modify:
        if to_modify == user:
            user.update(**request.dict())
            db.commit()
            return
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="you do not have access to modify this account")
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="user not found")


@app.post("/create_task", tags=["tasks"], status_code=status.HTTP_201_CREATED)
async def create_task(
        request: TaskValidator,
        user: User = Depends(PermissionsChecker("create_task")),
        db: Session = Depends(get_db)
        ):
    if request.department != user.department and user.position != Positions.CHAIRMAN:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "You need to be from the same department as the task to create it")
    task = Task(**request.dict())
    task.owner = user
    db.add(task)
    db.commit()
    return


@app.get("/tasks", tags=["tasks"])
async def get_tasks(
        db: Session = Depends(get_db),
        _: User = Depends(PermissionsChecker("view_task"))
        ):
    return db.query(Task).all()

         
@app.put("/modify_task/{task_id}", tags=["tasks"], status_code=status.HTTP_204_NO_CONTENT)
async def modify_task(
        task_id: int,
        request: TaskValidator,
        user: User = Depends(PermissionsChecker("modify_task")),
        db: Session = Depends(get_db)
        ):
    task = db.query(Task).filter_by(id=task_id).first()
    if task:
        if task.owner == user:
            if request.department == user.department or user.position == Positions.CHAIRMAN:
                task.update(**request.dict())
                db.commit()
                return
            raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You do not have permission to change the department of the task")
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="You must be the owner of the task to modify it")
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="task not found")
    

@app.delete('/delete_task/{task_id}', tags=["tasks"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
        task_id: int,
        user: User = Depends(PermissionsChecker("delete_task")),
        db: Session = Depends(get_db)
        ):
    task = db.query(Task).filter_by(id=task_id).first()
    if task:
        if task.owner == user or user.position == Positions.CHAIRMAN:
            db.delete(task)
            db.commit()
            return
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail='you do not have permission to delete this task')
    raise HTTPException(status.HTTP_404_NOT_FOUND, detail="task not found")

