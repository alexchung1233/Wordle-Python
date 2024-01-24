import boto3


# import of this module maintains a persistant session
session = boto3.Session()
credentials = session.get_credentials()
dynamodb = session.resource('dynamodb')
dict_table = dynamodb.Table('wordle-dictionary')
data_table = dynamodb.Table('wordle-data')

class DBImpl:
    """DB implementation"""

    def get_table(name: str):
        return dynamodb.Table(name)

    def get_dict_table():
        return dict_table

    def get_data_table():
        return data_table