import boto3
import botocore
import os 
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
import logging
import uuid


logger = logging.getLogger()

WORD_MIN = 5
WORD_MAX = 8

nltk.download('wordnet')

session = boto3.Session()
credentials = session.get_credentials()
dynamodb = session.resource('dynamodb', 'us-east-2')
wordle_dict_table = dynamodb.Table('wordle-dictionary')

def write(words):

    try:
        with wordle_dict_table.batch_writer() as writer:
            count = 1
            for word, word_length in words:
                print(f'{count}: Writing word {word}')
                writer.put_item(Item={'Word': word, 'WordLength': word_length})
                count +=1
    except botocore.exceptions.ClientError as err:
        logger.error(
            "Couldn't load data into table %s. Here's why: %s: %s",
            wordle_dict_table.name,
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
        raise

def main():
    Lem = WordNetLemmatizer()
    file_dir = os.path.dirname(os.path.realpath('__file__'))
    word_path = f"{file_dir}/src/10000-list.txt"
    filtered_words = []

    with open(word_path, mode='r') as f:
        for word in f.readlines():
            if len(word) <= WORD_MAX and len(word) >= WORD_MIN:

                # cleans up to remove \n
                word = word.replace('\n', '')

                # removes plural words
                lemword = Lem.lemmatize(word)
                filtered_words.append((lemword, len(lemword)))
    unique_words = set(filtered_words)
    print(f"Total unique_words {len(unique_words)}")
    write(unique_words)

if __name__ == "__main__":
    main()

