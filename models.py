from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    mobile = Column(String)
    password = Column(String)
    isAdmin = Column(Boolean)
    address = Column(String)
    bloodGroup = Column(String)
    organ_id = Column(Integer, ForeignKey("organs.id"), nullable=True)
    hospital_id = Column(Integer, ForeignKey('hospitals.id'), nullable=True)
    isAlive = Column(Boolean)
    isDonor = Column(Boolean)
    isReceipent = Column(Boolean)

class Organs(Base):
    __tablename__ = "organs"
    id = Column(Integer, primary_key=True, index=True)
    organ_name = Column(String)

class Hospital(Base):
    __tablename__ = "hospitals"
    id = Column(Integer, primary_key=True, index=True)
    hospital_name = Column(String)

organ = relationship("Organs", back_populates="users")
hospital = relationship("Hospital", back_populates="users")