import ply.lex as lex 
import ply.yacc as yacc

# ok so for this, we will have to have a parser for 'function', and then any content which could either start with _ or a letter, followed by anything else, after follows brackets which may or may not have a string(s) in it. 


# states
states = (('content', 'exclusive'),)


tokens = ('FUNCTION', 'ID', 'COMMA',)

def t_INITIAL_FUNCTION(t):
    r'function'
    t.type = 'FUNCTION'
    t.lexer.begin('id')
    return t

def t_FUNCTION_error(t):
    print(f"[FUNCTION] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

def t_ID(t): 
    r'[A-Z]'


lexer = lex.lex()

def p_sequence(p):
    '''S : FUNCTION CONTENT'''
    p[0] = p[2]


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()


print("Enter '--content' (e.g., --hello-world). Press Ctrl+D (or Ctrl+Z on Windows) to exit.")
while True:
    try:
        data = input("Enter Single Line: ")
    except EOFError:
        print("\nExiting.")
        break
    
    
    if not data:
        continue

    parsed = parser.parse(data, lexer=lexer)
    if parsed is not None:
        print("Accepted")


