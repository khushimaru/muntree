from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.crud import get_all_links

router = APIRouter()

@router.get("/links")
def list_links(session: Session = Depends(get_session)):
    return get_all_links(session)
