from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from random import randint

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Users(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=1, max_length=100)
    mobile: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=1, max_length=100)
    isAdmin: bool = Field(default=False)
    address: str = Field(min_length=1, max_length=100)
    bloodGroup: str = Field(min_length=1, max_length=3)
    organ_id: int = Field()
    hospital_id: int = Field()
    isAlive: bool = Field(default=False)
    isDonor: bool = Field(default=False)
    isReceipent: bool = Field(default=False)

class Organs(BaseModel):
    organ_name: str = Field(min_length=1, max_length=100)

class Hospital(BaseModel):
    hospital_name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=100)

class Donations(BaseModel):
    doner_id: int = Field()
    recipient_id: int = Field()
    organ_id: int = Field()
    status: str = Field(min_length=1, max_length=100)

@app.get("/")
async def root(db:Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.isAdmin == True).first()
    if user_model is None:
        user_model = models.Users()
        user_model.first_name = "admin"
        user_model.last_name = ""
        user_model.email = "admin@gmail.com"
        user_model.mobile = ""
        user_model.password = "root"
        user_model.isAdmin = True
        db.add(user_model)
        db.commit()
    organCount = db.query(models.Organs).count()
    if organCount == 0:
        organs_data = [
            "kidney",
            "liver",
            "eye"
        ]
        for data in organs_data:
            organ_model = models.Organs()
            organ_model.organ_name = data
            db.add(organ_model)
        db.commit()
    hospitalCount = db.query(models.Hospital).count()
    if hospitalCount == 0:
        hospitals_data = [
            "Apollo Hospitals",
            "Medanta",
            "Fortis"
        ]
        for data in hospitals_data:
            hospital_model = models.Hospital()
            hospital_model.hospital_name = data
            db.add(hospital_model)
        db.commit()
    return {"message": "Hello World"}

@app.get("/getAllUsers")
async def read(db:Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/registerUser")
async def create(user: Users, db:Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.email == user.email).first()
    if user_model is None:
        user_model = models.Users()
        user_model.first_name = user.first_name.upper()
        user_model.last_name = user.last_name.upper()
        user_model.email = user.email.lower()
        user_model.mobile = user.mobile
        user_model.password = user.password
        user_model.isAdmin = False
        db.add(user_model)
        db.commit()
        return user
    else:
        raise HTTPException(status_code=404, detail="User already found")

@app.post("/authenticateUser")
async def create(email:str, password:str, db:Session = Depends(get_db)):
    user_model = db.query(models.Users).filter(models.Users.email == email).first()
    if user_model is None:
        raise HTTPException(status_code=404, detail="User not found")
    if password != user_model.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    return {"message": "Authentication successful", "token": user_model.id, "isAdmin": user_model.isAdmin}

@app.put("/forgotPassword")
async def forgot_password(email: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    temporary_password = str(randint(100000, 999999))
    user.password = temporary_password
    db.commit()
    return {"message": "Temporary password sent successfully", "temporaryPassword": temporary_password}

@app.put("/changePassword")
async def change_password(email: str, old_password:str, new_password:str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.email == email).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if old_password != user.password:
        raise HTTPException(status_code=401, detail="Incorrect password")
    user.password = new_password
    db.commit()
    return {"message": "Password Changed successfully"}

@app.post("/donateOrgan")
async def create(donation: Donations,user_id: int,db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user.isDonor:
        doner_model = models.Donations()
        doner_model.doner_id = donation.doner_id
        doner_model.recipient_id = donation.recipient_id
        doner_model.organ_id = donation.organ_id
        doner_model.status = donation.status
        db.add(doner_model)
        db.commit()
        return donation
    
@app.post("/receiveOrgan")
async def create(receive: Donations,user_id: int,db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user.isReceipent:
        receipent_model = models.Donations()
        receipent_model.doner_id = receive.doner_id
        receipent_model.recipient_id = receive.recipient_id
        receipent_model.organ_id = receive.organ_id
        receipent_model.status = receive.status
        db.add(receipent_model)
        db.commit()
        return receive

@app.get("/getOrgans")
async def read(db:Session = Depends(get_db)):
    return db.query(models.Organs).all()

@app.get("/getHospital")
async def read(db:Session = Depends(get_db)):
    return db.query(models.Hospital).all()

# @app.put("/put/{book_id}")
# async def update(book_id: int, book: Book, db:Session = Depends(get_db)):
#     book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
#     if book_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {book_id} : Does Not Exists"
#         )
#     book_model.title = book.title
#     book_model.author = book.author
#     book_model.description = book.description
#     book_model.rating = book.rating
#     db.add(book_model)
#     db.commit()
#     return book

# @app.put("/delete/{book_id}")
# async def delete(book_id: int, db:Session = Depends(get_db)):
#     book_model = db.query(models.Books).filter(models.Books.id == book_id).first()
#     if book_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {book_id} : Does Not Exists"
#         )
#     db.query(models.Books).filter(models.Books.id == book_id).delete()
#     db.commit()