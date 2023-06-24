<program> ::= <statement_list>

<statement_list> ::= <statement> | <statement> <statement_list>

<statement> ::= <assignment_statement>
	     | <var_statement>
             | <function_declaration>
             | <function_call>
             | <procedure_declaration>
             | <procedure_call>
             | <if_statement>
             | <while_statement>
             | <for_statement>
             | <expression_statement>


<assignment_statement> ::= <identifier> ':=' <expression> ';'

<var_statement> ::= 'var' <identifier> ':' <types> ';'

<function_declaration> ::= 'function' <identifier> '(' <param_list> ')' ':' <types> ';' 'begin' <statement_list> 'end' ';'
<function_call> ::= <identifier> '(' <argument_list> ')' ';'

<procedure_declaration> ::= 'procedure' <identifier> '(' <param_list> ')' 'begin' <statement_list> 'end' ';'
<procedure_call> ::= <identifier> '(' <argument_list> ')' ';'
 
<if_statement> ::= 'if' <expression> 'then' 'begin' <statement_list> 'end' <else_statement>
<else_statement> ::= 'else' 'begin' <statement_list> 'end' ';' | ''

<while_statement> ::= 'while' <expression> 'do' 'begin' <statement_list> 'end;' | 'while' '(' <expression> ')' 'do' 'begin' <statement_list> 'end;'

<for_statement> ::= 'for' <identifier> 'to' <number> 'do' 'begin' <statement_list> 'end' ';' | 'for' 'var' <assignment_statement> 'to' <number> 'do' 'begin' <statement_list> 'end' ';'

<expression_statement> ::= <expression> ';'

<expression> ::= <term> | <expression> <additive_operator> <term>	| <expression> <relational_operator> <term>

<term> ::= <factor> | <factor> <multiplicative_operator> <term>

<factor> ::= <integer> | real | <string> | <char> | <boolean> | '(' <expression> ')' | <function_call>

<relational_operator> ::= '=' | '<>' | '<' | '>' | '<=' | '>='
<additive_operator> ::= '+' | '-'
<multiplicative_operator> ::= '*' | '/' | 'div' | 'mod'

<param_list> ::= <identifier> | <identifier> ',' <param_list>

<argument_list> ::= <expression> | <expression> ',' <argument_list>

<identifier> ::= <letter> | <identifier_char> | '_'

<number> ::= <integer> | <real>

<integer> ::= <digit>+
<real> ::= <digit>+ '.' <digit>* | '.' <digit>+
<string> ::= '"' <character>* '"' | "'" <character>* "'"
<boolean> ::= 'true' | 'false'
<char> ::= <letter> | '' | ' ' | 
<array> ::= 'array' <bounds> 'of' <types> ';'
<bounds> ::= '[' <number> '..' <number> ']'

<types> ::= <integer> | real | <string> | <char> | <boolean> | <array>

<letter> ::= [a-zA-Z]
<digit> ::= [0-9]

<identifier_char> ::= <letter>+ | <digit>+ | '_'
