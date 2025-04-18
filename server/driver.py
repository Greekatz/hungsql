import requests
import json
from abc import ABC, abstractmethod


# Abstract Transport Layer
class Transport(ABC):
    @abstractmethod
    def post_query(self, sql: str) -> dict:
        pass


class HTTPTransport(Transport):
    def __init__(self, url, username, password):
        self.url = url.rstrip("/")
        self.username = username
        self.password = password

    def post_query(self, sql: str) -> dict:
        payload = {"query": sql}
        response = requests.post(
            f"{self.url}/query",
            json=payload,
            auth=(self.username, self.password)
        )
        if response.status_code != 200:
            raise Exception(f"Query failed: {response.text}")
        return response.json()


class Cursor:
    def __init__(self, transport: Transport):
        self.transport = transport
        self._results = []

    def execute(self, sql):
        self._results = self.transport.post_query(sql)

    def fetchall(self):
        return self._results

    def close(self):
        self._results = []


class Connection:
    def __init__(self, url, username, password):
        self.transport = HTTPTransport(url, username, password)

    def cursor(self):
        return Cursor(self.transport)

    def close(self):
        # if any cleanup needed later
        pass


def connect(url, username="admin", password="1234"):
    return Connection(url, username, password)
