# Lua Operators Parser 
#importing lexer and parser
import ply.lex as lex
import ply.yacc as yacc

#defining the list of tokens
tokens = (
    'NUMBER', 'IDENTIFIER',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'POWER',
    'LPAREN', 'RPAREN'
)
#regular expressions for the above given token(excluding number and identifier)
t_PLUS   = r'\+'
t_MINUS  = r'-'
t_TIMES  = r'\*'
t_DIVIDE = r'/'
t_POWER  = r'\^'
t_LPAREN = r'\('
t_RPAREN = r'\)'

#to ignore spaces and tabs
t_ignore = ' \t'

#token for numbers (float datatype)
def t_NUMBER(t):
    #match the numbers entered to the given specifications below(decimal point is optional as the data entered is per user discretion)
    r'\d+(\.\d+)?'
    #convert the value to float datatype
    t.value = float(t.value)
    # return token object
    return t

#token for identifiers/variables
def t_IDENTIFIER(t):
    #match strings with the grammar
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t
#error handling function    
def t_error(t):
    # Stop parsing on illegal character and display it's position
    print(f"Illegal character '{t.value[0]}' at position {t.lexpos}")
    #skip  the character
    t.lexer.skip(1)
    #raise syntax error
    raise SyntaxError(f"Illegal character '{t.value[0]}'")      

#build lexer
lexer = lex.lex()

#Define operator precedence
precedence = (
    ('right', 'POWER'),           # power operator has right associativity
    ('left', 'TIMES', 'DIVIDE'),  # multiplication and division have same precedence
    ('left', 'PLUS', 'MINUS'),    # addition and subtraction have lowest precedence
)

#parsing for addition and subtraction operations
def p_expression_plus_minus(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    
    # if '+' operator is present, addition is to be done
    if p[2] == '+': p[0] = p[1] + p[3]
     # if '-' operator is present, subtraction is to be done
    else: p[0] = p[1] - p[3]

#parsing for simple expression
def p_expression_term(p):
    'expression : term'
    # pass the value of term to expression
    p[0] = p[1]

#parsing for multiplication and division
def p_term_times_divide(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    # if '*' operator is present, multiplication is to be done
    if p[2] == '*': p[0] = p[1] * p[3]
    # if '/' operator is present, division is to be done
    else: p[0] = p[1] / p[3]

#parsing for when the user enters only one factor(number)
def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

#parsing for exponential operation(^ in LUA)
def p_factor_power(p):
    'factor : base POWER factor'
    p[0] = p[1] ** p[3]

#parsing for a factor(number) that is just a base
def p_factor_base(p):
    'factor : base'
    #assigning base value 1 to factor
    p[0] = p[1]
#parsing for single number input
def p_base_number(p):
    'base : NUMBER'
    #assigning numerical value to the base
    p[0] = p[1]

#parsing for variables
def p_base_identifier(p):
    'base : IDENTIFIER'
    p[0] = 0
    #note for user that identifiers are assumed to be 0
    print(f"Note: '{p[1]}' treated as 0 for evaluation")

#parsing for expressions inside parenthisis
def p_base_parens(p):
    'base : LPAREN expression RPAREN'
    p[0] = p[2]

#error handling for parser errors
def p_error(p):
    if p:
        raise SyntaxError(f"Syntax error near '{p.value}' at position {p.lexpos}")
    else:
        raise SyntaxError("Syntax error at EOF")
#building parser
parser = yacc.yacc()


print("Operators Parser (supports + - * / ^ and parentheses)")
# infinite loop for taking continuous user input
while True:
    try:
        #prompt user for input
        s = input("\nEnter expression (or 'exit' to quit): ")
    except EOFError:
        break
    #exit condition
    if not s or s.lower() == 'exit':
        break
    try:
        #parsing entered expression
        result = parser.parse(s)
        print("Valid Expression")
        print("Result:", result)
        #catch errors and display error message
    except SyntaxError as e:
        print("Invalid Expression:", e)
    except Exception as e:
        print("Unexpected Error:", e)