import boto3
import botocore
import boto3.dynamodb.conditions as conditions

session = boto3.Session()
credentials = session.get_credentials()
dynamodb = session.resource('dynamodb')

class DBImpl:
    def get_table(name: str):
        return dynamodb.Table(name)

    def get_dict_table():
        return dynamodb.Table('wordle-dictionary')