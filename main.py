from lexer import Lexer, Token


with open('code.pas', 'r') as file:
    input_code = file.read()

lexer = Lexer(input_code)
token = Token(0, 0, '', '')
while True:
    token = lexer.get_next_token()
    if token.value == 'end':
        previousToken = token
        token = lexer.get_next_token()
        if previousToken.value == 'end' and token.value == '.':
            print(previousToken)
            print(token)
            break
    if token.type == Lexer.EOF:
        break
    print(token)