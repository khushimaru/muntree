from sqlmodel import Session, select
from backend.models import Admin, Link

def create_admin(session: Session, admin: Admin):
    session.add(admin)
    session.commit()
    session.refresh(admin)
    return admin

def delete_admin(session: Session, id: int):
    admin = session.get(Admin, id)
    if admin:
        session.delete(admin)
        session.commit()

def get_admin_by_email(session: Session, email: str):
    return session.exec(select(Admin).where(Admin.email == email)).first()

def get_all_links(session: Session):
    links =  session.exec(select(Link).where(Link.visible == True)).all()
    return [link.model_dump(exclude={"visible"}) for link in links]

def get_admin_links(session: Session):
    return session.exec(select(Link)).all()

# Unnecessary
# def get_admin_link(session: Session, id: int):
#     return session.exec(select(Link).where(Link.id == id)).first()

def update_link(session: Session, link: Link):
    existing_link = session.get(Link, link.id)
    if not existing_link:
        return None

    update_data = link.model_dump(exclude_unset=True, exclude={"id", "created_at"})

    for key, value in update_data.items():
        setattr(existing_link, key, value)

    session.add(existing_link)
    session.commit()
    session.refresh(existing_link)
    return existing_link


def create_link(session: Session, link: Link):
    session.add(link)
    session.commit()
    session.refresh(link)
    return link

def delete_link(session: Session, link_id: int):
    link = session.get(Link, link_id)
    if link:
        session.delete(link)
        session.commit()
