from controllers.base_controllers import BaseController
from services.article_service import ArticelService


class UserGetArticelController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        article_list = ArticelService().articles()
        result_list = []
        for article in article_list:
            result = {
                "id": article.id,
                "created_at": str(article.created_at),
                "content": article.content,
                "date": article.date,
                "title": article.title,
                "pic": article.pic,
                "author": article.author,
            }
            result_list.append(result)
        return {
            "code": 0,
            "msg": "success",
            "data": result_list
        }


class ArticelController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        self.get_argument_dict(must_keys=["user_id"])
        article_list = ArticelService().articles()
        result_list = []
        for article in article_list:
            result = {
                "id": article.id,
                "created_at": str(article.created_at),
                "content": article.content,
                "date": article.date,
                "title": article.title,
                "pic": article.pic,
                "author": article.author,
            }
            result_list.append(result)
        return {
            "code": 0,
            "msg": "success",
            "data": result_list
        }


class CreateArticelController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["content", "date", "pic", "title"])
        result = ArticelService().create_article(content=arg.get("content"),
                                                 date=arg.get("date"),
                                                 pic=arg.get("pic"),
                                                 title=arg.get("title"),
                                                 author=arg.get("author"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class UploadArticelController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["id"])
        result = ArticelService().update_article(article_id=arg.get("id"),
                                                 content=arg.get("content"),
                                                 date=arg.get("date"),
                                                 pic=arg.get("pic"),
                                                 title=arg.get("title"),
                                                 author=arg.get("author"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }


class RemoveArticelController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["id"])
        result = ArticelService().remove_article(article_id=arg.get("id"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }
