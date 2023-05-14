import sys

class Token:
    def __init__(self, row, col, type, value):
        self.row, self.col, self.type, self.value = row, col, type, value

    def __repr__(self):
        return f"Token: \tType: {Lexer.PRESENTATION[self.type]} \tValue: <{self.value}>"

    def __str__(self):
        return f"\tType: {Lexer.PRESENTATION[self.type]} \tValue: <{self.value}>"


class Lexer:
    def __init__(self, file):
        self.file = open(file, 'r')
        self.state = None

    # Типы лексем (токенов)
    PROGRAM, VAR, BEGIN, INTEGER, REAL, \
    BOOLEAN, CHAR, STRING, IF, THEN, ELSE, \
    WHILE, DO, REPEAT, UNTIL, WRITE, READ, \
    WRITELN, READLN, FUNCTION, PROCEDURE, \
    NOT, IDENTIFIER, FOR, LPAREN, RPAREN, \
    TRUE, FALSE, RBR, LBR, LESS, GREATER, \
    TAB, DOT, COMMA, COLON, SEMICOLON, \
    SINGLE_QUOTE, DOUBLE_QUOTE, \
    PLUS, MINUS, MULTIPLY, ASSIGN, DIVIDE, END, EOF, \
    AND, NOT, IN, NEWLINE, RESULT, EQUAL = range(52)


    PRESENTATION = {
        PROGRAM      : "program",
        VAR          : "var",
        BEGIN        : "begin",
        INTEGER      : "integer",
        REAL         : "real",
        BOOLEAN      : "boolean",
        CHAR         : "char",
        STRING       : "string",
        IF           : "if",
        THEN         : "then",
        ELSE         : "else",
        EQUAL        : "equal",
        WHILE        : "while",
        DO           : "do",
        REPEAT       : "repeat",
        UNTIL        : "until",
        FUNCTION     : "function",
        PROCEDURE    : "procedure",
        NOT          : "not",
        WRITE        : "write",
        READ         : "read",
        WRITELN      : "writeln",
        READLN       : "readln",
        FOR          : "for",
        LPAREN       : "lparen",
        RPAREN       : "rparen",
        TRUE         : "true",
        FALSE        : "false",
        RBR          : "rbr",
        LBR          : "lbr",
        LESS         : "less",
        GREATER      : "greater",
        TAB          : "tab",
        DOT          : "dot",
        COMMA        : "comma",
        COLON        : "colon",
        SEMICOLON    : "semicolon",
        SINGLE_QUOTE : "singleQuote",
        DOUBLE_QUOTE : "doubleQuote",
        PLUS         : "plus",
        MINUS        : "minus",
        MULTIPLY     : "multiply",
        ASSIGN       : "assign",
        DIVIDE       : "divide",
        END          : "end",
        EOF          : "eof",
        AND          : "and",
        NOT          : "not",
        IN           : "in",
        NEWLINE      : "newline",
        RESULT       : "result",
        IDENTIFIER: "identifier"
    }

    KEYWORDS = {
        'if'        : IF,
        'else'      : ELSE,
        'while'     : WHILE,
        'for'       : FOR,
        'do'        : DO,
        'function'  : FUNCTION,
        'procedure' : PROCEDURE,
        'repeat'    : REPEAT,
        'and'       : AND,
        'in'        : IN,
        'end'       : END,
        'var'       : VAR,
        'program'   : PROGRAM,
        'then'      : THEN,
        'begin'     : BEGIN
    }

    RESERVED_NAMES = {
        'write'   : WRITE,
        'read'    : READ,
        'writeln' : WRITELN,
        'readln'  : READLN,
        'true'    : TRUE,
        'false'   : FALSE,
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
        '\n': NEWLINE,
    }

    current_char = None
    row, col = 1, 0

    def error(self, message):
        print("Lexer error:", message, f"at line {self.row}, index {self.col - 1}")
        sys.exit(1)

    def get_next_char(self):
        if self.current_char == '\n':
            self.row += 1
            self.col = 0
        self.current_char = self.file.read(1)
        self.col += 1


    def get_next_token(self):
        self.state = None
        self.value = None
        while self.state == None:
            if self.current_char == None:
                self.get_next_char()
            # end of file
            if len(self.current_char) == 0:
                self.state = Lexer.EOF
            # comment
            elif self.current_char == '#':
                while self.current_char not in ['\n', '']:
                    self.get_next_char()
                if self.current_char == "\n":
                    self.get_next_char()
            # whitespaces and tabulation
            elif self.current_char in [' ', '\t', '\n']:
                match self.current_char:
                    case '\t':
                        self.state = Lexer.SYMBOLS[self.current_char]
                        self.value = self.current_char
                        self.get_next_char()
                    case ' ':
                        tabulation = ""
                        col = self.col
                        while self.current_char == ' ':
                            tabulation += self.current_char
                            self.get_next_char()
                            if len(tabulation) == self.n_tabs and col == 1: # if new line
                                self.state = Lexer.SYMBOLS[tabulation]
                                self.value = tabulation
                        if len(tabulation) != self.n_tabs and len(tabulation) > 1: # if new line
                            if col == 1:
                                self.error(f'Incorrect indent')
                    case '\n':
                        self.state = self.state = Lexer.SYMBOLS[self.current_char]
                        self.value = self.current_char
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
                    self.state = Lexer.SYMBOLS[self.current_char]
                    self.value = self.current_char #?
                    self.get_next_char() #?
            # numbers float and integer
            elif self.current_char.isdigit():
                number = 0
                while self.current_char.isdigit():
                    number = number*10 + int(self.current_char)
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
                    if self.current_char.isdigit() == False and self.current_char != ';' or number[len(number) - 1] == '.':
                        self.error(f'Invalid number ')

                    self.state = Lexer.REAL
                else:
                    self.state = Lexer.INTEGER
                self.value = str(number)
            # identifiers, keywords and reserved names
            elif self.current_char.isalpha() or self.current_char == '_':
                identifier = ""
                while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
                    identifier += self.current_char
                    self.get_next_char()
                if identifier in Lexer.KEYWORDS:
                    self.state = Lexer.KEYWORDS[identifier]
                    self.value = identifier #?
                elif identifier in Lexer.RESERVED_NAMES:
                    self.state = Lexer.IDENTIFIER
                    self.value = identifier #?
                else:
                    self.state = Lexer.IDENTIFIER
                    self.value = identifier
            else:
                self.error(f'Unexpected symbol: {self.current_char}')
        token = Token(self.row, self.col, self.state, self.value)
        return token