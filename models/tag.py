from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.base import Base


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    books = relationship(
        "Book", secondary="book_tags", back_populates="tags", lazy="joined"
    )
