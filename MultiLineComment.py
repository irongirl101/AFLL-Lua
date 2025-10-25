import ply.lex as lex
import ply.yacc as yacc

# states
# We use an exclusive 'comment' state to handle multi-line content
states = (
    ('comment', 'exclusive'),
)


tokens = ('MULTILINE_START', 'MULTILINE_CONTENT', 'MULTILINE_END')


def t_INITIAL_MULTILINE_START(t):
    r'--\[\['
    t.type = 'MULTILINE_START'
    t.lexer.begin('comment')
    return t

def t_INITIAL_error(t):
    print(f"[INITIAL] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

def t_comment_MULTILINE_CONTENT(t):
    r'(.|\n)+?(?=\]\])'  
    t.type = 'MULTILINE_CONTENT'
    return t

def t_comment_MULTILINE_END(t):
    r'\]\]'
    t.type = 'MULTILINE_END'
    t.lexer.begin('INITIAL')
    return t

def t_comment_error(t):
    print(f"[comment] Illegal character '{t.value[0]}' on line {t.lexer.lineno}")
    t.lexer.skip(1)

lexer = lex.lex()

def p_multiline_comment(p):
    '''S : MULTILINE_START MULTILINE_CONTENT MULTILINE_END'''
    p[0] = p[2] 

def p_error(p):
    if p:
        print(f"Syntax error at token {p.type} ('{p.value}')")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()


print("Enter a multi-line comment (e.g., --[[ ... ]]). Press Ctrl+D (or Ctrl+Z on Windows) to exit.")

lines = []
while True:
    line = input()
    lines.append(line)
    if ']]' in line:
        break

data = '\n'.join(lines)  
parsed = parser.parse(data, lexer=lexer)
if parsed is not None:
    print("Accepted. Comment content:")
    print(parsed)