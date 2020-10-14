from controllers.base_controllers import BaseController
from services.message_service import MessageService


class MessageController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        self.get_argument_dict(must_keys=["user_id"])
        message_list = MessageService().messages()

        result_list = []
        for message in message_list:
            result = {
                "id": message.id,
                "created_at": str(message.created_at),
                "name": message.name,
                "tel": message.tel,
                "email": message.email,
                "content": message.content
            }
            result_list.append(result)

        return {
            "code": 0,
            "msg": "success",
            "data": result_list
        }


class CreateMessageController(BaseController):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def post(self):
        arg = self.get_argument_dict(must_keys=["name", "tel", "email", "content"], check_token=False)

        result = MessageService().create_message(
            name=arg.get("name"),
            tel=arg.get("tel"),
            email=arg.get("email"),
            content=arg.get("content"))
        return {
            "code": 0,
            "msg": "success",
            "data": result
        }
