from sqlalchemy import and_

import models
import utils


class TagCRUD(utils.AppCRUD):
    def get_tags(self):
        return self.db.query(models.Tag).all()

    def get_tag_by_id(self, tag_id: int):
        return self.db.query(models.Tag).where(models.Tag.id == tag_id).one_or_none()

    def get_tag_by_name(self, name: str):
        return self.db.query(models.Tag).where(models.Tag.name == name).first()

    def get_or_create_tag(self, tag_name: str):
        check_tag = self.get_tag_by_name(tag_name)
        if check_tag is not None:
            return check_tag
        tag_db = models.Tag(name=tag_name)
        self.db.add(tag_db)
        self.db.commit()
        self.db.refresh(tag_db)
        return tag_db

    def delete_tag_for_book(self, book_id: int, tag_id: int):
        query = (
            self.db.query(models.BookTags)
            .where(
                and_(
                    models.BookTags.book_id == book_id, models.BookTags.tag_id == tag_id
                )
            )
            .one_or_none()
        )
        if query is None:
            return True
        self.db.delete(query)
        self.db.commit()
