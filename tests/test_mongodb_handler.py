import unittest
import inspect
from db.mongodb.mongo_db_handler import MongoDBHandler


class MongoDBHandlerTestCase(unittest.TestCase):


    @classmethod
    def setUpClass(cls):
        print(inspect.stack()[0][3])
        cls.mongodb = MongoDBHandler("local", "coiner", "price_info")
        """
        cls.mongodb.delete_items({})
        docs = [
            {"currency": "btc", "price": 10000},
            {"currency": "eth", "price": 1000},
            {"currency": "xrp", "price": 100},
            {"currency": "btc", "price": 20000},
            {"currency": "eth", "price": 2000},
            {"currency": "xrp", "price": 200}
        ]
        cls.mongodb.insert_items(docs)
        """
    @classmethod
    def tearDownClass(cls):
        pass

    def setUp(self):
        print(inspect.stack()[0][3])


    def tearDown(self):
        pass


    def no_test_set_db_collection(self):
        """
        test set_db
        :return:
        """
        print(inspect.stack()[0][3])
        self.mongodb.set_db_collection("trader", "trade_status")
        self.assertEqual(self.mongodb.get_current_db_name(), "trader")
        self.assertEqual(self.mongodb.get_current_collection_name(), "trade_status")

    def no_test_get_db_name(self):
        print(inspect.stack()[0][3])
        dbname = self.mongodb.get_current_db_name()
        self.assertEqual(dbname, "coiner")

    def no_test_get_collection_name(self):
        print(inspect.stack()[0][3])
        collection_name = self.mongodb.get_current_collection_name()
        self.assertEqual(collection_name, "price_info")

    def no_test_insert_item(self):
        print(inspect.stack()[0][3])
        doc = {"item": "item0", "name": "test_insert_item"}
        id = self.mongodb.insert_item(doc)
        assert id
        print(id)

    def no_test_insert_items(self):
        print(inspect.stack()[0][3])
        docs = [
                {"item": "item1", "name": "test_insert_items"},
                {"item": "item2", "name": "test_insert_items"}
               ]
        ids = self.mongodb.insert_items(docs)
        assert ids
        print(ids)

    def no_test_delete_items(self):
        print(inspect.stack()[0][3])

    def test_find_item(self):
        print(inspect.stack()[0][3])
        doc = self.mongodb.find_item({"currency": "btc"})
        print(doc)

    def test_find_items(self):
        print(inspect.stack()[0][3])
        cursor = self.mongodb.find_items({"currency": "eth"})
        assert cursor
        for doc in cursor:
            print(doc)

if __name__ == "__main__":
    unittest.main()


