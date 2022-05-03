from fastapi import FastAPI
from mongoengine import connect
from routes.authors import router as router_author, PREFIX_AUTHORS
from routes.editions import router as router_edition, PREFIX_EDITIONS
from routes.books import router as router_books, PREFIX_BOOKS
import uvicorn
import os

if os.environ.get('DOCKER_RUNNING', False):
    connect(db='library', host='mongodb', port=27017)
else:
    connect(db='library', host='localhost', port=27017)

app = FastAPI()
app.include_router(router_author, prefix=PREFIX_AUTHORS, tags=["authors"])
app.include_router(router_edition, prefix=PREFIX_EDITIONS, tags=["editions"])
app.include_router(router_books, prefix=PREFIX_BOOKS, tags=["books"])
