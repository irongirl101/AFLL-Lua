# importing lexer and parser 
import ply.lex as lex
import ply.yacc as yacc
# not we are only inputing integer types, and not float or any other data type. 

# tokens 
tokens = ('ID', 'COMMA', 'EQUAL', 'LOCAL', 'NUMBER')

t_COMMA = r','
t_EQUAL = r'='

t_ignore = ' \t\n'

# keyword that cannot be used as an identifier 
reserved = {
    'local': 'LOCAL'
}

def t_ID(t): 
    r'[a-zA-Z_][a-zA-Z_0-9]*' # token can accept anything 
    t.type = reserved.get(t.value, 'ID') # add ID tag 
    return t

def t_NUMBER(t): 
    r'-\d+' # accepting any integer 
    t.value = int(t.value) # type casting 
    return t 

# error 
def t_error(t): 
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# building lexer 
lexer = lex.lex()

# CFG 
def p_statement(p):
    '''statement : local_declaration
                 | assignment'''
    p[0] = p[1]
   
# CFG 
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
# CFG 
def p_assignment(p):
    '''assignment : var_list EQUAL exp_list'''
    p[0] = ('assignment', p[1], p[3])
# CFG 
def p_var_list(p):
    '''var_list : ID 
                | ID COMMA var_list'''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
# CFG 
def p_exp_list(p): 
    '''exp_list : expression
                | expression COMMA exp_list'''
    if len(p) == 2:
         p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

# CFG 
def p_expression(p):
    '''expression : ID
                  | NUMBER'''
    p[0] = p[1]

# error 
def p_error(p):
    if p:
        print(f"Syntax error at '{p.value}' (type: {p.type}) on line {p.lineno}")
    else:
        print("Syntax error at EOF")

#building parser 
parser = yacc.yacc()

# main
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


    parser.parse(data, lexer=lexer)