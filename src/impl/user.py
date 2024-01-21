import uuid


class UserImpl:
    def __init__(self, user_name) -> None:
        self.user_id: str = uuid.uuid4()
        self.user_name = user_name
    
    @classmethod
    def create_user(cls, user_name):
        new_user = cls(user_name)

    @classmethod
    def get_user_info(cls, user_id):
        pass

    def to_dict(self):
        pass