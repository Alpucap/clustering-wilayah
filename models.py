from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class ClusteringDatasetH(Base):
    __tablename__ = "clustering_dataset_h"
    clustering_dataset_h_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False)
    dataset_name = Column(String(100), nullable=False)
    description = Column(String(200))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="datasets")
    details = relationship("ClusteringDatasetD", back_populates="header")


class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    datasets = relationship("ClusteringDatasetH", back_populates="user")
    
class ClusteringDatasetD(Base):
    __tablename__ = "clustering_dataset_d"
    clustering_dataset_d_id = Column(Integer, primary_key=True, index=True)
    clustering_dataset_h_id = Column(Integer, ForeignKey("clustering_dataset_h.clustering_dataset_h_id", ondelete="CASCADE"), nullable=False)
    tahun = Column(Integer, nullable=False)
    kabupaten_kota = Column(String(100), nullable=False)
    angka_harapan_hidup = Column(DECIMAL(5,2))
    persentase_penduduk_miskin = Column(DECIMAL(5,2))
    index_kedalaman_kemiskinan = Column(DECIMAL(5,2))
    index_keparahan_kemiskinan = Column(DECIMAL(5,2))
    rata_rata_lama_sekolah = Column(DECIMAL(5,2))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    header = relationship("ClusteringDatasetH", back_populates="details")
