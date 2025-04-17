import csv
import os
import re
from typing import List, Dict

# def execute_query(sql):
#     match = re.match(r"SELECT (.+) FROM (\w+)( WHERE (.+))?", sql.strip(), re.IGNORECASE)
#     if not match:
#         raise ValueError("Invalid SQL")

#     select_columns = [col.strip() for col in match.group(1).split(",")]
#     table = match.group(2)
#     where = match.group(4)

#     filepath = f"db/{table}.csv"
#     print(filepath)
#     if not os.path.exists(filepath):
#         raise ValueError("Table not found")

#     with open(filepath) as f:
#         reader = csv.DictReader(f)
#         rows = list(reader)

#     if where:
#         rows = apply_where(rows, where)

#     result = [
#         {col: row.get(col, None) for col in select_columns}
#         for row in rows
#     ]
#     return {"rows": result}

# def apply_where(rows, clause):
#     conditions = [c.strip() for c in clause.split("AND")]

#     def check(row):
#         for condition in conditions:
#             if ">" in condition:
#                 k, v = map(str.strip, condition.split(">"))
#                 if float(row[k]) <= float(v): return False
#             elif "<" in condition:
#                 k, v = map(str.strip, condition.split("<"))
#                 if float(row[k]) >= float(v): return False
#             elif "=" in condition:
#                 k, v = map(str.strip, condition.split("="))
#                 v = v.strip("'\"")
#                 if row[k] != v: return False
#         return True

#     return list(filter(check, rows))

class Table:
    def __init__(self, table_name: str, directory: str="db"):
        self.table_name = table_name
        self.filepath = os.path.join(directory, f"{self.table_name}.csv")
    
    def exists(self) -> bool:
        return os.path.exists(self.filepath)
    
    def load_data(self) -> List[Dict[str, str]]:
        if not self.exists():
            raise ValueError(f"Table '{self.table_name} npt found")
        with open (self.filepath) as f:
            reader = csv.DictReader(f)
            return list(reader)


class Condition:
    def __init__(self, condition_str: str):
        self.conditions = [c.strip() for c in condition_str.split("AND")]
    
    def apply(self, rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
        def check(row):
            for condition in self.conditions:
                if ">" in condition:
                    k, v = map(str.strip, condition.split(">"))
                    if float(row[k]) <= float(v): return False
                elif "<" in condition:
                    k, v = map(str.strip, condition.split("<"))
                    if float(row[k]) >= float(v): return False
                elif "=" in condition:
                    k, v = map(str.strip, condition.split("="))
                    v = v.strip("'\"")
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
    
    def execute_query(self, sql: str) -> Dict:
        select_columns, table_name, where_clause = QueryParser.parse(sql)
        table = Table(table_name, self.db_directory)

        rows = table.load_data()

        if where_clause:
            condition = Condition(where_clause)
            rows = condition.apply(rows)

        if select_columns == ['*']:
            result = rows
        
        else: 
            result = [
                {col: row.get(col, None) for col in select_columns}
                for row in rows
            ]

        return {"rows": result}



