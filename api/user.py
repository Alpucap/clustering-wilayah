from sqlalchemy.orm import Session
from models import User
import bcrypt

#Method untuk create user
def create_user(db: Session, username: str, email: str, password: str):
    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    user = User(username=username, email=email, password=hashed_pw)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#Method untuk get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

#Method untuk get user by username
def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

#Method untuk verifikasi password
def verify_password(password: str, hashed: str) -> bool:
    return bcrypt.checkpw(password.encode(), hashed.encode())

#Method untuk get user by id
def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.user_id == user_id).first()

