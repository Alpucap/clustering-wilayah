from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.dialects.postgresql import JSON

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

class ActivityLog(Base):
    __tablename__ = "activity_log"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)

    metode_clustering = Column(String(50), nullable=False)
    fitur_digunakan = Column(JSON, nullable=False)
    tahun_awal = Column(Integer, nullable=False)
    tahun_akhir = Column(Integer, nullable=False)
    jumlah_cluster = Column(Integer)
    metrik_jarak = Column(String(50), nullable=False)

    silhouette = Column(String(50))
    dbi = Column(String(50))
    waktu_komputasi = Column(String(50))

    created_at = Column(TIMESTAMP, server_default=func.now())
    
    user = relationship("User")
