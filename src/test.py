import boto3
import botocore
import os 
import random
from nltk.stem.wordnet import WordNetLemmatizer
import logging
import boto3.dynamodb.conditions as conditions
from decimal import Decimal
logger = logging.getLogger()

session = boto3.Session()
credentials = session.get_credentials()
dynamodb = session.resource('dynamodb', 'us-east-2')
wordle_dict_table = dynamodb.Table('wordle-dictionary')


def main():


    response = wordle_dict_table.scan(
        FilterExpression=conditions.Attr('WordLength').eq(5),
        ReturnConsumedCapacity='TOTAL',
        ProjectionExpression='Word'
    )
    words = response['Items']
    rand_indx = random.randint(0,len(words))
    print(words[rand_indx]['Word'])
if __name__ == "__main__":
    main()  

