from AST import *
from lexer import Lexer


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = SymbolTable()

    # ... existing methods ...

    def program(self):
        return ProgramNode(self.statement_list(), self.symbol_table)

    def var_statement(self):
        self.eat(Lexer.VAR)
        identifier = self.current_token.value
        self.eat(Lexer.IDENTIFIER)
        self.eat(Lexer.COLON)
        types = self.types()
        self.eat(Lexer.SEMICOLON)

        # Add the variable to the symbol table
        self.symbol_table.add_symbol(identifier, types)

        return VarStatementNode(identifier, types)

    def function_declaration(self):
        self.eat(Lexer.FUNCTION)
        identifier = self.current_token.value
        self.eat(Lexer.IDENTIFIER)
        self.eat(Lexer.LPAREN)
        param_list = self.param_list()
        self.eat(Lexer.RPAREN)
        self.eat(Lexer.COLON)
        types = self.types()
        self.eat(Lexer.SEMICOLON)
        self.eat(Lexer.BEGIN)

        # Create a new symbol table for the function
        function_symbol_table = SymbolTable()

        # Add function parameters to the symbol table
        for param in param_list:
            function_symbol_table.add_symbol(param['identifier'], param['types'])

        statement_list = self.statement_list()

        # Merge the function's symbol table with the global symbol table
        self.symbol_table.symbols.update(function_symbol_table.symbols)

        self.eat(Lexer.END)
        self.eat(Lexer.SEMICOLON)

        return FunctionDeclarationNode(identifier, param_list, types, statement_list, function_symbol_table)
