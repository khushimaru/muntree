from fastapi import FastAPI
from app.routers import admin, links
from app.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(links.router, tags=["links"])
