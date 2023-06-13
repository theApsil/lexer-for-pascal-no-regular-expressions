import sys


class Token:
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
        AND, NOT, IN, NEWLINE, RESULT, EQUAL, ARRAY, TO, \
        OF, LE, GE, SLASH, NOTEQ, ARRDOT, NUMBER, COMMENT = range(62)

    token_names = {
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

    def __init__(self, token, value, line, position):
        self.name = token
        self.value = value
        self.line = line
        self.position = position

    def __repr__(self):
        return f'({self.token_names[self.name]}, {self.value})'


class Lexer:
    def __init__(self, file):
        self.file = file
        self.line = 0
        self.pos = 0
        self.statement = None
        self.char = None

    def error(self, message):
        print("Lexer error!", message, f"at line {self.row}, index {self.col - 1}")
        sys.exit(1)

    def __get_next_char(self):
        self.char = self.file.read(1)
        self.pos += 1
        if self.char == '\n':
            self.line += 1
            self.pos = 1


    def get_next_token(self):
        match self.statement:
            case None:
                if self.char is None:
                    self.__get_next_char()
                    return self.get_next_token()
                elif self.char in ['\n', ' ']:
                    self.__get_next_char()
                    return self.get_next_token()
                elif self.char == '':
                    return Token(Token.EOF, "", self.line, self.pos)
                elif self.char == '+':
                    self.__get_next_char()
                    return Token(Token.PLUS, "+", self.line, self.pos)
                elif self.char == '-':
                    self.__get_next_char()
                    return Token(Token.MINUS, "-", self.line, self.pos)
                elif self.char == '*':
                    self.__get_next_char()
                    return Token(Token.MULTIPLY, "*", self.line, self.pos)
                elif self.char == '(':
                    self.__get_next_char()
                    return Token(Token.LBR, "(", self.lineno, self.pos)
                elif self.char == ')':
                    self.__get_next_char()
                    return Token(Token.RBR, ")", self.lineno, self.pos)
                elif self.char == '[':
                    self.__get_next_char()
                    return Token(Token.LPAREN, "[", self.lineno, self.pos)
                elif self.char == ']':
                    self.__get_next_char()
                    return Token(Token.RPAREN, "]", self.lineno, self.pos)
                elif self.char == ';':
                    self.__get_next_char()
                    return Token(Token.SEMICOLON, ";", self.lineno, self.pos)
                elif self.char == ',':
                    self.__get_next_char()
                    return Token(Token.COMMA, ",", self.lineno, self.pos)
                elif self.char == '/':
                    self.state = Token.SLASH
                    return self.get_next_token()
                elif self.char == '=':
                    self.state = Token.EQUAL
                    return self.get_next_token()
                elif self.char == '<':
                    self.state = Token.LESS
                    return self.get_next_token()
                elif self.char == '>':
                    self.state = Token.GREATER
                    return self.get_next_token()
                elif self.char == ':':
                    self.state = Token.COLON
                    return self.get_next_token()
                elif self.char == '"':
                    self.state = Token.DOUBLE_QUOTE
                    return self.get_next_token()
                elif self.char == "'":
                    self.state = Token.SINGLE_QUOTE
                    return self.get_next_token()
                elif self.char == ".":
                    self.state = Token.DOT
                    return self.get_next_token()
                elif self.char.isalpha() or self.char == '_':
                    self.state = Token.IDENTIFIER
                    return self.get_next_token()
                elif self.char.isdigit():
                    self.state = Token.NUMBER
                    return self.get_next_token()
                else:
                    self.error("Unexpected symbol!")

            case Token.SLASH:
                self.__get_next_char()
                if self.char == "/":
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.COMMENT, "//", self.line, self.pos)
                else:
                    self.error(f"Expected /, but got {self.char}")
            case Token.COLON:
                self.__get_next_char()
                if self.char == "=":
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.ASSIGN, ":=", self.line, self.pos)
                else:
                    self.state = None
                    return Token(Token.COLON, ":", self.line, self.pos)
            case Token.LESS:
                self.__get_next_char()
                if self.char == "=":
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.LE, "<=", self.line, self.pos)
                elif self.char == ">":
                    self.state == None
                    self.__get_next_char()
                    return Token(Token.NOTEQ, "<>", self.line, self.pos)
                else:
                    self.state = None
                    return Token(Token.LESS, "<", self.line, self.pos)
            case Token.GREATER:
                self.__get_next_char()
                if self.char == "=":
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.GE, ">=", self.line, self.pos)
                else:
                    self.state = None
                    return Token(Token.GREATER, ">", self.line, self.pos)
            case Token.SINGLE_QUOTE:
                self.__get_next_char()
                string_literal = ""
                while self.char != "'":
                    if self.char == '':  # если достигнут конец файла
                        self.error('Closing quote expected!')
                    string_literal += self.char
                    self.__get_next_char()
                self.__get_next_char()
                self.state = None
                return Token(Token.SINGLE_QUOTE, string_literal, self.lineno, self.pos - 2)
            case Token.DOUBLE_QUOTE:
                self.__get_next_char()
                string_literal = ""
                while self.char != '"':
                    if self.char == '':  # если достигнут конец файла
                        self.error('Closing quote expected!')
                    string_literal += self.char
                    self.__get_next_char()
                self.__get_next_char()
                self.state = None
                return Token(Token.SINGLE_QUOTE, string_literal, self.lineno, self.pos - 2)
            case Token.DOT:
                self.__get_next_char()
                if self.char == ".":
                    self.state = None
                    self.__get_next_char()
                    return Token(Token.ARRDOT, "..", self.line, self.pos)
                else:
                    self.state = None
                    return Token(Token.DOT, ".", self.line, self.pos)
            case Token.NUMBER:
                int_literal = ""
                while self.char.isdigit():
                    int_literal += self.char
                    self.__get_next_char()
                if self.char == '.':
                    self.state = Token.REAL
                    float_literal = int_literal + '.'
                    self.__get_next_char()
                    while self.char.isdigit():
                        float_literal += self.char
                        self.__get_next_char()
                        if self.char == ".":
                            self.error("Wrong REAL declaration!")

                if self.char.isalpha() or self.char == '_':
                    self.error("Invalid ID entry!")
                if self.state == Token.INTEGER:
                    self.state = None
                    return Token(Token.INTEGER, int_literal, self.lineno, self.pos - 1)
                if self.state == Token.REAL:
                    self.state = None
                    return Token(Token.REAL, float_literal, self.lineno, self.pos - 1)
            case Token.IDENTIFIER:
                id = self.char
                self.__get_next_char()
                while self.char.isalpha() or self.char.isdigit() or self.char == '_':
                    id += self.char
                    self.__get_next_char()
                self.state = None
                if id in Token.KEYWORDS:
                    return Token(Token.KEYWORDS[id], id, self.lineno, self.pos - 1)
                else:
                    return Token(Token.IDENTIFIER, id, self.lineno, self.pos - 1)
        #
        # self.state = None
        # self.value = None
        # while self.state is None:
        #     if self.current_char is None:
        #         self.get_next_char()
        #     # end of file
        #     if self.current_char == '':
        #         self.state = Lexer.EOF
        #     # comment
        #     elif self.current_char == '/':
        #         previousChar = self.current_char
        #         self.get_next_char()
        #         if previousChar == self.current_char == '/':
        #             while self.current_char not in ['', '\n']:
        #                 self.get_next_char()
        #             if self.current_char == "\n":
        #                 self.get_next_char()
        #         else:
        #             self.state = Lexer.DIVIDE
        #             self.value = '/'
        #             self.get_next_char()
        #     # whitespaces and tabulation
        #     elif self.current_char in [' ', '\t', '\n']:
        #         self.get_next_char()
        #     # string quote1
        #     elif self.current_char == "'":
        #         self.state = Lexer.STRING
        #         self.value = ""
        #         self.get_next_char()
        #         while self.current_char != "'":
        #             self.value += self.current_char
        #             self.get_next_char()
        #         self.get_next_char()
        #     # string quote2
        #     elif self.current_char == '"':
        #         self.state = Lexer.STRING
        #         self.value = ""
        #         self.get_next_char()
        #         while self.current_char != '"':
        #             self.value += self.current_char
        #             self.get_next_char()
        #         self.get_next_char()
        #     # symbols
        #     elif self.current_char in Lexer.SYMBOLS:
        #         if self.current_char == ':':
        #             self.get_next_char()
        #             if self.current_char == '=':
        #                 self.state = Lexer.ASSIGN
        #                 self.value = ':='
        #                 self.get_next_char()
        #             else:
        #                 self.state = Lexer.COLON
        #                 self.value = ':'
        #                 self.get_next_char()
        #         else:
        #             self.state = Lexer.SYMBOLS[self.current_char]
        #             self.value = self.current_char #?
        #             self.get_next_char() #?
        #     # numbers float and integer
        #     elif self.current_char.isdigit():
        #         number = 0
        #         while self.current_char.isdigit():
        #             number = number*10 + int(self.current_char)
        #             self.get_next_char()
        #         if self.current_char.isalpha() or self.current_char == "_":
        #             self.error(f'Invalid identifier')
        #         if self.current_char == '.':
        #             number = str(number)
        #             number += '.'
        #             self.get_next_char()
        #             while self.current_char.isdigit():
        #                 number += self.current_char
        #                 self.get_next_char()
        #             if self.current_char.isdigit() == False and self.current_char != ';' or number[len(number) - 1] == '.':
        #                 self.error(f'Invalid number ')
        #
        #             self.state = Lexer.REAL
        #         else:
        #             self.state = Lexer.INTEGER
        #         self.value = str(number)
        #     # identifiers, keywords and reserved names
        #     elif self.current_char.isalpha() or self.current_char == '_':
        #         identifier = ""
        #         while self.current_char.isalpha() or self.current_char.isdigit() or self.current_char == '_':
        #             identifier += self.current_char
        #             self.get_next_char()
        #         if identifier in Lexer.KEYWORDS:
        #             self.state = Lexer.KEYWORDS[identifier]
        #             self.value = identifier #?
        #         elif identifier in Lexer.RESERVED_NAMES:
        #             self.state = Lexer.IDENTIFIER
        #             self.value = identifier #?
        #         else:
        #             self.state = Lexer.IDENTIFIER
        #             self.value = identifier
        #     else:
        #         self.error(f'Unexpected symbol: {self.current_char}')
        #
        #
        # token = Token(self.row, self.col, self.state, self.value)
        # return token