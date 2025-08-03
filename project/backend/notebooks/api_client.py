import time
import requests


class AutoJWTClient:
    def __init__(self, base_url, login_url, email, password, verify=True):
        self.base_url = base_url.rstrip("/")
        self.login_url = login_url
        self.email = email
        self.password = password
        self.verify = verify 

        self.access_token = None
        self.refresh_token = None
        self.token_expiry = 0  # epoch time

        self.session = requests.Session()
        self._login()

    def _login(self):
        response = self.session.post(
            f"{self.base_url}{self.login_url}",
            json={"email": self.email, "password": self.password},
            verify=self.verify  
        )
        if response.status_code != 200:
            raise Exception("Login failed")

        data = response.json()
        self.access_token = data["access"]
        self.refresh_token = data.get("refresh")
        self.token_expiry = self._decode_expiry(self.access_token)

    def _decode_expiry(self, token):
        import base64
        import json

        try:
            payload = token.split('.')[1]
            padding = '=' * (-len(payload) % 4)
            decoded = base64.urlsafe_b64decode(payload + padding)
            exp = json.loads(decoded)["exp"]
            return exp
        except Exception:
            return 0

    def _refresh_token_if_needed(self):
        now = time.time()
        if now >= self.token_expiry - 10:  # 10s buffer
            if not self.refresh_token:
                self._login()
            else:
                response = self.session.post(
                    f"{self.base_url}/auth/token/refresh/",
                    json={"refresh": self.refresh_token},
                    verify=self.verify  
                )
                if response.status_code != 200:
                    self._login()
                else:
                    data = response.json()
                    self.access_token = data["access"]
                    self.token_expiry = self._decode_expiry(self.access_token)

    def request(self, method, path, **kwargs):
        self._refresh_token_if_needed()

        headers = kwargs.pop("headers", {})
        headers["Authorization"] = f"Bearer {self.access_token}"
        kwargs["headers"] = headers

        kwargs.setdefault("verify", self.verify) 

        url = f"{self.base_url}{path}"
        return self.session.request(method, url, **kwargs)

    def get(self, path, **kwargs):
        return self.request("GET", path, **kwargs)

    def post(self, path, **kwargs):
        return self.request("POST", path, **kwargs)

    def put(self, path, **kwargs):
        return self.request("PUT", path, **kwargs)

    def delete(self, path, **kwargs):
        return self.request("DELETE", path, **kwargs)
