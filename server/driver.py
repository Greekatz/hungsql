import requests
import json


class Cursor:
    def __init__(self, connection):
        self.connection = connection
        self._results = []
    
    def execute(self, sql, params=None):
        payload = {"query": sql}
        response = requests.post(
            f"{self.connection.url}/query",
            json=payload,
            auth=(self.connection.username, self.connection.password)
        )
        if response.status_code != 200:
            raise Exception(f"Query failed: {response.text}")
        self._results = response.json().get("rows", [])

    
    def fetchall(self):
        return self._results
    
    def close(self):
        self._results = []

class Connection:
    def __init__(self, url, username, password):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password
    
    def cursor(self):
        return Cursor(self)
    
    def close(self):
        pass


def connect(url, username="admin", password="1234"):
    return Connection(url, username, password)