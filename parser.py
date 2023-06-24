from enum import Enum
from lexer import Lexer, Token

class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def insert(self, name, symbol_type):
        self.symbols[name] = symbol_type

    def lookup(self, name):
        return self.symbols.get(name, None)

class NodeType(Enum):
    PROGRAM = 1
    STATEMENT_LIST = 2
    ASSIGNMENT_STATEMENT = 3
    VAR_STATEMENT = 4
    FUNCTION_DECLARATION = 5
    FUNCTION_CALL = 6
    PROCEDURE_DECLARATION = 7
    PROCEDURE_CALL = 8
    IF_STATEMENT = 9
    ELSE_STATEMENT = 10
    WHILE_STATEMENT = 11
    FOR_STATEMENT = 12
    EXPRESSION_STATEMENT = 13
    EXPRESSION = 14
    TERM = 15
    FACTOR = 16
    RELATIONAL_OPERATOR = 17
    ADDITIVE_OPERATOR = 18
    MULTIPLICATIVE_OPERATOR = 19
    PARAM_LIST = 20
    ARGUMENT_LIST = 21
    IDENTIFIER = 22
    NUMBER = 23
    INTEGER = 24
    REAL = 25
    STRING = 26
    BOOLEAN = 27
    CHAR = 28
    ARRAY = 29
    BOUNDS = 30
    TYPES = 31
    BEGIN = 32

