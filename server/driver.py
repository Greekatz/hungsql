import requests
import json
from abc import ABC, abstractmethod
import datetime

STRING = str
BINARY = bytes
NUMBER = float
DATETIME = datetime.datetime
ROWID = int


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
        self.arraysize = 1
        self.transport = transport
        self._results = []
        self._row_index = 1
        self._has_results = False
        self.description = None
        self.rowcount = -1

    def execute(self, sql, params=None):
        self._results = self.transport.post_query(sql)
        self._row_index = 1
        self._has_results = bool(self._results)

        if self._has_results:
            self.description = [
                (col, STRING, None, None, None, None, None)
                for col in self._results[0]
            ]

    def fetchone(self):
        if not self._has_results:
            raise Exception("No result set available. Did you forget to call .execute()?")

        if self._row_index >= len(self._results):
            return None

        row = self._results[self._row_index]
        self._row_index += 1
        return row

    def fetchall(self):
        if not self._has_results:
            raise Exception("No result set available.")
        return self._results[1:]  # skip header row

    def __iter__(self):
        return self

    def __next__(self):
        row = self.fetchone()
        if row is None:
            raise StopIteration
        return row

    next = __next__

    def close(self):
        self._results = []
        self._row_index = 0
        self._has_results = False
        self.description = None
        self.rowcount = -1

    


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


class TPCConnection:
    def __init__(self):
        pass
