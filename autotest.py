import unittest
from io import StringIO
from lexer import Lexer, Token

class LexerTestCase(unittest.TestCase):
    def test_lexer(self):
        input_code = """
        program HelloWorld;
        begin
            var x : integer;
            writeln('Hello, World!');
            x := -1.0;
        end.
        """

        expected_tokens = [
            Token(3, 1, 'IDENTIFIER', 'program'),
            Token(3, 9, 'IDENTIFIER', 'HelloWorld'),
            Token(3, 19, 'SEMICOLON', ';'),
            Token(4, 1, 'BEGIN', 'begin'),
            Token(5, 5, 'IDENTIFIER', 'var'),
            Token(5, 9, 'IDENTIFIER', 'x'),
            Token(5, 11, 'IDENTIFIER', 'integer'),
            Token(5, 18, 'SEMICOLON', ';'),
            Token(6, 5, 'IDENTIFIER', 'writeln'),
            Token(6, 13, 'LPAREN', '('),
            Token(6, 14, 'STRING', 'Hello, World!'),
            Token(6, 29, 'RPAREN', ')'),
            Token(6, 30, 'SEMICOLON', ';'),
            Token(7, 5, 'IDENTIFIER', 'x'),
            Token(7, 7, 'ASSIGN', ':='),
            Token(7, 10, 'MINUS', '-'),
            Token(7, 11, 'REAL', '1.0'),
            Token(7, 14, 'SEMICOLON', ';'),
            Token(8, 1, 'END', 'end'),
            Token(8, 4, 'DOT', '.')
        ]

        lexer = Lexer(input_code)
        actual_tokens = []
        while True:
            token = lexer.get_next_token()
            actual_tokens.append(token)
            if token.type == Lexer.EOF:
                break

        self.assertEqual(actual_tokens, expected_tokens)

if __name__ == '__main__':
    unittest.main()