from lexer import Lexer, Token
from parser import Parser

with open('code.pas', 'r') as file:
    input_code = file.read()

lexer = Lexer(input_code)
token = Token(0, 0, "", "")
while token.type != Lexer.EOF:
    token = lexer.get_next_token()
    print(token)