from services.base_service import BaseService
from models.article_model import ArticleModel


class ArticelService(BaseService):
    def __init__(self, *args, **kwargs):
        super(ArticelService, self).__init__(*args, **kwargs)

    def create_article(self, content, date, pic, title, author=''):
        article = ArticleModel(
            content=content,
            date=date,
            pic=pic,
            title=title,
            author=author
        )
        with self.session_scope() as session:
            session.add(article)
            session.commit()
        return True

    def articles(self):
        with self.session_scope() as session:
            articleList = session.query(ArticleModel).all()
        return articleList

    def update_article(self, article_id, content, date, pic, title, author):
        with self.session_scope() as session:
            article = session.query(ArticleModel) \
                .filter(ArticleModel.id == article_id).first()
            if not article:
                self.return_error(20002)
            article.content = content
            article.date = date
            article.title = title
            article.pic = pic
            article.author = author
            session.commit()
        return True

    def remove_article(self, article_id):
        with self.session_scope() as session:
            resource = session.query(ArticleModel) \
                .filter(ArticleModel.id == article_id).first()
            if not resource:
                self.return_error(20002)
            session.delete(resource)
            session.commit()
        return True
