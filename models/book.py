from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db.base import Base


class Book(Base):
    __tablename__ = "book"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, unique=True)
    publisher = Column(String, index=True, nullable=False)
    author = Column(String, nullable=False)
    pages = Column(String)
    tags = relationship("Tag", secondary="book_tags", back_populates="books")
    created_at = Column(DateTime(timezone=True), default=datetime.utcnow)
    updated_at = Column(
        DateTime(timezone=True), onupdate=datetime.utcnow, default=datetime.utcnow
    )


class BookTags(Base):
    __tablename__ = "book_tags"

    id = Column(Integer, primary_key=True)
    book_id = Column(Integer, ForeignKey("book.id", ondelete="SET NULL"))
    tag_id = Column(Integer, ForeignKey("tag.id", ondelete="SET NULL"))
