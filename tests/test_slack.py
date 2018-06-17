import unittest
from pusher.slack import PushSlack
import inspect

class TestSlacker(unittest.TestCase):
    def setUp(self):
        self.pusher = PushSlack()

    def tearDown(self):
        pass

    def test_send_message(self):
        self.pusher.send_message("#general", "This is the 테스트 메세지")

if __name__ == "__main__":
    unittest.main()