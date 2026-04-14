from enum import Enum

# Contiene todos los tokens que se requieren con sus valores
class TokenType(Enum):
    ENDFILE = 300
    ERROR = 301
   
    # Reserved Words 
    IF = 'if'
    ELSE = 'else'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'

    # Specials Symbols.

    PLUS = '+'
    MINUS = '-'
    TIMES = '*'
    OVER = '/'
    LT = '<'
    LTEQ = '<='
    RT = '>'
    RTEQ = '>='
    EQ = '=='
    NEQ = '!='
    ASSIGN = '='
    SEMI = ';'
    COMMA = ','
    LPAREN = '('
    RPAREN = ')'
    LBRACKET = '['
    RBRACKET = ']'
    LBRACE = '{'
    RBRACE= '}'

    # El lexer ignora los comentarios
    LCOMMENT = '/*'
    RCOMMENT = '*/'

    # Others:
    ID = 310
    NUM = 311
    
# StateType
class StateType(Enum):
    START = 0
    INID = 1 # letras
    INNUM = 2 # números 
    DEAD = 3 # estado muerto = error
    DONE = 4 # FINAL 

class ReservedWords(Enum):
    IF = 'if'
    ELSE = 'else'
    INT = 'int'
    RETURN = 'return'
    VOID = 'void'
    WHILE = 'while'