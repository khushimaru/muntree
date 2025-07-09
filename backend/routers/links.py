from fastapi import APIRouter, Depends
from sqlmodel import Session
from backend.utils.database import get_session
from backend.utils.crud import get_all_links

router = APIRouter()

@router.get("/links")
def list_links(session: Session = Depends(get_session)):
    return get_all_links(session)
