from fastapi import FastAPI, HTTPException

from sqlmodel import Session, select, col

from models import User, Group, Permission, PermissionType, PermissionCategory
from database import engine, create_db_and_tables

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if session.query(User).count():
            print("Yes")
        else:
            owner_user = User(
                name="owner",
                email="name@example.com",
                password_hash="none",
                password_salt="none",
            )
            owner_user.permissions.append(
                Permission(type=PermissionType.READ, category=PermissionCategory.USER)
            )
            owner_user.permissions.append(
                Permission(type=PermissionType.UPDATE, category=PermissionCategory.USER)
            )
            owner_group = Group(name="owner", users=[owner_user])
            session.add(owner_group)
            session.commit()


@app.get("/api/user/{user_name}")
async def get_user(user_name: str):
    with Session(engine) as session:
        user = session.exec(
            select(User.name, User.id).where(col(User.name) == user_name)
        ).first()

    if user is not None:
        return user
    else:
        raise HTTPException(status_code=404, detail=f"User {user_name} not found!")
