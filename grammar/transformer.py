from lark import Transformer

class SQLTransformer(Transformer):
    def select_query(self, items):
        select = items[0]
        from_ = items[1]
        where = items[2] if len(items) > 2 else None
        return {"select": select, "from": from_, "where": where}

    def selected_column(self, items):
        if len(items) == 1:
            return {"column": items[0]}
        elif len(items) == 2:
            if isinstance(items[0], str) and isinstance(items[1], str):
                return {"column": items[0], "alias": items[1]}
            return {"table": items[0], "column": items[1]}
        elif len(items) == 3:
            return {"table": items[0], "column": items[1], "alias": items[2]}

    def referred_table(self, items):
        if len(items) == 1:
            return {"table": items[0]}
        return {"table": items[0], "alias": items[1]}

    def STR(self, token):
        return token[1:-1]

    def INT(self, token):
        return int(token)

    def IDENTIFIER(self, token):
        return str(token)
