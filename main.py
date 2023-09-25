from fastapi import FastAPI

from sqlmodel import Session, select

from models import *
from database import *

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    with Session(engine) as session:
        statement = select(User)


@app.get('/')
async def root():
    return {'message': "Hello World"}