class Node:
    def __init__(self, node_type, value=None, children=None):
        self.node_type = node_type
        self.value = value
        self.children = children if children else []

    def add_child(self, child):
        self.children.append(child)

    def __repr__(self):
        return f"Node: Type={self.node_type}, Value={self.value}, Children={self.children}"

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()
        self.symbol_table = SymbolTable()  # Создаем таблицу символов

    def parse(self):
        return self.parse_program()

    def match(self, expected_type):
        if self.current_token.type == expected_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error(f"Unexpected token: {self.current_token}")

    def error(self, message):
        raise Exception(f"Parser error: {message}")

    def parse_program(self):
        statement_list = self.parse_statement_list()
        return Node(NodeType.PROGRAM, children=[statement_list])

    def parse_statement_list(self):
        statement = self.parse_statement()
        if self.current_token.type != Lexer.EOF:
            statement_list = self.parse_statement_list()
            statement.add_child(statement_list)
        return statement

    def parse_statement(self):
        if self.current_token.type == Lexer.IDENTIFIER:
            return self.parse_assignment_statement()
        elif self.current_token.type == Lexer.VAR:
            return self.parse_var_statement()
        elif self.current_token.type == Lexer.FUNCTION:
            return self.parse_function_declaration()
        elif self.current_token.type == Lexer.PROCEDURE:
            return self.parse_procedure_declaration()
        elif self.current_token.type == Lexer.IF:
            return self.parse_if_statement()
        elif self.current_token.type == Lexer.WHILE:
            return self.parse_while_statement()
        elif self.current_token.type == Lexer.FOR:
            return self.parse_for_statement()
        else:
            return self.parse_expression_statement()

    def parse_assignment_statement(self):
        identifier = self.parse_identifier()
        self.match(Lexer.ASSIGN)
        expression = self.parse_expression()
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.ASSIGNMENT_STATEMENT, children=[identifier, expression])

    def parse_var_statement(self):
        self.match(Lexer.VAR)
        identifier = self.parse_identifier()
        self.match(Lexer.COLON)
        type_node = self.parse_types()
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.VAR_STATEMENT, children=[identifier, type_node])

    def parse_expression_statement(self):
        expression = self.parse_expression()
        return Node(NodeType.EXPRESSION_STATEMENT, children=[expression])

    def parse_function_declaration(self):
        self.match(Lexer.FUNCTION)
        identifier = self.parse_identifier()
        self.match(Lexer.LPAREN)
        param_list = self.parse_param_list()
        self.match(Lexer.RPAREN)
        self.match(Lexer.COLON)
        type_node = self.parse_types()
        self.match(Lexer.SEMICOLON)
        self.match(Lexer.BEGIN)
        statement_list = self.parse_statement_list()
        self.match(Lexer.END)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.FUNCTION_DECLARATION, value=identifier, children=[param_list, type_node, statement_list])

    def parse_param_list(self):
        if self.current_token.type == Lexer.RPAREN:
            return None
        identifier = self.parse_identifier()
        self.match(Lexer.COLON)
        type_node = self.parse_types()
        if self.current_token.type == Lexer.SEMICOLON:
            self.match(Lexer.SEMICOLON)
            param_list = self.parse_param_list()
            param_list.add_child(Node(NodeType.IDENTIFIER, value=identifier))
            param_list.add_child(type_node)
            return param_list
        return Node(NodeType.PARAM_LIST, children=[Node(NodeType.IDENTIFIER, value=identifier), type_node])

    def parse_procedure_declaration(self):
        self.match(Lexer.PROCEDURE)
        identifier = self.parse_identifier()
        self.match(Lexer.LPAREN)
        param_list = self.parse_param_list()
        self.match(Lexer.RPAREN)
        self.match(Lexer.SEMICOLON)
        self.match(Lexer.BEGIN)
        statement_list = self.parse_statement_list()
        self.match(Lexer.END)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.PROCEDURE_DECLARATION, value=identifier, children=[param_list, statement_list])

    def parse_if_statement(self):
        self.match(Lexer.IF)
        expression = self.parse_expression()
        self.match(Lexer.THEN)
        self.match(Lexer.BEGIN)
        statement_list = self.parse_statement_list()
        if self.current_token.type == Lexer.ELSE:
            self.match(Lexer.ELSE)
            else_statement = self.parse_else_statement()
            return Node(NodeType.IF_STATEMENT, children=[expression, statement_list, else_statement])
        self.match(Lexer.END)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.IF_STATEMENT, children=[expression, statement_list])

    def parse_else_statement(self):
        self.match(Lexer.BEGIN)
        statement_list = self.parse_statement_list()
        self.match(Lexer.END)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.ELSE_STATEMENT, children=[statement_list])

    def parse_while_statement(self):
        self.match(Lexer.WHILE)
        expression = self.parse_expression()
        self.match(Lexer.DO)
        self.match(Lexer.BEGIN)
        statement_list = self.parse_statement_list()
        self.match(Lexer.END)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.WHILE_STATEMENT, children=[expression, statement_list])

    def parse_for_statement(self):
        self.match(Lexer.FOR)
        identifier = self.parse_identifier()
        self.match(Lexer.ASSIGN)
        expression1 = self.parse_expression()
        if self.current_token.type == Lexer.TO:
            self.match(Lexer.TO)
        else:
            self.match(Lexer.DOT)
            self.match(Lexer.DOT)
            #self.match(Lexer.TO)
        expression2 = self.parse_expression()
        self.match(Lexer.DO)
        self.match(Lexer.BEGIN)
        statement_list = self.parse_statement_list()
        self.match(Lexer.END)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.FOR_STATEMENT, value=identifier, children=[expression1, expression2, statement_list])

    def parse_repeat_statement(self):
        self.match(Lexer.REPEAT)
        statement_list = self.parse_statement_list()
        self.match(Lexer.UNTIL)
        expression = self.parse_expression()
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.REPEAT_STATEMENT, children=[statement_list, expression])

    def parse_write_statement(self):
        self.match(Lexer.WRITE)
        self.match(Lexer.LPAREN)
        expression = self.parse_expression()
        self.match(Lexer.RPAREN)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.WRITE_STATEMENT, children=[expression])

    def parse_read_statement(self):
        self.match(Lexer.READ)
        self.match(Lexer.LPAREN)
        identifier = self.parse_identifier()
        self.match(Lexer.RPAREN)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.READ_STATEMENT, children=[identifier])

    def parse_writeln_statement(self):
        self.match(Lexer.WRITELN)
        self.match(Lexer.LPAREN)
        expression = self.parse_expression()
        self.match(Lexer.RPAREN)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.WRITELN_STATEMENT, children=[expression])

    def parse_readln_statement(self):
        self.match(Lexer.READLN)
        self.match(Lexer.LPAREN)
        identifier = self.parse_identifier()
        self.match(Lexer.RPAREN)
        self.match(Lexer.SEMICOLON)
        return Node(NodeType.READLN_STATEMENT, children=[identifier])

    def parse_expression(self):
        term = self.parse_term()
        if self.current_token.type == Lexer.PLUS:
            self.match(Lexer.PLUS)
            return Node(NodeType.ADDITION, children=[term, self.parse_expression()])
        elif self.current_token.type == Lexer.MINUS:
            self.match(Lexer.MINUS)
            return Node(NodeType.SUBTRACTION, children=[term, self.parse_expression()])
        return term

    def parse_term(self):
        factor = self.parse_factor()
        if self.current_token.type == Lexer.MULTIPLY:
            self.match(Lexer.MULTIPLY)
            return Node(NodeType.MULTIPLICATION, children=[factor, self.parse_term()])
        elif self.current_token.type == Lexer.DIVIDE:
            self.match(Lexer.DIVIDE)
            return Node(NodeType.DIVISION, children=[factor, self.parse_term()])
        return factor

    def parse_factor(self):
        """
        factor : INTEGER
               | REAL
               | STRING
               | TRUE
               | FALSE
               | LPAREN expr RPAREN
               | variable
               | function_call
        """
        token = self.current_token

        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token.value)
        elif token.type == TokenType.REAL:
            self.eat(TokenType.REAL)
            return Num(token.value)
        elif token.type == TokenType.STRING:
            self.eat(TokenType.STRING)
            return String(token.value)
        elif token.type == TokenType.TRUE:
            self.eat(TokenType.TRUE)
            return Boolean(True)
        elif token.type == TokenType.FALSE:
            self.eat(TokenType.FALSE)
            return Boolean(False)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.parse_expression()
            self.eat(TokenType.RPAREN)
            return node
        elif self.current_token.type == TokenType.IDENTIFIER:
            return self.parse_variable()
        elif self.current_token.type == TokenType.IDENTIFIER_LPAREN:
            return self.parse_function_call()

    def parse_function_call(self, identifier):
        self.match(Lexer.LPAREN)
        argument_list = self.parse_argument_list()
        self.match(Lexer.RPAREN)
        return Node(NodeType.FUNCTION_CALL, value=identifier, children=[argument_list])

    def parse_argument_list(self):
        if self.current_token.type == Lexer.RPAREN:
            return None
        expression = self.parse_expression()
        if self.current_token.type == Lexer.COMMA:
            self.match(Lexer.COMMA)
            argument_list = self.parse_argument_list()
            argument_list.add_child(expression)
            return argument_list
        return Node(NodeType.ARGUMENT_LIST, children=[expression])

    def parse_identifier(self):
        identifier = Node(NodeType.IDENTIFIER, value=self.current_token.value)
        self.match(Lexer.IDENTIFIER)
        return identifier

    def parse_types(self):
        if self.current_token.type == Lexer.ARRAY:
            return self.parse_array()
        return self.parse_type()

    def parse_type(self):
        if self.current_token.type == Lexer.INTEGER:
            type_node = Node(NodeType.INTEGER)
            self.match(Lexer.INTEGER)
            return type_node
        elif self.current_token.type == Lexer.REAL:
            type_node = Node(NodeType.REAL)
            self.match(Lexer.REAL)
            return type_node
        elif self.current_token.type == Lexer.STRING:
            type_node = Node(NodeType.STRING)
            self.match(Lexer.STRING)
            return type_node
        elif self.current_token.type == Lexer.BOOLEAN:
            type_node = Node(NodeType.BOOLEAN)
            self.match(Lexer.BOOLEAN)
            return type_node
        elif self.current_token.type == Lexer.CHAR:
            type_node = Node(NodeType.CHAR)
            self.match(Lexer.CHAR)
            return type_node

    def parse_array(self):
        self.match(Lexer.ARRAY)
        bounds = self.parse_bounds()
        self.match(Lexer.OF)
        type_node = self.parse_type()
        return Node(NodeType.ARRAY, children=[bounds, type_node])

    def parse_bounds(self):
        self.match(Lexer.LBRACKET)
        bound1 = self.parse_bound()
        self.match(Lexer.DOT)
        self.match(Lexer.DOT)
        bound2 = self.parse_bound()
        self.match(Lexer.RBRACKET)
        return Node(NodeType.BOUNDS, children=[bound1, bound2])

    def parse_bound(self):
        if self.current_token.type == Lexer.INTEGER:
            node = Node(NodeType.INTEGER, value=self.current_token.value)
            self.match(Lexer.INTEGER)
            return node
        elif self.current_token.type == Lexer.IDENTIFIER:
            return self.parse_identifier()
