from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session

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
    return {"message": "Hello World"}

@app.get("/getAllUsers")
async def read(db:Session = Depends(get_db)):
    return db.query(models.Users).all()

@app.post("/registerUser")
async def create(user: Users, db:Session = Depends(get_db)):
    user_model = models.Users()
    user_model.first_name = user.first_name
    user_model.last_name = user.last_name
    user_model.email = user.email
    user_model.mobile = user.mobile
    user_model.password = user.password
    user_model.isAdmin = False
    db.add(user_model)
    db.commit()
    return user

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