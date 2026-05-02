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

class NodeKind(Enum):
    DeclK = 0
    StmtK = 1
    ExpK = 2

class DeclKind(Enum):
    VarK = 0
    FunK = 1
    ParamK = 2

class StmtKind(Enum):
    CompoundK = 0
    IfK = 1
    WhileK = 2
    ReturnK = 3

class ExpKind(Enum):
    AssignK = 0
    IdK = 1
    OpK = 2
    ConstK = 3
    CallK = 4

MAXCHILDREN = 3

class TreeNode:
    def __init__(self):
        self.child = [None] * MAXCHILDREN
        self.sibling = None

        self.nodekind = None
        self.decl = None
        self.stmt = None
        self.exp = None

        self.name = None
        self.type = None
        self.val = None
        self.op = None
        self.size = None
        self.nextline = None