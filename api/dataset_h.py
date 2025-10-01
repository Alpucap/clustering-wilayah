from sqlalchemy.orm import Session
from models import ClusteringDatasetH

def create_dataset_header(db: Session, user_id: int, dataset_name: str, description: str = None):
    header = ClusteringDatasetH(
        user_id=user_id,
        dataset_name=dataset_name,
        description=description
    )
    db.add(header)
    db.commit()
    db.refresh(header)
    return header

def get_datasets_by_user(db: Session, user_id: int):
    return db.query(ClusteringDatasetH).filter(ClusteringDatasetH.user_id == user_id).all()
