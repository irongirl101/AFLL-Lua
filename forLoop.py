# importing lexer and parser 
import ply.lex as lex
import ply.yacc as yacc
# tokens for a numeric for loop  
# for int i = x,y 
tokens = ('FOR', 'IDENTIFIER', 'EQUAL', 'NUMBER', 'COMMA')

# do not allow an identifier be FOR 
reserved = {
    'for': 'FOR'
}
t_COMMA = r','
t_EQUAL = r'='
t_ignore = ' \t'


# an identifier can be anything as long as its not for 
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*' # it could be i, i9, _ etc etc -> a variable 
    if t.value in reserved: # checking if r is in reserved, then go to that token. 
        t.type = reserved[t.value]
    return t
 
# tokenizing integer values 
def t_NUMBER(t):
    r'-\d+' # taking into account negative values as well 
    t.value = int(t.value)
    return t

# if any incorrect values found, throw an error. 
def t_error(t):
    print(f"Illegal character '{t.value[0]}'")
    t.lexer.skip(1)

# build lexer 
lexer = lex.lex()

# parser for for loop 
def p_loop(p):
     # CFG for the loop (we are not considering do <statement> end)
     # loops could look like for i = x
    #                        for i = x,y 
    #                        for i = x,y,z (z being step counter)
    '''loop : FOR IDENTIFIER EQUAL NUMBER COMMA NUMBER COMMA NUMBER 
            | FOR IDENTIFIER EQUAL NUMBER COMMA NUMBER  
            | FOR IDENTIFIER EQUAL NUMBER'''

# if any error
def p_error(p):
    if p:
        print(f"Syntax error near '{p.value}'")
    else:
        print("Syntax error at EOF")

# build parser 
parser = yacc.yacc()

# show user an example 
print("for Loop Parser (form: for i = n)")

# continue asking for inputs till EOF 
while True:
    try:
        data = input("Enter loop: ")
    except EOFError:
        print("\nExiting.")
        break

    if not data:
        print("Accepted")
        continue
    # parse the data 
    result = parser.parse(data)

