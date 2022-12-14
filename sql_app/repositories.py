from sqlalchemy.orm import Session

from . import models, schemas
class student:
    class Config:
        orm_mode = True
    async def create(db: Session, item: schemas.StudentCreate):
        db_item = models.Student(First_Name=item.First_Name,Last_Name=item.Last_Name,DOB=item.DOB,Amount_Due=item.Amount_Due)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    
    def fetch_by_id(db: Session,_id):
        return db.query(models.Student).filter(models.Student.id == _id).first()
    
    def fetch_by_first_name(db: Session,name):
        return db.query(models.Student).filter(models.Student.First_Name == name).first()
    
    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Student).offset(skip).limit(limit).all()
    
    async def delete(db: Session,item_id):
        db_item= db.query(models.Student).filter_by(id=item_id).first()
        db.delete(db_item)
        db.commit()
        
        
    async def update(db: Session,item_data):
        updated_item = db.merge(item_data)
        db.commit()
        return updated_item
