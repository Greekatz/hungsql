from hungsql.sql.grammar.parser import sql_parser
from hungsql.sql.transformer import SQLTransformer
from hungsql.sql.interpreter import SQLInterpreter

class Cursor:
    def __init__(self, tables: dict[str, list[dict]]):
        self.tables = tables
        self._results: list[tuple] = []
        self._description: list[tuple] = []
        self._index = 0

    @property
    def description(self):
        return self._description

    @property
    def rowcount(self):
        return len(self._results)

    def execute(self, sql: str):
        tree = sql_parser.parse(sql)
        ast = SQLTransformer().transform(tree)
        raw_rows = SQLInterpreter(self.tables).execute(ast)

        self._index = 0 

        if not raw_rows:
            self._results = []
            self._description = []
            return self

        columns = list(raw_rows[0].keys())
        self._results = [tuple(row[col] for col in columns) for row in raw_rows]
        self._description = [(col, None, None, None, None, None, None) for col in columns]

    def fetchmany(self, size=1000):
        result = self._results[self._index:self._index + size]
        self._index += len(result)
        return result

    def fetchall(self):
        result = self._results[self._index:]
        self._index = len(self._results)
        return result

    def fetchone(self):
        if self._index < len(self._results):
            row = self._results[self._index]
            self._index += 1
            return row
        return None

    def close(self):
        self._index = 0
        self._results = []
        self._description = []
