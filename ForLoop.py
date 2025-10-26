# Lua 'for' Loop Parser
import ply.lex as lex
import ply.yacc as yacc


tokens = ('FOR', 'IDENTIFIER', 'EQUAL', 'NUMBER')

reserved = {
    'for': 'FOR'
}

t_EQUAL = r'='
t_ignore = ' \t'

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[t.value]
    return t

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()


def p_loop(p):
    '''loop : FOR IDENTIFIER EQUAL NUMBER'''
    n = p[4]
    print(f"\n Valid 'for' loop detected: repeating {n} times.")
    num = int(input("Enter a number to print: "))
    for _ in range(n):
        print(num)

def p_error(p):
    if p:
        print(f"Syntax error near '{p.value}'")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

print("for Loop Parser (form: for i = n)")
print("Example: for i = 5\n")

while True:
    try:
        data = input("Enter loop: ")
    except EOFError:
        print("\nExiting.")
        break

    if not data:
        continue

    result = parser.parse(data)

