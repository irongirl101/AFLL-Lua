# Lua Operators Parser 
import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'NUMBER', 'IDENTIFIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN'
)

t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_POWER  = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+(\.\d+)?'
    t.value = float(t.value)
    return t

def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

def t_error(t):
    # Stop parsing on illegal character
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    t.lexer.skip(1)
    raise SyntaxError(f"Illegal character '{t.value[0]}'")

lexer = lex.lex()

precedence = (
    ('right', 'POWER'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'PLUS', 'MINUS'),
)

def p_expression_plus_minus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    if p[2] == '+': p[0] = p[1] + p[3]
    else: p[0] = p[1] - p[3]

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_times_divide(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    if p[2] == '*': p[0] = p[1] * p[3]
    else: p[0] = p[1] / p[3]

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_power(p):
    'factor : base POWER factor'
    p[0] = p[1] ** p[3]

def p_factor_base(p):
    'factor : base'
    p[0] = p[1]

def p_base_number(p):
    'base : NUMBER'
    p[0] = p[1]

def p_base_identifier(p):
    'base : IDENTIFIER'
    p[0] = 0
    print(f"Note: '{p[1]}' treated as 0 for evaluation")

def p_base_parens(p):
    'base : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error near '{p.value}' at position {p.lexpos}")
    else:
        raise SyntaxError("Syntax error at EOF")

parser = yacc.yacc()

print("Lua Arithmetic Operators Parser (supports + - * / ^ and parentheses)")
while True:
    try:
        s = input("\nEnter expression (or 'exit' to quit): ")
    except EOFError:
        break
    if not s or s.lower() == 'exit':
        break
    try:
        result = parser.parse(s)
        print("Valid Expression")
        print("Result:", result)
    except SyntaxError as e:
        print("Invalid Expression:", e)
    except Exception as e:
        print("Unexpected Error:", e)
