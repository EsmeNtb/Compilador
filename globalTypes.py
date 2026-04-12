from enum import Enum

# Contiene todos los tokens que se requieren con sus valores
class TokenType(Enum):
    ENDFILE = 300
    ERROR = 301

    # Reserved words
    KALTXI = 'kaltxì' # hello
    RUTXE = 'rutxe'  # please
    IRAYO = 'irayo' # thanks
    EWLL = 'ewll' # plant
    EYLAN = 'eylan' # friend
    IPU = 'ipu' # humorous
    RRTA = 'Rrta' # Earth
    ATAN = 'atan' # light
    ATXKXE = 'atxkxe' # land
    AHO = 'aho' # pray
    EAMPIN = 'eampin' # blue | green
    EMREY= 'emrey' # survive
    EYAWR= 'eyawr' # correct
    EYKTAN = 'eyktan' # leader
    EYWA = 'Eywa'
    PANDORA = 'Pandora'
    FAHEW = 'fahew' # smell
    TAWTUTE = 'tawtute' # sky-person


    # Multicharacter tokens
    ID = 310
    NUM = 311
    STRING = 312

    # Special Symbols
    ASSIGN = ':='
    PLUS = '+'
    MINUS = '-'
    LPAREN = '('
    RPAREN = ')'
    SEMI = ';'
    COMMA = ','
    PERCENT = '%'
    AMPERSAND = '&'
    EXCLAMATION ='!'
    LT = '<'
    RT = '>'
    TIMES = '*'
    
# StateType
class StateType(Enum):
    START = 0
    INASSIGN = 1
    INCOMMENT = 2
    INNUM = 3
    INID = 4
    DONE = 5

class ReservedWords(Enum):
    KALTXI = 'kaltxì' # hello
    RUTXE = 'rutxe'  # please
    IRAYO = 'irayo' # thanks
    EWLL = 'ewll' # plant
    EYLAN = 'eylan' # friend
    IPU = 'ipu' # humorous
    RRTA = 'Rrta' # Earth
    ATAN = 'atan' # light
    ATXKXE = 'atxkxe' # land
    AHO = 'aho' # pray
    EAMPIN = 'eampin' # blue | green
    EMREY= 'emrey' # survive
    EYAWR= 'eyawr' # correct
    EYKTAN = 'eyktan' # leader
    EYWA = 'Eywa'
    PANDORA = 'Pandora'
    FAHEW = 'fahew' # smell
    TAWTUTE = 'tawtute' # sky-person
