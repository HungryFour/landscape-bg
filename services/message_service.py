from services.base_service import BaseService
from models.message_model import MessageModel


class MessageService(BaseService):
    def __init__(self, *args, **kwargs):
        super(MessageService, self).__init__(*args, **kwargs)

    def create_message(self, name, tel, email, content):
        message = MessageModel(
            name=name,
            tel=tel,
            email=email,
            content=content
        )
        with self.session_scope() as session:
            session.add(message)
            session.commit()
        return True

    def messages(self):
        with self.session_scope() as session:
            messageList = session.query(MessageModel).all()
        return messageList
