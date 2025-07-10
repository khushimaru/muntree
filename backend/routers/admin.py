from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session
from utils.database import get_session
from utils.models import Admin, Link
from utils.auth import verify_password, create_jwt, decode_jwt
from utils.crud import create_admin, get_admin_by_email, create_link, get_admin_links, delete_link, update_link

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

from utils.config import ADMIN_REGISTRATION_KEY, REGISTRATION_ENABLED
from utils.auth import hash_password
from pydantic import BaseModel

class RegisterAdminRequest(BaseModel):
    email: str
    password: str
    registration_key: str

@router.post("/register")
def register_admin(
    body: RegisterAdminRequest,
    session: Session = Depends(get_session)
):
    if REGISTRATION_ENABLED == 0:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Registrations for new admins are disabled, please contact muntree@jkartik.in for help.")
    if body.registration_key != ADMIN_REGISTRATION_KEY:
        raise HTTPException(status_code=403, detail="Invalid registration key")

    existing_admin = get_admin_by_email(session, body.email)
    if existing_admin:
        raise HTTPException(status_code=400, detail="Admin with this email already exists")

    hashed_pw = hash_password(body.password)
    new_admin = Admin(email=body.email, hashed_password=hashed_pw)
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
