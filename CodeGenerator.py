def generate_cpp_code(pascal_ast):
    cpp_code = ""

    if pascal_ast.type == "PROGRAM":
        # Генерация заголовка программы
        program_name = pascal_ast.children[0].value
        cpp_code += f"#include <iostream>\n\n"
        cpp_code += f"int main() {{\n"

        # Генерация остальной части программы
        statement_list = pascal_ast.children[0]
        cpp_code += generate_cpp_code(statement_list)

        # Завершение программы
        cpp_code += f"\n    return 0;\n"
        cpp_code += f"}}"

    elif pascal_ast.type == "STATEMENT_LIST":
        for statement in pascal_ast.children:
            cpp_code += generate_cpp_code(statement)

    elif pascal_ast.type == "ASSIGNMENT_STATEMENT":
        variable = pascal_ast.children[0].value
        value = generate_cpp_code(pascal_ast.children[1])
        cpp_code += f"    {variable} = {value};\n"

    elif pascal_ast.type == "VAR_STATEMENT":
        variable = pascal_ast.children[0].value
        data_type = pascal_ast.children[1].value
        cpp_code += f"    {data_type} {variable};\n"

    elif pascal_ast.type == "FUNCTION_DECLARATION":
        function_name = pascal_ast.children[0].value
        return_type = pascal_ast.children[1].value
        parameters = generate_cpp_code(pascal_ast.children[2])
        function_body = generate_cpp_code(pascal_ast.children[3])
        cpp_code += f"{return_type} {function_name}({parameters}) {{\n"
        cpp_code += f"{function_body}\n"
        cpp_code += f"}}\n"

    elif pascal_ast.type == "FUNCTION_CALL":
        function_name = pascal_ast.children[0].value
        arguments = generate_cpp_code(pascal_ast.children[1])
        cpp_code += f"{function_name}({arguments});\n"

    elif pascal_ast.type == "PARAM_LIST":
        params = []
        for param in pascal_ast.children:
            params.append(generate_cpp_code(param))
        cpp_code += ", ".join(params)

    elif pascal_ast.type == "ARGUMENT_LIST":
        args = []
        for arg in pascal_ast.children:
            args.append(generate_cpp_code(arg))
        cpp_code += ", ".join(args)

    elif pascal_ast.type == "IF_STATEMENT":
        condition = generate_cpp_code(pascal_ast.children[0])
        if_body = generate_cpp_code(pascal_ast.children[1])
        else_body = generate_cpp_code(pascal_ast.children[2])
        cpp_code += f"if ({condition}) {{\n"
        cpp_code += f"{if_body}\n"
        cpp_code += f"}}"
        if else_body:
            cpp_code += f" else {{\n"
            cpp_code += f"{else_body}\n"
            cpp_code += f"}}\n"

    elif pascal_ast.type == "WHILE_STATEMENT":
        condition = generate_cpp_code(pascal_ast.children[0])
        loop_body = generate_cpp_code(pascal_ast.children[1])
        cpp_code += f"while ({condition}) {{\n"
        cpp_code += f"{loop_body}\n"
        cpp_code += f"}}\n"

    elif pascal_ast.type == "FOR_STATEMENT":
        variable = pascal_ast.children[0].value
        start_value = generate_cpp_code(pascal_ast.children[1])
        end_value = generate_cpp_code(pascal_ast.children[2])
        loop_body = generate_cpp_code(pascal_ast.children[3])
        cpp_code += f"for ({variable} = {start_value}; {variable} <= {end_value}; {variable}++) {{\n"
        cpp_code += f"{loop_body}\n"
        cpp_code += f"}}\n"

    elif pascal_ast.type == "EXPRESSION_STATEMENT":
        expression = generate_cpp_code(pascal_ast.children[0])
        cpp_code += f"{expression};\n"

    elif pascal_ast.type == "EXPRESSION":
        if len(pascal_ast.children) == 1:
            cpp_code += generate_cpp_code(pascal_ast.children[0])
        elif len(pascal_ast.children) == 3:
            left_operand = generate_cpp_code(pascal_ast.children[0])
            operator = pascal_ast.children[1].value
            right_operand = generate_cpp_code(pascal_ast.children[2])
            cpp_code += f"{left_operand} {operator} {right_operand}"

    elif pascal_ast.type == "FACTOR":
        if pascal_ast.children[0].type == "FUNCTION_CALL":
            cpp_code += generate_cpp_code(pascal_ast.children[0])
        else:
            cpp_code += pascal_ast.children[0].value

    elif pascal_ast.type == "RELATIONAL_OPERATOR":
        cpp_code += pascal_ast.children[0].value

    elif pascal_ast.type == "ADDITIVE_OPERATOR":
        cpp_code += pascal_ast.children[0].value

    elif pascal_ast.type == "MULTIPLICATIVE_OPERATOR":
        cpp_code += pascal_ast.children[0].value

    return cpp_code


# Пример использования
pascal_ast = parse_pascal_code(pascal_code)
cpp_code = generate_cpp_code(pascal_ast)
print(cpp_code)
