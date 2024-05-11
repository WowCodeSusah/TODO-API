from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func

class User(Base):
    __tablename__ = "Users"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    dateOfBirth = Column(String, nullable=False)
    email = Column(String, nullable=False)
    timeCreated = Column(DateTime(timezone=True), server_default=func.now())
    
    
    