
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from dbcsv.client.dbapi2 import connect


def main():
    conn = connect(dsn="schema1", username="user@example.com", password="User12345pass")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE 1 = 1;")
    print(cursor.fetchone())
    print(cursor.fetchone())
    cursor.close()
if __name__ == "__main__":
    main()
