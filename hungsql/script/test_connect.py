
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from hungsql.dbapi import connect


def main():
    conn = connect(dsn="schema1", user="user231@example.com", password="SecurePass123123")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE 1 = 1;")
    print(cursor.fetchone())
    print(cursor.fetchone())
    cursor.close()
if __name__ == "__main__":
    main()
