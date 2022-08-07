from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sql_app import models
from db import get_db, engine
import sql_app.models as models
import sql_app.schemas as schemas
from sql_app.repositories import student
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder

app = FastAPI(title="Assignment_3 FastAPI Application",
    description="FastAPI Application with Swagger and Sqlalchemy")

models.Base.metadata.create_all(bind=engine)


@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.get('/')
def welcome():
    return "Welcome to the CRUD-Fast-API home page written by Navaneeth and Isaac. Please navigate to /docs for swagger documentation. Please navigate to https://github.com/navaneethjawahar/FastAPI-CRUD for the code"

@app.post('/student', response_model=schemas.Item,status_code=201)
async def create_student(item_request: schemas.StudentCreate, db: Session = Depends(get_db)):
    """
    Create a student record and store it in the database
    """
    
    db_item = student.fetch_by_first_name(db, name=item_request.First_Name)
    if db_item:
        raise HTTPException(status_code=400, detail="Item already exists!")

    return await student.create(db=db, item=item_request)

@app.get('/student',response_model=List[schemas.Item])
def get_students(db: Session = Depends(get_db)):
    """
    Get all the students stored in the database
    """
    # if name:
    #     items =[]
    #     db_item = student.fetch_by_first_name(db,name)
    #     items.append(db_item)
    #     return items
    # else:
    return student.fetch_all(db)


@app.get('/student/{id}', response_model=schemas.Item)
def get_item(id: int,db: Session = Depends(get_db)):
    """
    Get the student record with the given ID provided by User stored in database
    """
    db_item = student.fetch_by_id(db,id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    return db_item

@app.delete('/student/{id}', tags=["Item"])
async def delete_item(id: int,db: Session = Depends(get_db)):
    """
    Delete the Item record with the given ID provided by User stored in database
    """
    db_item = student.fetch_by_id(db,id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found with the given ID")
    await student.delete(db,id)
    return "Item deleted successfully!"

@app.put('/student/{id}', tags=["Item"],response_model=schemas.Item)
async def update_item(id: int,item_request: schemas.Item, db: Session = Depends(get_db)):
    """
    Update the student record stored in the database
    """
    db_item = student.fetch_by_id(db, int(id))
    if db_item:
        update_item_encoded = jsonable_encoder(item_request)
        db_item.First_Name = update_item_encoded['First_Name']
        db_item.price = update_item_encoded['Last_Name']
        db_item.DOB = update_item_encoded['DOB']
        db_item.Amount_Due = update_item_encoded['Amount_Due']
        return await student.update(db=db, item_data=db_item)
    else:
        raise HTTPException(status_code=400, detail="Item not found with the given ID")
    
  

if __name__ == "__main__":
    uvicorn.run("index:app", port=9000, reload=True,debug=True)     