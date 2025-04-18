import csv
import os
import re
from typing import List, Dict


class Table:
    def __init__(self, table_name: str, directory: str="db"):
        self.table_name = table_name
        self.filepath = os.path.join(directory, f"{self.table_name}.csv")
    
    def exists(self) -> bool:
        return os.path.exists(self.filepath)
    
    def load_data(self) -> List[Dict[str, str]]:
        if not self.exists():
            raise ValueError(f"Table '{self.table_name} not found")
        with open (self.filepath) as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def schema_inference(self) -> Dict[str, str]:
        rows = self.load_data()
        if not rows:
            return {}
        schema = {} 

        schema = {}
        sample_row = rows[0]
        for key, value in sample_row.items():
            if value.isdigit():
                schema[key] = "int"
            else:
                try:
                    float(value)
                    schema[key] = "float"
                except:
                    schema[key] = "str"
        return schema




class Condition:
    def __init__(self, condition_str: str, schema: Dict[str, str]):
        self.conditions = [c.strip() for c in condition_str.split("AND")]
        self.schema = schema

    def apply(self, rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
        def check(row):
            for condition in self.conditions:
                if ">" in condition:
                    k, v = map(str.strip, condition.split(">"))
                    if self.schema.get(k) in ("int", "float"):
                        if float(row[k]) <= float(v): return False
                    else:
                        raise ValueError(f"Cannot use '>' with string column '{k}'")

                elif "<" in condition:
                    k, v = map(str.strip, condition.split("<"))
                    if self.schema.get(k) in ("int", "float"):
                        if float(row[k]) >= float(v): return False
                    else:
                        raise ValueError(f"Cannot use '<' with string column '{k}'")

                elif "=" in condition:
                    k, v = map(str.strip, condition.split("="))
                    v = v.strip("'\"")
                    if self.schema.get(k) == "int" and not v.isdigit():
                        raise ValueError(f"Expected int for column '{k}' but got string")
                    if self.schema.get(k) == "str" and v.isdigit():
                        raise ValueError(f"Expected string for column '{k}' but got number")
                    if row[k] != v: return False
            return True
        return list(filter(check, rows))



class QueryParser:

    @staticmethod
    def parse(sql: str):
        match = re.match(r"SELECT (.+) FROM (\w+)( WHERE (.+))?", sql.strip(), re.IGNORECASE)
        if not match:
            raise ValueError("Invalid SQL")
        
        select_columns = [col.strip() for col in match.group(1).split(",")]
        table = match.group(2)
        where = match.group(4)
        return select_columns, table, where
    

class DatabaseEngine:
    def __init__(self, db_directory: str = "db"):
        self.db_directory = db_directory
    
    def execute_query(self, sql: str) -> List[List[str]]:
        select_columns, table_name, where_clause = QueryParser.parse(sql)
        table = Table(table_name, self.db_directory)
        rows = table.load_data()
        schema = table.schema_inference()

        if where_clause:
            condition = Condition(where_clause, schema)
            rows = condition.apply(rows)

        # Xác định danh sách cột
        if select_columns == ['*']:
            columns = list(rows[0].keys()) if rows else []
        else:
            columns = select_columns

        # Chuyển mỗi hàng thành list theo đúng thứ tự cột
        formatted_rows = [[row.get(col, "") for col in columns] for row in rows]

        # Trả về: dòng đầu là header + các dòng dữ liệu
        return [columns] + formatted_rows
            

        



