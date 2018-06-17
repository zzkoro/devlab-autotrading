from pymongo import MongoClient
from pymongo.cursor import CursorType
import configparser

from db.base_handler import DBHandler

class MongoDBHandler(DBHandler):
    """
    PyMongo를 래핑해서 사용하는 클래스입니다 DBHandler 추상 클래스를 상속합니다.
    리모트 DB와 로컬DB를 모두 사용할 수 있도록 __init__에서 mode로 구분합니다.
    """
    def __init__(self, mode="local", db_name=None, collection_name=None):
        """
        MongoDBHandler __init__ 구현부

        :param mode: 로컬DB인지 리모트DB 인지 구분합니다 예) "local", "remote"
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받습니다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받습니다.

        :returns: None

        :raises: db_name과 collection_name이 없으면 Exception을 발생시킵니다

        """

        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        self.db_config = config['MONGODB']

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))
        elif mode == "local":
            self._client = MongoClient("mongodb://{user}:{password}@{local_ip}:{port}".format(**self.db_config))

        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def set_db_collection(self, db_name=None, collection_name=None):
        """
        MongoDB에서 작업하려는 데이터베이스와 콜렉션을 변경할때 사용합니다.

        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받습니다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받습니다.
        :return: None
        :raises: db_name이 없으면 Exception을 발생시킵니다.
        """
        if db_name is None:
            raise Exception("Need to dbname name")

        self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

    def get_current_db_name(self):
        """
        현재 MongoDB에서 작업중인 데이터베이스의 이름을 반환합니다.

        :return: self._db.name: 현재 사용중인 데이터베이스 이름을 반환
        """
        return self._db.name

    def get_current_collection_name(self):
        """
        현재 MongoDB에서 작업 중인 콜렉션의 이름을 반환합니다.

        :return: self._collection.name: 현재 사용중인 콜렉션 이름을 반환
        """
        return self._collection.name

    def insert_item(self, data, db_name=None, collection_name=None):
        """
        MongoDB에 하나의 문서를 입력하기 위한 메서드입니다.

        :param data:
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받습니다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받습니다.
        :return:
            inserted_id: 입력 완료된 문서의 ObjectId를 반환합니다
        """
        if db_name is not None:
            self.db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.insert_one(data).inserted_id

    def insert_items(self, datas, db_name=None, collection_name=None):
        """
        MongoDB에 다수의 문서를 입력하기 위한 메서드입니다.

        :param data:
        :param db_name: MongoDB에서 데이터베이스에 해당하는 이름을 받습니다.
        :param collection_name: 데이터베이스에 속하는 콜렉션 이름을 받습니다.
        :return:
            inserted_ids: 입력 완료된 문서의 ObjectId 리스트를 반환합니다
        """
        if db_name is not None:
            self.db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.insert_many(datas).inserted_ids

    def delete_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에서 다수의 문서를 삭제하는 메소드

        :param condition:
        :param db_name:
        :param collection_name:
        :return:
            DeleteResult: PyMongo의 문서 삭제 결과 객체
        """
        if condition is None:
            raise Exception("Need to condition")
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

        return self._collection.delete_many(condition)

    def find_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에서 다수의 문서를 검색하기 위한 메서드입니다.

        :param condition: 검색조건
        :param db_name: 데이터베이스명
        :param collection_name: 콜렉션 이름
        :return: Cursor를 반환
        """
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)


    def find_item(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB에서 하나의 문서를 검새하기 위한 메서드

        :param condition: 검색조건
        :param db_name: 데이터베이스명
        :param collection_name: 콜렉션 이름
        :return: document
        """
        if condition is None:
            condition = {}
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find_one(condition)


