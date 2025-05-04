import csv
from pathlib import Path
from typing import Dict, List, Optional

from hungsql.dbapi.cursor import Cursor
from hungsql.dbapi.exceptions import NotSupportedError

class Connection:
    def __init__(self, user_email: str, token: Optional[str] = None, dsn: str = "schema1"):
        self.user_email = user_email
        self.token = token
        self.schema = dsn
        self.tables: Dict[str, List[dict]] = self._load_tables()

    def _load_tables(self) -> Dict[str, List[dict]]:
        base_path = Path(__file__).resolve().parents[2] / "db" / self.schema
        if not base_path.exists():
            raise FileNotFoundError(f"Schema folder '{self.schema}' not found at: {base_path}")

        tables = {}

        for table_dir in base_path.iterdir():
            if table_dir.is_dir():
                csv_file = table_dir / f"{table_dir.name}.csv"
                if csv_file.exists():
                    try:
                        with open(csv_file, newline="", encoding="utf-8") as f:
                            reader = csv.DictReader(f)
                            tables[table_dir.name] = list(reader)
                    except Exception as e:
                        print(f"[WARN] Failed to load table '{table_dir.name}': {e}")
                else:
                    print(f"[WARN] Expected file '{csv_file.name}' not found in folder '{table_dir.name}'")

        return tables

    def cursor(self) -> Cursor:
        return Cursor(self.tables)
    
    def rollback(self):
        raise NotSupportedError("rollback() is currently not supported")

    