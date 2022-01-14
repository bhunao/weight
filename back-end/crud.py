from datetime import datetime
from sqlalchemy.orm import Session

from . import models, schemas


def get_weights(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Weight).offset(skip).limit(limit).all()


def create_user_weight(db: Session, weight: schemas.WeightCreate):
    date = datetime.now()
    db_weight = models.Weight(**weight.dict(), date=date)
    db.add(db_weight)
    db.commit()
    db.refresh(db_weight)
    return db_weight

def get_weight_by_id(db: Session, id: int):
    return db.query(models.Weight).filter(models.Weight.id == id).first()