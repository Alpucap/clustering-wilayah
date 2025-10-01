from sqlalchemy.orm import Session
from models import ClusteringDatasetD

def add_dataset_detail(db: Session, header_id: int, tahun: int, kabupaten: str, ahh: float, p0: float, p1: float, p2: float, rls: float):
    detail = ClusteringDatasetD(
        clustering_dataset_h_id=header_id,
        tahun=tahun,
        kabupaten_kota=kabupaten,
        angka_harapan_hidup=ahh,
        persentase_penduduk_miskin=p0,
        index_kedalaman_kemiskinan=p1,
        index_keparahan_kemiskinan=p2,
        rata_rata_lama_sekolah=rls
    )
    db.add(detail)
    db.commit()
    db.refresh(detail)
    return detail

def get_details_by_header(db: Session, header_id: int):
    return db.query(ClusteringDatasetD).filter(
        ClusteringDatasetD.clustering_dataset_h_id == header_id
    ).all()
