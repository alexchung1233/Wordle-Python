import uuid
import impl.db_impl as db_impl
import exceptions
import botocore
import boto3.dynamodb.conditions as conditions

DBImpl = db_impl.DBImpl

class UserImpl:
    def __init__(self, user_name, user_id='') -> None:
        if not user_id:
            self.user_id: str = str(uuid.uuid4())
        else:
            self.user_id = user_id
        self.user_name = user_name
    
    @classmethod
    def create_user(cls, user_name):
        new_user = cls(user_name)
        new_user._write_user()
        return new_user
    
    def _write_user(self):
        table = DBImpl.get_data_table()
        table.put_item(Item={'UserID': self.user_id, 'GameID': 'UserInfo', 'UserName': self.user_name})

    @classmethod
    def get_user_info(cls, user_id):
        table = DBImpl.get_data_table()
        response = table.scan(FilterExpression=conditions.Attr('UserID').eq(user_id))
        if response['Items']:
            data = response['Items']
            return cls(user_name=data[0].get('UserName'), user_id=data[0].get('UserID'))
        raise exceptions.UserNotFound

    def to_dict(self):
        return {'user_id': self.user_id,
                'user_name': self.user_name}