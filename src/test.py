import boto3
session = boto3.Session()
credentials = session.get_credentials()

dynamodb = session.client('dynamodb')
print(credentials.get_frozen_credentials())
print(dynamodb.list_tables())
# table = dynamodb.Table('worlde_dictionary')
# print(table.get_item(Key={"WordID":"hello001"}))