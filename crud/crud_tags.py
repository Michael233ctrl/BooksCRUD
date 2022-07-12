from sqlalchemy import and_
from sqlalchemy.orm import Session

from models import Tag, BookTags


def get_tag_by_id(db: Session, tag_id: int):
    return db.query(Tag).where(Tag.id == tag_id).one_or_none()


def get_tag_by_name(db: Session, name: str):
    return db.query(Tag).where(Tag.name == name).first()


def get_or_create_tag(db: Session, tag_name: str):
    check_tag = get_tag_by_name(db, tag_name)
    if check_tag is not None:
        return check_tag

    tag_db = Tag(name=tag_name)
    db.add(tag_db)
    db.commit()
    db.refresh(tag_db)
    return tag_db


def delete_tag_for_book(db: Session, book_id, tag_id):
    query = (
        db.query(BookTags)
        .where(and_(BookTags.book_id == book_id, BookTags.tag_id == tag_id))
        .one_or_none()
    )
    if query is None:
        return

    db.delete(query)
    db.commit()
    return "Deleted!"
