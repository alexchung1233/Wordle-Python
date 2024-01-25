"""Impl class containing logic to handle dictionary words"""
import impl.db_impl as db_impl
import exceptions

DBImpl = db_impl.DBImpl

class DictionaryImpl:

    @classmethod
    def add_word(cls, word: str):
        table = DBImpl.get_dict_table()
        if cls.check_if_exists(word):
            raise exceptions.DuplicateWord
        table.put_item(Item={'Word': word, 'WordLength': len(word)})
    
    @classmethod
    def check_if_exists(cls, word: str):
        table = DBImpl.get_dict_table()

        response = table.get_item(Key={'Word': word, 'WordLength': len(word)})
        if response.get('Item'):
            return True
        return False