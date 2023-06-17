import unittest
from lexer import Lexer, Token
import sys

class LexerTestCase(unittest.TestCase):
    def test_program(self):
        input_string = "program test; end."
        expected_tokens = [
            "Token: \tType: program \tValue: <program>",
            "Token: \tType: identifier \tValue: <test>",
            "Token: \tType: semicolon \tValue: <;>",
            "Token: \tType: end \tValue: <end>",
            "Token: \tType: dot \tValue: <.>"
        ]
        self.assertTokensEqual(input_string, expected_tokens)

    def test_variables(self):
        input_string = "var x: integer; end."
        expected_tokens = [
            "Token: \tType: var \tValue: <var>",
            "Token: \tType: identifier \tValue: <x>",
            "Token: \tType: colon \tValue: <:>",
            "Token: \tType: integer \tValue: <integer>",
            "Token: \tType: semicolon \tValue: <;>",
            "Token: \tType: end \tValue: <end>",
            "Token: \tType: dot \tValue: <.>"
        ]
        self.assertTokensEqual(input_string, expected_tokens)

    def test_while_loop(self):
        input_string = "while i < 10 do i := i + 1; end."
        expected_tokens = [
            "Token: \tType: while \tValue: <while>",
            "Token: \tType: identifier \tValue: <i>",
            "Token: \tType: less \tValue: <<>",
            "Token: \tType: integer \tValue: <10>",
            "Token: \tType: do \tValue: <do>",
            "Token: \tType: identifier \tValue: <i>",
            "Token: \tType: assign \tValue: <:=>",
            "Token: \tType: identifier \tValue: <i>",
            "Token: \tType: plus \tValue: <+>",
            "Token: \tType: integer \tValue: <1>",
            "Token: \tType: semicolon \tValue: <;>",
            "Token: \tType: end \tValue: <end>",
            "Token: \tType: dot \tValue: <.>"
        ]
        self.assertTokensEqual(input_string, expected_tokens)

    # Add more test cases here

    def assertTokensEqual(self, input_string, expected_tokens):
        lexer = Lexer(input_string)
        tokens = []
        token = Token(0, 0, '', '')
        while True:
            token = lexer.get_next_token()
            tokens.append(str(token))
            if token.value == 'end':
                previousToken = token
                token = lexer.get_next_token()
                if previousToken.value == 'end' and token.value == '.':
                    tokens.append(str(token))
                    break
        self.assertEqual(tokens, expected_tokens)

if __name__ == "__main__":
    unittest.main()
