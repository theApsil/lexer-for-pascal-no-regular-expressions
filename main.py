from lexer import Lexer, Token
from parser import Parser

f = open("code.pas")

lexer = Lexer(f)
token = lexer.get_next_token()
while token.name != Token.EOF:
    print(token)
    token = lexer.get_next_token()
print(token)
f.close()


