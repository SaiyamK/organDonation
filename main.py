from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session, aliased
from random import randint
from fastapi.middleware.cors import CORSMiddleware
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from PIL import Image, ImageDraw, ImageFont

app = FastAPI()

origins = [
    "http://localhost.donation.com",
    "https://localhost.organdonation.com",
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    hospital_id: int = Field()
    isAlive: bool = Field(default=False)

class Organs(BaseModel):
    organ_name: str = Field(min_length=1, max_length=100)

class Hospital(BaseModel):
    hospital_name: str = Field(min_length=1, max_length=100)
    address: str = Field(min_length=1, max_length=100)

class Donations(BaseModel):
    donor_id: int = Field()
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
            "Kidney",
            "Liver",
            "Eye",
            "Heart",
            "Lungs",
            "Pancreas",
            "Intestines"
        ]
        for data in organs_data:
            organ_model = models.Organs()
            organ_model.organ_name = data
            db.add(organ_model)
        db.commit()
    hospitalCount = db.query(models.Hospital).count()
    if hospitalCount == 0:
        hospitals_data = [
            "Apollo Hospital",
            "Medanta",
            "Fortis Hospital",
            "BLK Hospital",
            "AIIMS",
            "Max Super Speciality Hospital"
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

@app.get("/getUsersByTokenId")
async def read(user_id:int, db:Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return user
        
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
        user_model.address = user.address
        user_model.bloodGroup = user.bloodGroup
        user_model.hospital_id = user.hospital_id
        user_model.isAlive = user.isAlive
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
    sender_email = 'saiyamkalra@gmail.com'
    recipient_email = user.email
    password = 'rlij yqlg yrio SECRET'
    subject = 'OTP For Password Reset - Organ Donation'
    body = f'Your OTP is {temporary_password}'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.quit()
    return {"message": "Temporary password sent successfully"}

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

@app.get("/getOrgans")
async def read(db:Session = Depends(get_db)):
    return db.query(models.Organs).all()

@app.get("/getHospital")
async def read(db:Session = Depends(get_db)):
    return db.query(models.Hospital).all()

@app.get("/previousContributions/{user_id}")
async def read(user_id: int, db: Session = Depends(get_db)):
    userR = aliased(models.Users)
    query = (
    db.query(models.Users, models.Donations, models.Organs, userR)
    .join(models.Donations, models.Donations.donor_id == models.Users.id, isouter=False)
    .join(models.Organs, models.Donations.organ_id == models.Organs.id, isouter=False)
    .join(userR, models.Donations.recipient_id == userR.id, isouter=True)
    .filter(models.Users.id == user_id)
    .all()
    )
    donor_data = []
    for donor, donations, organ, recipient in query:
        donation_status = donations.status
        organ_name = organ.organ_name
        recipient_name = f"{recipient.first_name} {recipient.last_name}" if recipient else None
        donor_data.append({
            "organ_name": organ_name,
            "recipient_name": recipient_name,
            "donation_status": donation_status
        })
    return donor_data

@app.put("/contribute/{user_id}/{organ_id}")
async def read(user_id: int, organ_id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    organ = db.query(models.Organs).filter(models.Organs.id == organ_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} : Does Not Exists"
        )
    if organ is None:
        raise HTTPException(
            status_code=404,
            detail=f"Organ ID {organ_id} : Does Not Exists"
        )
    donation_model = models.Donations()
    donation_model.donor_id = user_id
    donation_model.organ_id = organ_id
    db.add(donation_model)
    db.commit()
    return {"message": "Contribution Placed successfully"}

@app.get("/previousRequests/{user_id}")
async def read(user_id: int, db: Session = Depends(get_db)):
    userR = aliased(models.Users)
    query = (
    db.query(models.Users, models.Donations, models.Organs, userR)
    .join(models.Donations, models.Donations.recipient_id == models.Users.id, isouter=False)
    .join(models.Organs, models.Donations.organ_id == models.Organs.id, isouter=False)
    .join(userR, models.Donations.donor_id == userR.id, isouter=True)
    .filter(models.Users.id == user_id)
    .all()
    )
    donor_data = []
    for recipient, donations, organ, donor in query:
        donation_status = donations.status
        organ_name = organ.organ_name
        donor_name = f"{donor.first_name} {donor.last_name}" if donor else None
        donor_data.append({
            "organ_name": organ_name,
            "donor_name": donor_name,
            "donation_status": donation_status
        })
    return donor_data

@app.put("/request/{user_id}/{organ_id}")
async def read(user_id: int, organ_id: int, reason: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == user_id).first()
    organ = db.query(models.Organs).filter(models.Organs.id == organ_id).first()
    if user is None:
        raise HTTPException(
            status_code=404,
            detail=f"User ID {user_id} : Does Not Exists"
        )
    if organ is None:
        raise HTTPException(
            status_code=404,
            detail=f"Organ ID {organ_id} : Does Not Exists"
        )
    donation_model = models.Donations()
    donation_model.recipient_id = user_id
    donation_model.organ_id = organ_id
    donation_model.reason = reason
    db.add(donation_model)
    db.commit()
    return {"message": "Request Placed successfully"}

@app.get("/getAvailableOrgansForDonation")
async def read(db: Session = Depends(get_db)):
    query = (
    db.query(models.Users, models.Donations, models.Organs)
    .join(models.Donations, models.Donations.donor_id == models.Users.id, isouter=False)
    .join(models.Organs, models.Donations.organ_id == models.Organs.id, isouter=False)
    .filter(models.Donations.recipient_id.is_(None))
    .all()
    )
    donor_data = []
    for donor, donations, organ in query:
        donation_id = donations.id
        organ_name = organ.organ_name
        donor_name = donor.first_name +" " + donor.last_name
        donor_data.append({
            "donation_id": donation_id,
            "organ_name": organ_name,
            "donor_name": donor_name
        })
    return donor_data

@app.delete("/delete/{donation_id}")
async def delete(donation_id: int, db:Session = Depends(get_db)):
    donation_model = db.query(models.Donations).filter(models.Donations.id == donation_id).first()
    if donation_model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Donation ID {donation_id} : Does Not Exists"
        )
    db.query(models.Donations).filter(models.Donations.id == donation_id).delete()
    db.commit()
    return {"message": "Deleted"}

@app.get("/getRequests")
async def read(db: Session = Depends(get_db)):
    userR = aliased(models.Users)
    donationR = aliased(models.Donations)
    userD = aliased(models.Users)
    donationD = aliased(models.Donations)
    query = (
    db.query(userR, userD, donationR, donationD, models.Organs)
    .join(userR, userR.id == donationR.recipient_id, isouter=False)
    .join(userD, userD.id == donationD.donor_id, isouter=False)
    .join(donationD, donationR.organ_id == donationD.organ_id, isouter=False)
    .join(models.Organs, donationR.organ_id == models.Organs.id, isouter=False)
    .filter(donationD.recipient_id.is_(None))
    .filter(donationR.donor_id.is_(None))
    .filter(donationR.status == 'pending')
    .filter(donationD.status == 'pending')
    .all()
    )
    data = []
    for userR, userD, donationR, donationD, organ in query:
        donor_name = userD.first_name + " " + userD.last_name
        recipient_name = userR.first_name + " " + userR.last_name
        organ_name = organ.organ_name
        donation_recipient_table_id = donationR.id
        donation_donor_table_id = donationD.id
        organ_id = organ.id
        data.append({
            "donation_recipient_table_id": donation_recipient_table_id,
            "donation_donor_table_id": donation_donor_table_id,
            "donor_name": donor_name,
            "recipient_name": recipient_name,
            "organ_name": organ_name,
            "organ_id": organ_id
        })
    return data

@app.put("/approveRequest/{donation_recipient_table_id}/{donation_donor_table_id}/{organ_id}")
async def read(donation_recipient_table_id: int, donation_donor_table_id: int, organ_id: int, db: Session = Depends(get_db)):
    donationR = db.query(models.Donations).filter(models.Donations.id == donation_recipient_table_id).first()
    donationD = db.query(models.Donations).filter(models.Donations.id == donation_donor_table_id).first()
    donor = db.query(models.Users).filter(models.Users.id == donationD.donor_id).first()
    donation_model = models.Donations()
    donation_model.donor_id = donationD.donor_id
    donation_model.recipient_id = donationR.recipient_id
    donation_model.organ_id = organ_id
    donation_model.status = 'approved'
    db.add(donation_model)
    db.query(models.Donations).filter(models.Donations.id == donation_recipient_table_id).delete()
    db.query(models.Donations).filter(models.Donations.id == donation_donor_table_id).delete()
    db.commit()
    im = Image.open("cert.jpg")
    d = ImageDraw.Draw(im)
    location = (1300, 1150)
    text_color = (168, 131, 36)
    font = ImageFont.truetype("arial.ttf", 150)
    donorFullName = donor.first_name + " " + donor.last_name
    d.text(location, donorFullName, fill=text_color, font=font)
    cert_file_path = "certificate_" + donorFullName + ".pdf"
    im.save(cert_file_path)
    sender_email = 'saiyamkalra@gmail.com'
    recipient_email = donor.email
    password = 'rlij yqlg yrio SECRET'
    subject = 'Certificate and Thanks for Your Donation'
    body = f'Thanks for your donation! Please find the attached certificate.'
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = recipient_email
    message['Subject'] = subject
    message.attach(MIMEText(body, 'plain'))
    with open(cert_file_path, 'rb') as cert_file:
        cert_attachment = MIMEApplication(cert_file.read(), _subtype="pdf")
        cert_attachment.add_header('Content-Disposition', 'attachment', filename=f'certificate_{donorFullName}.pdf')
        message.attach(cert_attachment)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(sender_email, password)
    server.sendmail(sender_email, recipient_email, message.as_string())
    server.quit()
    return {"message": "Approved"}

@app.put("/rejectRequest/{donation_recipient_table_id}")
async def read(donation_recipient_table_id: int, db: Session = Depends(get_db)):
    donationR = db.query(models.Donations).filter(models.Donations.id == donation_recipient_table_id).first()
    if donationR is None:
        raise HTTPException(
            status_code=404,
            detail=f"Donation ID {donation_recipient_table_id} : Does Not Exists"
        )
    donationR.status = 'rejected'
    db.add(donationR)
    db.commit()
    return {"message": "Request Rejected"}