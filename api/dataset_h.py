from sqlalchemy.orm import Session
from models import ClusteringDatasetH

#Method untuk add dataset header
def add_dataset_header(db: Session, user_id: int, dataset_name: str, description: str = None):
    header = ClusteringDatasetH(
        user_id=user_id,
        dataset_name=dataset_name,
        description=description
    )
    db.add(header)
    db.commit()
    db.refresh(header)
    return header

#Method untuk get dataset header by user id
def get_datasets_by_user(db: Session, user_id: int):
    return db.query(ClusteringDatasetH).filter(ClusteringDatasetH.user_id == user_id).all()
