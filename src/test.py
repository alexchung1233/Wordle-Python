import boto3
dynamodb = boto3.client('dynamodb')
print(dynamodb.list_tables())
# table = dynamodb.Table('worlde_dictionary')
# print(table.get_item(Key={"WordID":"hello001"}))