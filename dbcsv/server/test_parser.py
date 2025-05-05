import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parents[2]))

from lark import Lark
from dbcsv.server.sql.transformer import SQLTransformer

with open ('./hungsql/sql/grammar/sql_grammar.lark', 'r') as f:
    sql_grammar = f.read()
# Create the parser
parser = Lark(sql_grammar, start="start", parser="lalr")

# Example usage
if __name__ == "__main__":
    test_queries = [
    # Valid queries
    "select * from users;",
    "select id,name from users where id = 1;",
    "select id, name from users where age < 30  and name = 'Alice';",
    "select id, name from users where join_date >= '2023-01-01';",
    "select name, name from users where '1' = 1;",
    "select name, name from users where 1 = 1;",

    # Invalid queries (should raise an error)
    "select * from where id = 1;",  # Missing table name
    "select id, name from users where id =;",  # Missing value
    "select id, name users where id = 1;",  # Missing FROM
    ]


    for query in test_queries:
        print(f"\nParsing: {query}")
        try:
            result = parser.parse(query)
            transformer = SQLTransformer()
            ast = transformer.transform(result)
            print("Result:")
            import pprint
            pprint.pprint(ast, indent=2)
        except Exception as e:
            print(f"Error: {e}") 