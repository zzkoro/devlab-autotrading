from slacker import Slacker
from pusher.base_pusher import Pusher
import configparser

class PushSlack(Pusher):
    def __init__(self):
        """
        슬랙으로 메시지를 보내기 위한 PushSlack의 __init__ 메서드

        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')
        token = config['SLACK']['token']
        self.slack = Slacker(token)

    def send_message(self, thread="#general", message=None):
        """
        메세지 전송
        :param thread:
        :param message:
        :return:
        """
        self.slack.chat.post_message(thread, message)