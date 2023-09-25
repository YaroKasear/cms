from fastapi import FastAPI

from sqlmodel import Session, select, exists

from models import *
from database import *

app = FastAPI()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        if session.query(User).count():
            print('Yes')
        else:
            ownerUser = User(
                name='Owner',
                email='name@example.com',
                password_hash='none',
                password_salt='none'
            )
            ownerPermission = Permission(
                name='Owner',
                type=PermissionType.OWNER,
                role=PermissionRole.USER,
                users=[ownerUser]
            )
            ownerGroup = Group(
                name='Owner',
                users=[ownerUser],
                permissions=[ownerPermission]
            )
            session.add(ownerUser)
            session.commit()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/user/{user_name}")
async def get_user(user_name: str):
    with Session(engine) as session:
        try:
            user = session.exec(
                select(User).where(User.name == user_name)
            ).one()
        except:
            return {'error': 'not found'}

    return user.dict()
