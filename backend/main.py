from fastapi import FastAPI
from routers import admin, links
from utils.database import create_db_and_tables

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

app.include_router(admin.router, prefix="/admin", tags=["admin"])
app.include_router(links.router, tags=["links"])

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Allows all origins, adjust as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)