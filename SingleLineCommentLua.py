import ply.lex as lex 
import ply.yacc as yacc

# List of token names. This is always required
tokens = ('HYPHEN')

# Regular expression rules for simple tokens
t = r'-'


# Error handling rule
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# Building the lexer
lexer = lex.lex()

def p_sequence(p):
    '''S : A S B
    | A B '''

# Error rule for syntax errors
def p_error(p):
    print("Syntax error")
    exit(1)
# Build the parser
parser = yacc.yacc()

while True:
    data = input("Enter a^n b^n sequence (e.g., 'aaabbb'): ")
    lexer.input(data)
    parsed = parser.parse(data)
    if parsed == None:
        print("Accepted")