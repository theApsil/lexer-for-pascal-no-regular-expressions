from lexer import Lexer, Token
from parser import Parser

with open('code.pas', 'r') as file:
    input_code = file.read()

lexer = Lexer(input_code)
parser = Parser(lexer)
parse_tree = parser.parse()
print(parse_tree)
# while True:
#     token = lexer.get_next_token()
#     if token.type == Lexer.EOF:
#         break
#     print(token)