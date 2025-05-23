from lark import Transformer, Token


class SQLTransformer(Transformer):
    def start(self, items):
        return items[0]

    def select_statement(self, items):
        return {
            'type': 'select',
            'columns': items[0],
            'table': items[1],
            'where': items[2] if len(items) > 2 else None
        }

    def column_list(self, items):
        if isinstance(items[0], Token) and items[0].type == 'ASTERISK':
            return ['*']
        return [item for item in items if not isinstance(item, Token) or item.type != ',']

    def column_name(self, items):
        return items[0].value

    def table_name(self, items):
        return items[0].value

    def where_clause(self, items):
        return items[0]

    def condition(self, items):
        return items[0]

    def expression(self, items):
        return items[0]

    def and_expr(self, items):
        return {
            'op': 'AND',
            'left': items[0],
            'right': items[1]
        }

    def or_expr(self, items):
        return {
            'op': 'OR',
            'left': items[0],
            'right': items[1]
        }

    def comparison_expression(self, items):
        return {
            'left_operand': items[0],
            'op': items[1].value,
            'right_operand': items[2]
        }

    def is_null(self, items):
        return {
            'left_operand': items[0],
            'op': 'IS NULL'
        }

    def is_not_null(self, items):
        return {
            'left_operand': items[0],
            'op': 'IS NOT NULL'
        }

    def operand(self, items: list[Token]):
        token = items[0]
        if isinstance(token, Token):
            match token.type:
                case "SIGNED_NUMBER":
                    try:
                        return int(token.value)
                    except ValueError:
                        return float(token.value)
                case "CNAME"| "ESCAPED_STRING" | "SINGLE_QUOTED_STRING":
                    return token.value
                case "NULL":
                    return None
                case _:
                    raise ValueError(f"Unexpected token type: {type(token)}")
        else:
            raise ValueError(f"Expected Token, got {type(token)}")
