from lark import Lark
from grammar.Transformer import SQLTransformer

# Load your grammar from file
with open("./grammar/sql_grammar.lark", "r") as f:
    grammar = f.read()

# Initialize the parser
parser = Lark(grammar, start="start", parser="lalr", transformer=SQLTransformer())

# Test cases
test_queries = [
    # Valid queries
    "select * from users;",
    "select id,name from users where id = 1;",
    "select u.id, u.name from users as u where u.age > 25 and u.status is not null;",
    "select id, name from users where (age < 30 or salary > 50000) and name = 'Alice';",
    "select id, name from users where join_date >= '2023-01-01';",
    
    # Invalid queries (should raise an error)
    "select * from where id = 1;",  # Missing table name
    "select id, name from users where id =;",  # Missing value
    "select id, name users where id = 1;",  # Missing FROM
]

# Test each query
for query in test_queries:
    print(f"\nTesting query: {query}")
    try:
        tree = parser.parse(query)
        print("✅ Parsed successfully!")
        print(tree.pretty())  # Print the parse tree
    except Exception as e:
        print(f"❌ Failed to parse: {e}")