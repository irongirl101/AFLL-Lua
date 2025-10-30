# importing lexer and parser 
import ply.lex as lex 
import ply.yacc as yacc

# ok for this, as a comment could have hyphens in the comment itself, i need to have two different grammars for both halves. 
# one for the double hyphen, one for the rest of the content, it being anything. 

# states
# why have states? -> well, in the initial stage, you are looking for only --, and you should have a CFG for the content added as well. so 
# you must change to the content state, which is exclusive of the initial state, for that parse. 
states = (('content', 'exclusive'),)

#tokens 
tokens = ('DOUBLE_HYPHEN', 'CONTENT')

# LEXER 
def t_INITIAL_DOUBLE_HYPHEN(t):
    r'--'
    t.type = 'DOUBLE_HYPHEN' #assigning '--' to double hyphen token 
    t.lexer.begin('content') # once read go to content state 
    return t

# error 
def t_INITIAL_error(t):
    print(f"[INITIAL] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

# t for content 
def t_content_CONTENT(t):
    r'.+' # content can accept anything. 
    t.type = 'CONTENT' # assign 
    t.lexer.begin('INITIAL') # go back to initial state 
    return t

# error 
def t_content_error(t):
    print(f"[content] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

 
lexer = lex.lex()


# PARSER 
# CFG for sequence 
def p_sequence(p):
    '''S : DOUBLE_HYPHEN CONTENT'''
    p[0] = p[2] # (?)

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

# parser build 
parser = yacc.yacc()

# MAIN
while True:
    try:
        data = input("Enter Single Line: ")
    except EOFError:
        print("\nExiting.")
        break
    
    if not data:
        continue

    parsed = parser.parse(data, lexer=lexer) # parse wrt to lexer 
    if parsed is not None:
        print("Accepted")
        ch = input("Do you want to continue?")
        if ch not in ['y','Y']: 
            break
        else:
            continue

