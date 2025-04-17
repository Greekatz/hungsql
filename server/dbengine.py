import csv
import os
import re

def execute_query(sql):
    match = re.match(r"SELECT (.+) FROM (\w+)( WHERE (.+))?", sql.strip(), re.IGNORECASE)
    if not match:
        raise ValueError("Invalid SQL")

    select_columns = [col.strip() for col in match.group(1).split(",")]
    table = match.group(2)
    where = match.group(4)

    filepath = f"db/{table}.csv"
    print(filepath)
    if not os.path.exists(filepath):
        raise ValueError("Table not found")

    with open(filepath) as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if where:
        rows = apply_where(rows, where)

    result = [
        {col: row.get(col, None) for col in select_columns}
        for row in rows
    ]
    return {"rows": result}

def apply_where(rows, clause):
    conditions = [c.strip() for c in clause.split("AND")]

    def check(row):
        for condition in conditions:
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
