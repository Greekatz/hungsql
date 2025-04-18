import csv
import os
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple, Union, Pattern

@dataclass
class TableSchema:
    name: str
    columns: Dict[str, str]  # column_name -> type ("int", "float", "str")

class Table:
    def __init__(self, table_name: str, directory: str = "db"):
        self.name = table_name
        self.filepath = os.path.join(directory, f"{self.name}.csv")
        self._validate_filepath()
    
    def _validate_filepath(self) -> None:
        """Ensure the file path is safe and within the designated directory"""
        if not os.path.abspath(self.filepath).startswith(os.path.abspath(os.path.dirname(self.filepath))):
            raise ValueError("Invalid file path")
    
    def exists(self) -> bool:
        return os.path.exists(self.filepath)
    
    def load_data(self) -> List[Dict[str, str]]:
        """Load table data with proper error handling"""
        if not self.exists():
            raise FileNotFoundError(f"Table '{self.name}' not found at {self.filepath}")
        
        try:
            with open(self.filepath, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except (csv.Error, IOError) as e:
            raise RuntimeError(f"Failed to load table data: {str(e)}")
    
    def infer_schema(self) -> TableSchema:
        """Infer schema with type validation"""
        rows = self.load_data()
        if not rows:
            return TableSchema(self.name, {})
        
        schema = {}
        sample_row = rows[0]
        
        for column, value in sample_row.items():
            if value.isdigit():
                schema[column] = "int"
            else:
                try:
                    float(value)
                    schema[column] = "float"
                except ValueError:
                    schema[column] = "str"
        
        return TableSchema(self.name, schema)

class QueryCondition:
    OPERATOR_PATTERN: Pattern = re.compile(r'(>=|<=|!=|>|<|=)')
    
    def __init__(self, condition_str: str, schema: TableSchema):
        self.conditions = self._parse_conditions(condition_str)
        self.schema = schema
    
    def _parse_conditions(self, condition_str: str) -> List[Tuple[str, str, str]]:
        """Parse conditions into (column, operator, value) tuples"""
        if not condition_str:
            return []
        
        conditions = []
        for clause in condition_str.split("AND"):
            clause = clause.strip()
            if not clause:
                continue
                
            match = self.OPERATOR_PATTERN.search(clause)
            if not match:
                raise ValueError(f"Invalid condition format: {clause}")
            
            operator = match.group()
            col, val = clause.split(operator, 1)
            conditions.append((col.strip(), operator, val.strip().strip('"\'')))
        
        return conditions
    
    def apply(self, rows: List[Dict[str, str]]) -> List[Dict[str, str]]:
        """Filter rows based on conditions"""
        return [row for row in rows if self._row_matches_conditions(row)]
    
    def _row_matches_conditions(self, row: Dict[str, str]) -> bool:
        """Check if a single row matches all conditions"""
        for column, operator, value in self.conditions:
            if not self._check_condition(row, column, operator, value):
                return False
        return True
    
    def _check_condition(self, row: Dict[str, str], 
                        column: str, 
                        operator: str, 
                        value: str) -> bool:
        """Validate and evaluate a single condition"""
        if column not in row:
            raise ValueError(f"Column '{column}' not found in table")
        
        column_type = self.schema.columns.get(column, "str")
        row_value = row[column]
        
        try:
            if operator == "=":
                return self._compare_equal(row_value, value, column_type)
            
            # Numeric comparisons
            if column_type not in ("int", "float"):
                raise ValueError(f"Cannot use operator '{operator}' with non-numeric column '{column}'")
            
            row_num = float(row_value) if column_type == "float" else int(row_value)
            val_num = float(value) if column_type == "float" else int(value)
            
            return {
                ">": row_num > val_num,
                "<": row_num < val_num,
                ">=": row_num >= val_num,
                "<=": row_num <= val_num,
                "!=": row_num != val_num,
            }.get(operator, False)
            
        except (ValueError, TypeError) as e:
            raise ValueError(f"Type mismatch in condition {column}{operator}{value}: {str(e)}")

    def _compare_equal(self, row_value: str, condition_value: str, column_type: str) -> bool:
        """Special handling for equality comparisons with type checking"""
        if column_type == "int":
            return int(row_value) == int(condition_value)
        elif column_type == "float":
            return float(row_value) == float(condition_value)
        return row_value == condition_value

class QueryParser:
    SQL_PATTERN: Pattern = re.compile(
        r"SELECT\s+(.+?)\s+FROM\s+(\w+)(?:\s+WHERE\s+(.+))?$", 
        re.IGNORECASE
    )
    
    @classmethod
    def parse(cls, sql: str) -> Tuple[List[str], str, Optional[str]]:
        """Parse SQL query into components with validation"""
        match = cls.SQL_PATTERN.match(sql.strip())
        if not match:
            raise ValueError("Invalid SQL query format")
        
        columns = [col.strip() for col in match.group(1).split(",")]
        table = match.group(2)
        where_clause = match.group(3)
        
        return columns, table, where_clause

class DatabaseEngine:
    def __init__(self, db_directory: str = "db"):
        self.db_directory = db_directory
        os.makedirs(db_directory, exist_ok=True)
    
    def execute_query(self, sql: str) -> List[List[str]]:
        """Execute SQL query and return results with header row"""
        columns, table_name, where_clause = QueryParser.parse(sql)
        table = Table(table_name, self.db_directory)
        
        try:
            rows = table.load_data()
            schema = table.infer_schema()
            
            if where_clause:
                condition = QueryCondition(where_clause, schema)
                rows = condition.apply(rows)
            
            result_columns = self._determine_output_columns(columns, rows)
            return self._format_results(result_columns, rows)
            
        except Exception as e:
            raise RuntimeError(f"Query execution failed: {str(e)}")
    
    def _determine_output_columns(self, 
                                requested_columns: List[str], 
                                rows: List[Dict[str, str]]) -> List[str]:
        """Determine which columns to include in results"""
        if not rows:
            return [] if '*' in requested_columns else requested_columns
        
        if requested_columns == ['*']:
            return list(rows[0].keys())
        
        # Validate requested columns exist
        available_columns = set(rows[0].keys()) if rows else set()
        for col in requested_columns:
            if col not in available_columns:
                raise ValueError(f"Column '{col}' not found in table")
        
        return requested_columns
    
    def _format_results(self, 
                       columns: List[str], 
                       rows: List[Dict[str, str]]) -> List[List[str]]:
        """Format results as list of lists with header row"""
        if not columns:
            return []
        
        formatted_rows = [[row.get(col, "") for col in columns] for row in rows]
        return [columns] + formatted_rows