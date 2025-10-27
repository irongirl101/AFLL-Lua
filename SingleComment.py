import ply.lex as lex 
import ply.yacc as yacc

# ok for this, as a comment could have hyphens in the comment itself, i need to have two different grammars for both halves. 
# one for the double hyphen, one for the rest of the content, it being anything. 


# states
states = (('content', 'exclusive'),)


tokens = ('DOUBLE_HYPHEN', 'CONTENT')

def t_INITIAL_DOUBLE_HYPHEN(t):
    r'--'
    t.type = 'DOUBLE_HYPHEN'
    t.lexer.begin('content')
    return t

def t_INITIAL_error(t):
    print(f"[INITIAL] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

def t_content_CONTENT(t):
    r'.+'
    t.type = 'CONTENT'
    t.lexer.begin('INITIAL')
    return t

def t_content_error(t):
    print(f"[content] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def p_sequence(p):
    '''S : DOUBLE_HYPHEN CONTENT'''
    p[0] = p[2]


def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()



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

