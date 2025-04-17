import pytest
import os
import csv
from server.dbengine import DatabaseEngine


TEST_CSV_PATH = "db/users.csv"

@pytest.fixture(scope="module", autouse=True)
def setup_csv():
    os.makedirs("db", exist_ok=True)
    with open(TEST_CSV_PATH, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["name", "age"])
        writer.writeheader()
        writer.writerows([
            {"name": "Alice", "age": "30"},
            {"name": "Bob", "age": "25"}
        ])
    yield
    os.remove(TEST_CSV_PATH)

def test_select_all():
    engine = DatabaseEngine()
    result = engine.execute_query("SELECT * FROM users")
    assert result["rows"]

def test_select_columns():
    engine = DatabaseEngine()
    result = engine.execute_query("SELECT name, age FROM users")
    assert result["rows"] == [
        {"name": "Alice", "age": "30"},
        {"name": "Bob", "age": "25"}
    ]