from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, ForeignKey, JSON, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime

# Persistent SQLite DB for Dev (PostgreSQL compatible schema)
DATABASE_URL = "sqlite:///./kavach_titanium.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# --- Core Entities ---

class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True, index=True) # UUID
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, index=True)
    account_numbers = Column(JSON) # List of account numbers
    risk_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    transactions = relationship("Transaction", back_populates="user")
    complaints = relationship("Complaint", back_populates="user")

class Fraudster(Base):
    __tablename__ = "fraudsters"
    fraudster_id = Column(String, primary_key=True, index=True)
    identified_patterns = Column(JSON) # e.g., {"common_ip": "1.2.3.4"}
    risk_level = Column(String) # HIGH, CRITICAL
    associated_accounts = Column(JSON)
    detection_date = Column(DateTime, default=datetime.utcnow)
    
    alerts = relationship("FraudAlert", back_populates="fraudster")

class ATM(Base):
    __tablename__ = "atms"
    id = Column(String, primary_key=True, index=True)
    city = Column(String, index=True)
    location = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    status = Column(String, default="ONLINE")

# --- Operational Data ---

class Transaction(Base):
    __tablename__ = "transactions"
    txn_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=True) # Linked to User if known
    
    # Core Transaction Details
    amount = Column(Float)
    currency = Column(String, default="INR")
    merchant = Column(String)
    merchant_category = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    # Location & Device
    geo_lat = Column(Float)
    geo_lon = Column(Float)
    city = Column(String)
    device_fingerprint = Column(String)
    ip_address = Column(String)
    
    # ML Features (Stored for audit/retraining)
    features = Column(JSON) # velocity, account_age, etc.
    
    # Analysis Results
    is_fraud = Column(Boolean, default=False)
    fraud_probability = Column(Float, default=0.0)
    fraud_type = Column(String) # ANOMALY, PATTERN, VELOCITY_CHECK
    status = Column(String, default="PROCESSING") # PROCESSING, SUCCESS, BLOCKED
    
    user = relationship("User", back_populates="transactions")
    alerts = relationship("FraudAlert", back_populates="transaction")

class FraudAlert(Base):
    __tablename__ = "fraud_alerts"
    alert_id = Column(String, primary_key=True)
    transaction_id = Column(String, ForeignKey("transactions.txn_id"))
    fraudster_id = Column(String, ForeignKey("fraudsters.fraudster_id"), nullable=True)
    
    severity = Column(String) # MEDIUM, HIGH, SEVERE
    description = Column(String)
    predicted_location = Column(JSON) # Lat/Lon for interception
    timestamp = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="NEW") # NEW, INVESTIGATING, RESOLVED
    
    transaction = relationship("Transaction", back_populates="alerts")
    fraudster = relationship("Fraudster", back_populates="alerts")

class Complaint(Base):
    __tablename__ = "complaints"
    ticket_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=True)
    
    reporter_name = Column(String)
    contact_email = Column(String)
    mobile_no = Column(String)
    account_no = Column(String)
    
    fraud_type = Column(String) # PHISHING, CLONING, UPI_FRAUD
    description = Column(Text)
    evidence_path = Column(String, nullable=True)
    
    status = Column(String, default="OPEN") # OPEN, IN_PROGRESS, RESOLVED, REJECTED
    priority = Column(String, default="MEDIUM")
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="complaints")

class AuditLog(Base):
    __tablename__ = "audit_logs"
    log_id = Column(Integer, primary_key=True, autoincrement=True)
    action = Column(String)
    entity_id = Column(String)
    details = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

def init_db():
    Base.metadata.create_all(bind=engine)
    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
