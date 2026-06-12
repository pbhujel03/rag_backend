from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.models.base import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)
    filename = Column(String)
    file_type = Column(String)
    chunk_count = Column(Integer)
    chunking_strategy = Column(String)
    uploaded_at = Column(DateTime, default=datetime.utcnow)