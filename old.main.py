   
# @app.post("/donateOrgan")
# async def create(donation: Donations,user_id: int,db:Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user.isDonor:
#         donor_model = models.Donations()
#         donor_model.donor_id = donation.donor_id
#         donor_model.recipient_id = donation.recipient_id
#         donor_model.organ_id = donation.organ_id
#         donor_model.status = donation.status
#         db.add(donor_model)
#         db.commit()
#         return donation
    
# @app.post("/receiveOrgan")
# async def create(receive: Donations,user_id: int,db:Session = Depends(get_db)):
#     user = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user.isRecipient:
#         receipent_model = models.Donations()
#         receipent_model.donor_id = receive.donor_id
#         receipent_model.recipient_id = receive.recipient_id
#         receipent_model.organ_id = receive.organ_id
#         receipent_model.status = receive.status
#         db.add(receipent_model)
#         db.commit()
#         return receive

# @app.get("/getDonor")
# async def read(db:Session = Depends(get_db)):
#     query = (
#         db.query(models.Users, models.Organs, models.Hospitals)
#         .join(models.Organs, models.Users.organ_id == models.Organs.id, isouter=True)
#         .join(models.Hospitals, models.Users.hospital_id == models.Hospitals.id, isouter=True)
#         .filter(models.Users.isDonor == True)
#         .all()
#     )
#     donor_data = []
#     for user, organ, hospital in query:
#         donor_data.append({
#             "user_id": user.id,
#             "first_name": user.first_name,
#             "last_name": user.last_name,
#             "email": user.email,
#             "mobile": user.mobile,
#             "address": user.address,
#             "bloodGroup": user.bloodGroup,
#             "organ_name": organ.organ_name if organ else None,
#             "hospital_name": hospital.hospital_name if hospital else None,
#             "isAlive": user.isAlive,
#             "isDonor": user.isDonor,
#             "isRecipient": user.isRecipient,
#         })
#     return donor_data

# @app.get("/getRecipient")
# async def read(db:Session = Depends(get_db)):
#     recepient = db.query(models.Users).filter(models.Users.isRecipient == True).all()
#     return recepient

# @app.put("/registerDR/{user_id}")
# async def create(user_id:int, user: Users, db:Session = Depends(get_db)):
#     user_model = db.query(models.Users).filter(models.Users.id == user_id).first()
#     if user_model is None:
#         raise HTTPException(
#             status_code=404,
#             detail=f"ID {user_id} : Does Not Exists"
#         )
#     user_model.address = user.address
#     user_model.bloodGroup = user.bloodGroup
#     user_model.organ_id = user.organ_id
#     user_model.hospital_id = user.hospital_id
#     user_model.isAlive = user.isAlive
#     user_model.isDonor = user.isDonor
#     user_model.isRecipient = user.isRecipient
#     db.add(user_model)
#     db.commit()
#     return user

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