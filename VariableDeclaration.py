import ply.lex as lex
import ply.yacc as yacc

tokens = ('ID', 'COMMA', 'EQUAL', 'LOCAL', 'NUMBER')

t_COMMA = r','
t_EQUAL = r'='

t_ignore = ' \t\n'

reserved = {
    'local': 'LOCAL'
}

def t_ID(t): 
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value, 'ID')
    return t

def t_NUMBER(t): 
    r'\d+'
    t.value = int(t.value)
    return t 

def t_error(t): 
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

lexer = lex.lex()



def p_statement(p):
    '''statement : local_declaration
                 | assignment'''
    p[0] = p[1]
   

def p_local_declaration(p): 
    # both must start with LOCAL
    '''local_declaration : LOCAL var_list
                         | LOCAL var_list EQUAL exp_list'''
    if len(p) == 3: 
        # Case: local a, b
        p[0] = ('local_dec', p[2], None)
    else:
        # Case: local a, b = c, d
        p[0] = ('local_dec', p[2], p[4])

def p_assignment(p):
    '''assignment : var_list EQUAL exp_list'''
    p[0] = ('assignment', p[1], p[3])

def p_var_list(p):
    '''var_list : ID 
                | ID COMMA var_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_exp_list(p): 
    '''exp_list : expression
                | expression COMMA exp_list'''
    if len(p) == 2:
         p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_expression(p):
    '''expression : ID
                  | NUMBER'''
    p[0] = p[1]

def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()

print("Parser ready. Enter Lua declarations (e.g., 'local a, b = 1, x' or 'c = 10').")

while True:
    try:
        data = input("Enter Variable Declaration: ")
    except EOFError:
        print("\nExiting.")
        break
    
    if not data:
        continue
    parsed = parser.parse(data, lexer=lexer)
    if parsed is not None:
        print("Accepted")