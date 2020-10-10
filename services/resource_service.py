from services.base_service import BaseService
from models.resource_model import ResourceModel


class ResourceService(BaseService):
    def __init__(self, *args, **kwargs):
        super(ResourceService, self).__init__(*args, **kwargs)

    def create_resource(self, video, cover_pic, title, info, category, director, is_video):
        resource = ResourceModel(
            video=video,
            cover_pic=cover_pic,
            title=title,
            info=info,
            category=category,
            director=director,
            is_video=is_video
        )
        with self.session_scope() as session:
            session.add(resource)
            session.commit()
        return True

    def resources(self):
        with self.session_scope() as session:
            resourcesList = session.query(ResourceModel).all()
        return resourcesList

    def update_resource(self, resource_id, video, cover_pic, title, info, category, director, is_video):
        with self.session_scope() as session:
            resource = session.query(ResourceModel) \
                .filter(ResourceModel.id == resource_id).first()

            if not resource:
                self.return_error(20002)

            resource.video = video
            resource.cover_pic = cover_pic
            resource.title = title
            resource.category = category
            resource.director = director
            resource.info = info
            resource.is_video = is_video

            session.commit()
        return True

    def remove_resource(self, resource_id):
        with self.session_scope() as session:
            resource = session.query(ResourceModel) \
                .filter(ResourceModel.id == resource_id).first()
            if not resource:
                self.return_error(20002)
            session.delete(resource)
            session.commit()
        return True
