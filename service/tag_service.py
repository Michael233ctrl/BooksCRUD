import crud
import utils


class TagService(utils.AppService):
    def get_tags(self) -> utils.ServiceResult:
        tags_db = crud.TagCRUD(self.db).get_tags()
        return utils.ServiceResult(tags_db)

    def delete_tag_for_book(self, book_id: int, tag_id: int) -> utils.ServiceResult:
        if crud.TagCRUD(self.db).delete_tag_for_book(book_id, tag_id):
            return utils.ServiceResult(utils.AppException.BookTagDoesNotExist())
        return utils.ServiceResult("Success!")
