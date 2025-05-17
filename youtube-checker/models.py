from sqlalchemy import Column, String, Boolean, DateTime, Float, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from config import DB_PATH

Base = declarative_base()

class VideoCheckResult(Base):
    __tablename__ = 'video_check_results'
    video_id = Column(String, primary_key=True)
    is_russian = Column(Boolean)
    checked_at = Column(DateTime, default=datetime.utcnow)
    channel_title = Column(String)
    channel_description = Column(String)
    country = Column(String)
    confidence = Column(Float)

# Create engine and session
engine = create_engine(f'sqlite:///{DB_PATH}')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

__all__ = ['Base', 'VideoCheckResult', 'Session'] 