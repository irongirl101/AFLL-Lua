# importing lexer and parser 
import ply.lex as lex
import ply.yacc as yacc

# states
# We use an exclusive 'comment' state to handle multi-line content
states = (
    ('comment', 'exclusive'),
)
# multiline starts with --[[ end with ]]
tokens = ('MULTILINE_START', 'MULTILINE_CONTENT', 'MULTILINE_END')

def t_INITIAL_MULTILINE_START(t):
    r'--\[\[' # /-> for next line 
    t.type = 'MULTILINE_START' #  assigning token to --[[
    t.lexer.begin('comment') # once assigned, change the lexer begin to the comment state. 
    return t

# if does not pass, error
def t_INITIAL_error(t):
    print(f"[INITIAL] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

# content 
def t_comment_MULTILINE_CONTENT(t):
    r'(.|\n)+?(?=\]\])'   # moving to next line, taking into account multiline inputs 
    t.type = 'MULTILINE_CONTENT' # assign content to token
    return t

# ending multiline ]]
def t_comment_MULTILINE_END(t):
    r'\]\]'
    t.type = 'MULTILINE_END' # assigning type to MULTILINE END 
    t.lexer.begin('INITIAL') # state goes back to initial (for the next inputs?)
    return t
#error handling 
def t_comment_error(t):
    print(f"[comment] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)
#bulding lexer 
lexer = lex.lex()

#Parser 
def p_multiline_comment(p):
    '''S : MULTILINE_START MULTILINE_CONTENT MULTILINE_END''' # CFG 
    p[0] = p[2] # multiple lines 

# error in parsing 
def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

#parser 
parser = yacc.yacc()

print("Enter a multi-line comment (e.g., --[[ ... ]]).")
while True:
    lines = [] # adding all comment lines 
    while True:
        line = input()
        if line.strip().lower() == 'exit':
            exit()  # exits the whole program immediately
        lines.append(line)
        if ']]' in line:
            break

    data = '\n'.join(lines)  
    parsed = parser.parse(data, lexer=lexer)
    if parsed is not None:
        print("Accepted. Comment content:")
        print(parsed)
    else:
        print("Not accepted")
