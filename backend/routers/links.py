from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend.database import get_session
from backend.crud import get_all_links

router = APIRouter()

@router.get("/links")
def list_links(session: Session = Depends(get_session)):
    return get_all_links(session)
