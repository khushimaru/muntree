from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from backend.database import get_session
from backend.models import Admin, Link
from backend.auth import verify_password, create_jwt, decode_jwt
from backend.crud import create_admin, get_admin_by_email, create_link, get_admin_links, delete_link, update_link

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/admin/login")

def get_current_admin(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = decode_jwt(token)
        if payload.get("sub") != "admin":
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
        return payload
    except Exception:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

# Registration should not be exposed by default.
from backend.config import ADMIN_REGISTRATION_KEY
from fastapi import Query
from backend.auth import hash_password
@router.post("/register")
def register_admin(
    admin_data: Admin,
    registration_key: str = Query(...),
    session: Session = Depends(get_session)
):
    if registration_key != ADMIN_REGISTRATION_KEY:
        raise HTTPException(status_code=403, detail="Invalid registration key")

    existing_admin = get_admin_by_email(session, admin_data.email)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    hashed_pw = hash_password(admin_data.hashed_password)
    new_admin = Admin(email=admin_data.email, hashed_password=hashed_pw)
    create_admin(session, new_admin)

    return {"ok": True}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    admin = get_admin_by_email(session, form_data.username)
    if not admin or not verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt({"sub": "admin"})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/links")
def read_links(admin: dict = Depends(get_current_admin), session: Session = Depends(get_session)):
    return get_admin_links(session)

@router.post("/links")
def add_link(link: Link, admin: dict = Depends(get_current_admin), session: Session = Depends(get_session)):
    return create_link(session, link)

@router.delete("/links/{link_id}")
def remove_link(link_id: int, admin: dict = Depends(get_current_admin), session: Session = Depends(get_session)):
    delete_link(session, link_id)
    return {"ok": True}

@router.patch("/links/{link_id}")
def edit_link(
    link_id: int,
    link_data: Link,
    admin: dict = Depends(get_current_admin),
    session: Session = Depends(get_session)
):
    link_data.id = link_id

    updated_link = update_link(session, link_data)
    if not updated_link:
        raise HTTPException(status_code=404, detail="Link not found")

    return {"ok": True, "link": updated_link}
