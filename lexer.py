import sys


class Token:
    def __init__(self, row, col, type, value):
        self.row, self.col, self.type, self.value = row, col, type, value

    def __repr__(self):
        return f"Token: \tType: {Lexer.PRESENTATION[self.type]} \tValue: <{self.value}>"

    def __str__(self):
        return f"-{Lexer.PRESENTATION[self.type]}\t'{self.value}'"


class Lexer:
    def __init__(self, input_string):
        self.input_string = input_string
        self.input_length = len(input_string)
        self.current_pos = 0
        self.current_char = None
        self.row, self.col = 1, 0

    PROGRAM, VAR, BEGIN, INTEGER, REAL, \
        BOOLEAN, CHAR, STRING, IF, THEN, ELSE, \
        WHILE, DO, REPEAT, UNTIL, WRITE, READ, \
        WRITELN, READLN, FUNCTION, PROCEDURE, \
        NOT, IDENTIFIER, FOR, LPAREN, RPAREN, \
        TRUE, FALSE, RBR, LBR, LESS, GREATER, \
        TAB, DOT, COMMA, COLON, SEMICOLON, \
        SINGLE_QUOTE, DOUBLE_QUOTE, \
        PLUS, MINUS, MULTIPLY, ASSIGN, DIVIDE, END, EOF, \
        AND, NOT, IN, NEWLINE, RESULT, EQUAL, ARRAY, TO, \
        OF, LE, GE, SLASH, NOTEQ, ARRDOT, NUMBER, COMMENT = range(62)

    PRESENTATION = {
        PROGRAM: "program",
        VAR: "var",
        BEGIN: "begin",
        INTEGER: "integer",
        REAL: "real",
        BOOLEAN: "boolean",
        ARRAY: "array",
        CHAR: "char",
        STRING: "string",
        IF: "if",
        THEN: "then",
        ELSE: "else",
        EQUAL: "equal",
        WHILE: "while",
        DO: "do",
        REPEAT: "repeat",
        UNTIL: "until",
        FUNCTION: "function",
        PROCEDURE: "procedure",
        NOT: "not",
        WRITE: "write",
        READ: "read",
        TO: "to",
        ARRDOT: "doubleDot",
        WRITELN: "writeln",
        NUMBER: "number",
        READLN: "readln",
        FOR: "for",
        LPAREN: "lparen",
        RPAREN: "rparen",
        TRUE: "true",
        FALSE: "false",
        RBR: "rbr",
        LBR: "lbr",
        LESS: "less",
        GREATER: "greater",
        TAB: "tab",
        DOT: "dot",
        COMMA: "comma",
        COLON: "colon",
        SEMICOLON: "semicolon",
        SINGLE_QUOTE: "singleQuote",
        DOUBLE_QUOTE: "doubleQuote",
        PLUS: "plus",
        MINUS: "minus",
        MULTIPLY: "multiply",
        ASSIGN: "assign",
        DIVIDE: "divide",
        END: "end",
        EOF: "eof",
        AND: "and",
        NOT: "not",
        IN: "in",
        NEWLINE: "newline",
        RESULT: "result",
        LE: "le",
        GE: "ge",
        SLASH: "slash",
        NOTEQ: "noteq",
        COMMENT: "comment",
        IDENTIFIER: "identifier"
    }

    KEYWORDS = {
        'if': IF,
        'else': ELSE,
        'while': WHILE,
        'for': FOR,
        'do': DO,
        'function': FUNCTION,
        'procedure': PROCEDURE,
        'array': ARRAY,
        'repeat': REPEAT,
        'and': AND,
        'in': IN,
        'end': END,
        'then': THEN,
        'begin': BEGIN,
        'var': VAR,
        'program': PROGRAM
    }

    RESERVED_NAMES = {
        'write': WRITE,
        'read': READ,
        'writeln': WRITELN,
        'readln': READLN,
        'true': TRUE,
        'to': TO,
        'false': FALSE,
        'until': UNTIL,
        'of': OF
    }

    n_tabs = 4
    SYMBOLS = {
        ':=': ASSIGN,
        '=': EQUAL,
        '+': PLUS,
        '-': MINUS,
        '*': MULTIPLY,
        '/': DIVIDE,
        '(': LPAREN,
        ')': RPAREN,
        '[': LBR,
        ']': RBR,
        '\t': TAB,
        ' ' * n_tabs: TAB,
        ',': COMMA,
        ':': COLON,
        ';': SEMICOLON,
        '<': LESS,
        '>': GREATER,
        "'": SINGLE_QUOTE,
        '"': DOUBLE_QUOTE,
        '.': DOT,
        '\n': NEWLINE
    }

    def error(self, message):
        print("Lexer error:", message, f"at line {self.row}, index {self.col - 1}")
        sys.exit(1)

    def get_next_char(self):
        if self.current_char == '\n':
            self.row += 1
            self.col = 0
        if self.current_pos < self.input_length:
            self.current_char = self.input_string[self.current_pos]
            self.current_pos += 1
            self.col += 1
        else:
            self.current_char = ''

    def get_next_token(self):
        self.state = None
        self.value = None
        while self.state is None:
            if self.current_char is None:
                self.get_next_char()
            # end of file
            if self.current_char == '':
                self.state = Lexer.EOF
            # comment
            elif self.current_char == '/':
                previousChar = self.current_char
                self.get_next_char()
                if previousChar == self.current_char == '/':
                    while self.current_char not in ['', '\n']:
                        self.get_next_char()
                    if self.current_char == "\n":
                        self.get_next_char()
                else:
                    self.state = Lexer.DIVIDE
                    self.value = '/'
                    self.get_next_char()
            # whitespaces and tabulation
            elif self.current_char in [' ', '\t', '\n']:
                self.get_next_char()
            # string quote1
            elif self.current_char == "'":
                self.state = Lexer.STRING
                self.value = ""
                self.get_next_char()
                while self.current_char != "'":
                    self.value += self.current_char
                    self.get_next_char()
                self.get_next_char()
            # string quote2
            elif self.current_char == '"':
                self.state = Lexer.STRING
                self.value = ""
                self.get_next_char()
                while self.current_char != '"':
                    self.value += self.current_char
                    self.get_next_char()
                self.get_next_char()
            # symbols
            elif self.current_char in Lexer.SYMBOLS:
                if self.current_char == ':':
                    self.get_next_char()
                    if self.current_char == '=':
                        self.state = Lexer.ASSIGN
                        self.value = ':='
                        self.get_next_char()
                    else:
                        self.state = Lexer.COLON
                        self.value = ':'
                        self.get_next_char()
                else:
                    self.state = Lexer.SYMBOLS[self.current_char]
                    self.value = self.current_char  # ?
                    self.get_next_char()  # ?
            # numbers float and integer
            elif self.current_char != None and self.current_char.isdigit():
                number = 0
                while self.current_char.isdigit():
                    number = number * 10 + int(self.current_char)
                    self.get_next_char()
                if self.current_char.isalpha() or self.current_char == "_":
                    self.error(f'Invalid identifier')
                if self.current_char == '.':
                    number = str(number)
                    number += '.'
                    self.get_next_char()
                    while self.current_char.isdigit():
                        number += self.current_char
                        self.get_next_char()
                    if self.current_char.isdigit() == False and self.current_char != ';' or number[
                        len(number) - 1] == '.':
                        self.error(f'Invalid number ')

                    self.state = Lexer.REAL
                else:
                    self.state = Lexer.INTEGER
                self.value = str(number)
            # identifiers, keywords and reserved names
            elif self.current_char != None and self.current_char.isalpha() or self.current_char == '_':
                identifier = ""
                while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
                    identifier += self.current_char
                    self.get_next_char()
                if identifier in Lexer.KEYWORDS:
                    self.state = Lexer.KEYWORDS[identifier]
                    self.value = identifier  # ?
                elif identifier in Lexer.RESERVED_NAMES:
                    self.state = Lexer.IDENTIFIER
                    self.value = identifier  # ?
                else:
                    self.state = Lexer.IDENTIFIER
                    self.value = identifier
            else:
                self.error(f'Unexpected symbol: {self.current_char}')

        token = Token(self.row, self.col, self.state, self.value)
        return token