import requests
from datetime import datetime
from checklib import Status


class Helper:
    TCP_CONNECTION_TIMEOUT = 15

    def __init__(self, checker, port: int = 5000):
        self.c = checker
        self.port = port
        self.base_url = f"http://{checker.host}:{port}"
        self.session = requests.Session()

    def register(self, username: str, password: str) -> requests.Response:
        url = f"{self.base_url}/register"
        payload = {'username': username, 'password': password, 'password2': password}
        response = self.session.post(url=url, data=payload)
        return response

    def login(self, username: str, password: str) -> requests.Response:
        url = f"{self.base_url}/login"
        payload = {'username': username, 'password': password}
        response = self.session.post(url, data=payload)
        return response

    def profile(self) -> requests.Response:
        url = f"{self.base_url}/profile"
        response = self.session.get(url)
        return response

    def profile_api(self, user_id: str, token: str, payload: str) -> requests.Response:
        url = f"{self.base_url}/api/profile/{user_id}"
        headers = {'Authorization': f'Bearer {token}'}
        response = self.session.put(url, data=payload, headers=headers)
        return response

    def create_flag(self, token: str, flag: str) -> requests.Response:
        url = f"{self.base_url}/api/flags"
        created_at = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
        payload = {'flag': flag, 'created_at': created_at}
        headers = {'Authorization': f'Bearer {token}'}
        response = self.session.post(url, json=payload, headers=headers)
        return response

    def get_flag(self, flag_id: str, token: str) -> requests.Response:
        url = f"{self.base_url}/api/flags/{flag_id}"
        headers = {'Authorization': f'Bearer {token}'}
        response = self.session.get(url, headers=headers)
        return response

    def check_es(self, token: str) -> requests.Response:
        url = f"{self.base_url}/api/flags/check_es"
        headers = {'Authorization': f'Bearer {token}'}
        response = self.session.get(url, headers=headers)
        return response
