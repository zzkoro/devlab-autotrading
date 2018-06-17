import configparser
from machine.base_machine import Machine
import requests
import time

class KorbitMachine(Machine):
    """
    코빗 거래소와의 거래를 위한 클래스입니다.
    BASE_API_URL은 REST API 호출을 위한 기본 URL입니다.
    TRADE_CURRENCY_TYPE은 코빗에서 거래가 가능한 화폐의 종류입니다.
    """

    BASE_API_URL = "https://api.korbit.co.kr"
    TRADE_CURRENCY_TYPE = ["btc", "bch", "btg", "eth", "etc", "xrp", "krw"]

    def __init__(self):
        """
        KorbitMachine 클래스에서 가장 먼저 호출되는 메서드입니다.
        config.ini에서 client_id, client_secret, username, password 정보를 읽어옵니다.
        """
        config = configparser.ConfigParser()
        config.read('conf/config.ini')

        self.CLIENT_ID = config['KORBIT']['client_id']
        self.CLIENT_SECRET = config['KORBIT']['client_secret']
        self.USER_NAME = config['KORBIT']['username']
        self.PASSWORD = config['KORBIT']['password']

        self.access_token = None
        self.refresh_token = None
        self.token_type = None

    def set_token(self, grant_type="password"):
        """액세스 토큰 정보를 만들기 위한 메서드입니다.

        Returns:
            만료시간(expire), 액세스 토큰(access_token), 리프레시토큰(refresh_token)을 반환합니다.

        Raises:
            grant_type이 password나 refresh_token이 아닌 경우 Exception을 발생시킵니다

        """

        token_api_path = "/v1/oauth2/access_token"
        url_path = self.BASE_API_URL + token_api_path

        if grant_type == "password":
            data = {
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "username": self.USER_NAME,
                "password": self.PASSWORD,
                "grant_type": grant_type
            }
        elif grant_type == "refresh_token":
            data = {
                "client_id": self.CLIENT_ID,
                "client_secret": self.CLIENT_SECRET,
                "refresh_token": self.refresh_token,
                "grant_type": grant_type
            }
        else:
            raise Exception("Unexcpected grant_type")

        res = requests.post(url_path, data=data)
        result = res.json()

        self.access_token = result["access_token"]
        self.token_type = result["token_type"]
        self.refresh_token = result["refresh_token"]
        self.expire = result["expires_in"]

        return self.expire, self.access_token, self.refresh_token

    def get_token(self):
        """액세스 토큰 정보를 받기 위한 메서드입니다

        Returns:
            액세스 토큰(access_token)이 있는 경우 반환합니다

        Raises:
            access_token이 없는 경우 Exception을 발생시킵니다
        """

        if self.access_token is not None:
            return self.access_token
        else:
            raise Exception("Need to set_token")

    def get_ticker(self, currency_type=None):
        """마지막 체결정보(Tick)를 구하는 메서드입니다.
        Args:
            currency_type(str): 화폐의 종류를 입력받습니다. 화폐의 종류는 TRADE_CURRENCY_TYPE에 정의돼 있습니다.

        Returns:
            결과를 딕셔너리로 반환합니다.
            결과 필드는 timestamp, last, bid, ask, high, low, volume으로 구성됩니다.

        Raise:
            currency_type이 없으면 Exception을 발생시킵니다
        """

        if currency_type is None:
            raise Exception('Need to currency type')
        time.sleep(1)

        params = {'currency_pair': currency_type}
        ticker_api_path = "/v1/ticker/detailed"
        url_path = self.BASE_API_URL + ticker_api_path
        res = requests.get(url_path, params=params)
        response_json = res.json()
        result = {}
        result["timestamp"] = str(response_json["timestamp"])
        result["last"] = str(response_json["last"])
        result["bid"] = str(response_json["bid"])
        result["ask"] = str(response_json["ask"])
        result["high"] = str(response_json["high"])
        result["low"] = str(response_json["low"])
        result["volume"] = str(response_json["volume"])
        return result


    def get_filled_orders(self, currency_type=None, per="minute"):
        """체결 정보를 구하는 메서드입니다

        Args:
            currency_type(str): 화폐의 종류를 입력받습니다 화폐의 종류는 TRADE_CURRENCY_TYPE에 저의돼 있습니다
            per(str): minute, hour, day로 체결정보를 받아올 시각을 지정합니다

        Returns:
            최근 체결 정보를 딕셔너리의 리스트 형태로 반환합니다.
        """

        if currency_type is None:
            raise Exception("Need to currency_type")
        time.sleep(1)
        params = {'currency_pair': currency_type, 'time': per}
        orders_api_path = "/v1/transactions"
        url_path = self.BASE_API_URL + orders_api_path
        res = requests.get(url_path, params=params)
        result = res.json()
        for item in result:
            item["coin"] = currency_type

        print(result)

        return result


    def get_wallet_status(self):
        """사용자의 지갑정보를 조회하는 메서드입니다

        Returns:
            사용자의 지갑에 화폐별 잔액을 딕셔너리 형태로 반환합니다
        """

        time.sleep(1)
        wallet_status_api_path = "/v1/user/balances"
        url_path = self.BASE_API_URL + wallet_status_api_path
        headers = {"Authorization": "Bearer " + self.access_token}
        res = requests.get(url_path, headers=headers)
        result = res.json()
        wallet_status = { currency: dict(avail=result[currency]["available"]) for currency in self.TRADE_CURRENCY_TYPE }
        for item in self.TRADE_CURRENCY_TYPE:
            wallet_status[item]["balance"] = str(float(result[item]["trade_in_use"]) + float(result[item]["withdrawal_in_use"]))
        return wallet_status