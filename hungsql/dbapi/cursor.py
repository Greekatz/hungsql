from hungsql.sql.grammar.parser import sql_parser
from hungsql.sql.transformer import SQLTransformer
from hungsql.sql.interpreter import SQLInterpreter

class Cursor:
    def __init__(self, tables: dict[str, list[dict]]):
        self.tables = tables
        self._results: list[tuple] = []
        self._description: list[tuple] = []
        self._position = 0  # for pagination tracking

    @property
    def description(self):
        return self._description

    @property
    def rowcount(self):
        return len(self._results)

    def execute(self, sql: str):
        tree = sql_parser.parse(sql)
        ast = SQLTransformer().transform(tree)
        query = SQLInterpreter(self.tables).execute(ast)

        if not query:
            self._results = []
            self._description = []
            return

        columns = list(query[0].keys())
        self._results = [tuple(row[col] for col in columns) for row in query]
        self._description = [(col, None, None, None, None, None, None) for col in columns]
        self._position = 0  # reset pagination

    def fetchmany(self, size=1000):
        chunk = self._results[self._position:self._position + size]
        self._position += len(chunk)
        return chunk

    def fetchone(self):
        if self._position < len(self._results):
            row = self._results[self._position]
            self._position += 1
            return row
        return None
    
    def fetchall(self):
        return self._results


    def close(self):
        self._results = []
        self._description = []
        self._position = 0
