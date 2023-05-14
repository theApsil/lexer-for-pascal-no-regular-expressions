from lexer import Lexer

lexer = Lexer("code.pas")
while True:
    token = lexer.get_next_token()
    if token.type == Lexer.EOF:
        break
    if token.type != Lexer.NEWLINE and token.type != Lexer.TAB:
        print(token)
