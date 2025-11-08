from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import streamlit as st

DATABASE_URL = st.secrets["DB_URL"]

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
