import pytest
from dbcsv.sql.grammar.parser import sql_parser
from dbcsv.sql.transformer import SQLTransformer
from lark.exceptions import LarkError

@pytest.mark.parametrize("sql", [
    "select * from users;",
    "select id, name from users where 1 = 1;",
    "select id from users where age > 18 and name = 'Alice';",
])
def test_valid_queries(sql):
    tree = sql_parser.parse(sql)
    ast = SQLTransformer().transform(tree)
    assert isinstance(ast, dict)

@pytest.mark.parametrize("sql", [
    "select from users;",
    "select id, name users where id = 1;",
])
def test_invalid_queries(sql):
    with pytest.raises(LarkError):
        sql_parser.parse(sql)
