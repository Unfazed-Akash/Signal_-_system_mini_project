from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Persistent SQLite DB
DATABASE_URL = "sqlite:///./kavach_titanium.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class ATM(Base):
    __tablename__ = "atms"
    id = Column(String, primary_key=True, index=True)
    city = Column(String, index=True)
    location = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    status = Column(String, default="ONLINE") # ONLINE, MAINTENANCE, ATTACK_MODE

class Suspect(Base):
    __tablename__ = "suspects"
    id = Column(String, primary_key=True)
    name = Column(String)
    risk_score = Column(Float)
    last_seen_city = Column(String)
    history_fraud_count = Column(Integer, default=0)

class Transaction(Base):
    __tablename__ = "transactions"
    txn_id = Column(String, primary_key=True, index=True)
    atm_id = Column(String, ForeignKey("atms.id"))
    sender_id = Column(String) # Masked account or user ID
    amount = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)
    lat = Column(Float)
    lng = Column(Float)
    city = Column(String)
    
    # Analysis Fields
    is_fraud = Column(Boolean, default=False)
    fraud_probability = Column(Float, default=0.0)
    fraud_type = Column(String, nullable=True) # VELOCITY, ANOMALY, PATTERN, NULL
    
    # Intervention
    status = Column(String, default="SUCCESS") # SUCCESS, DECLINED_FRAUD, PENDING_VERIFICATION

class FraudReport(Base):
    __tablename__ = "fraud_reports"
    report_id = Column(Integer, primary_key=True, index=True)
    reporter_name = Column(String)
    description = Column(String)
    fraud_category = Column(String) # UPI, HACKING, etc.
    status = Column(String, default="OPEN")
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
