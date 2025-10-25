import ply.lex as lex
import ply.yacc as yacc

tokens = ('FOR','OPT','COMMA','STATEMENT','DO','END','EQUAL')

reserved={
    'for':'FOR', 
    'do': 'DO', 
    'end':'END'
}

t_COMMA = r','
t_EQUAL = r'='
t_ignore = ' \t\n'


# for i = x,y,z do statement end 


def p_loop(p): 
    '''loop '''

