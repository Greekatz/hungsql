class SQLInterpreter:
    def __init__(self, tables: dict[str, list[dict]]):
        self.tables = tables  

    def execute(self, ast: dict) -> list[dict]:
        if ast["type"] == "select":
            table = self.tables.get(ast["table"])
            if table is None:
                raise ValueError(f"Table '{ast['table']}' not found")

        # Apply WHERE
        filtered = (
            [row for row in table if self._evaluate_condition(row, ast["where"])]
            if ast["where"]
            else table
        )

        # Select columns
        if ast["columns"] == ["*"]:
            return filtered
        else:
            return [
                {col: row[col] for col in ast["columns"] if col in row}
                for row in filtered
            ]
        
    def _normalize_type(self, left, right):
        """Coerce left (from CSV) to type of right (from query)."""
        if isinstance(right, int):
            try:
                return int(left)
            except (ValueError, TypeError):
                return left
        if isinstance(right, float):
            try:
                return float(left)
            except (ValueError, TypeError):
                return left
        return left

    def _evaluate_condition(self, row: dict, cond: dict) -> bool:
        if "op" not in cond:
            return True

        op = cond["op"]
        left_raw = cond["left_operand"]
        right_raw = cond.get("right_operand")

        # Handle left side
        if isinstance(left_raw, str) and left_raw in row:
            left = row[left_raw]
        elif isinstance(left_raw, str) and left_raw.isdigit():
            left = int(left_raw)
        else:
            left = left_raw

        # Handle right side
        if isinstance(right_raw, str) and right_raw in row:
            right = row[right_raw]
        elif isinstance(right_raw, str) and right_raw.isdigit():
            right = int(right_raw)
        else:
            right = right_raw

        match op:
            case "=": return left == right
            case "!=": return left != right
            case ">": return left > right
            case "<": return left < right
            case ">=": return left >= right
            case "<=": return left <= right
            case "IS NULL": return left is None
            case "IS NOT NULL": return left is not None
