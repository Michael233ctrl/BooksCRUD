from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from db.session import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    publisher = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(DateTime(timezone=True), default=datetime.utcnow)
