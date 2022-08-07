from sqlalchemy import Column, ForeignKey, Integer, String, Float

from db import Base

class Student(Base):
    class Config:
        orm_mode = True
    __tablename__="Student"
    id = Column('id',Integer,primary_key=True)
    First_Name = Column('first_name',String(255))
    Last_Name = Column('last_name',String(255))
    DOB = Column('dob',String(255))
    Amount_Due = Column('amount_due',Float)


    def __repr__(self):
        return f"Student(name={self.First_Name +' '+self.Last_Name}, dob={self.DOB}, amount_due = {self.Amount_Due})"
    
    def json(self):
        
        return {'Student ID': self.id, 
                'First Name': self.First_Name, 
                'Last Name': self.Last_Name, 
                'Date of Birth': self.DOB,
                'Amount Due': self.Amount_Due}
        
    