import crud
import utils
import schemas


class TagService(utils.AppService):
    async def get_tags(self) -> utils.ServiceResult:
        tags_db = crud.TagCRUD(self.db).get_tags()
        return utils.ServiceResult(tags_db)

    def update_tag(self, tag_id: int, tag: schemas.TagCreate) -> utils.ServiceResult:
        tag_by_id = crud.TagCRUD(self.db).get_tag_by_id(tag_id)
        tag_by_name = crud.TagCRUD(self.db).get_tag_by_name(tag.name)
        if tag_by_name is not None and tag_by_name.id != tag_by_id.id:
            return utils.ServiceResult(
                utils.AppException.TagUpdate(
                    context={
                        "message": f"Id mismatch! Tag with name: "
                        f"'{tag_by_name.name}' has id: '{tag_by_name.id}', not '{tag_id}'"
                    }
                )
            )
        if not (tag_db := crud.TagCRUD(self.db).update_tag(tag_id, tag)):
            return utils.ServiceResult(utils.AppException.TagUpdate())
        return utils.ServiceResult(tag_db)

    def delete_tag(self, tag_id: int) -> utils.ServiceResult:
        if crud.TagCRUD(self.db).delete_tag(tag_id):
            return utils.ServiceResult(utils.AppException.TagGet())
        return utils.ServiceResult("Success!")
