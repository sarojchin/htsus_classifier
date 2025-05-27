from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# Database URL - you'll need to set this environment variable
#DATABASE_URL = "postgresql://postgres:Ortega20.01!@localhost:5432/customs_classifier"

#hosted on render
DATABASE_URL = "postgresql://classifications_user:xtliZyoPJwILVIhSYkwQbd4iRLBkGSsd@dpg-d0ppp7euk2gs739tvq50-a/classifications"

# Create SQLAlchemy engine  
engine = create_engine(DATABASE_URL)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class
Base = declarative_base()

class Classification(Base):
    __tablename__ = "classifications"

    id = Column(Integer, primary_key=True, index=True)
    product_description = Column(String)
    classification_result = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

# Create tables     
Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 