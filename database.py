from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://neondb_owner:npg_tZOyNdj20Crq@ep-rough-mode-a1dhgduq-pooler.ap-southeast-1.aws.neon.tech/clustering_wilayah?sslmode=require"
)

engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependency (untuk tiap halaman pakai session sendiri)
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
