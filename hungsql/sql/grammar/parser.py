from lark import Lark
from pathlib import Path

grammar_path = Path(__file__).resolve().parent / "sql_grammar.lark"

sql_parser = Lark.open(grammar_path, start="start", parser="lalr", maybe_placeholders=True)