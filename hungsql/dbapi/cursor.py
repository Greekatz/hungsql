from hungsql.sql.grammar.parser import sql_parser
from hungsql.sql.transformer import SQLTransformer
from hungsql.sql.interpreter import SQLInterpreter

class Cursor:
    def __init__(self, tables: dict[str, list[dict]]):
        self.tables = tables
        self._results: list[tuple] = []
        self._description: list[tuple] = []

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


        columns = list(query[0].keys())
        self._results = [tuple(row[col] for col in columns) for row in query]
        self._description = [(col, None, None, None, None, None, None) for col in columns]

    def fetchmany(self, size=1000):
        return self._results[:size]

    def fetchall(self):
        return self._results

    def fetchone(self):
        return self._results[0] if self._results else None

    def close(self):
        self._results = []
        self._description = []
