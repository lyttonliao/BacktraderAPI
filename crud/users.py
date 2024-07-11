from sqlalchemy.orm import Session

from ..models import user as user_model
from ..schemas import user as user_schema

def get_user_by_email(db: Session, email: str):
    return db.query(user_model.User).filter(user_model.User.email == email).first()

def get_user(db: Session, user_id: int):
    return db.query(user_model.User).filter(user_model.User.id == user_id).first()

def create_user(db: Session, user: user_schema.UserCreate):
    db_user = user_model.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
