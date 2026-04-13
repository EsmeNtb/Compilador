from globalTypes import *

def globales(prog, pos, long):
    global programa, posicion, progLong

    programa = prog
    posicion = pos 
    progLong = long

def reservedLookup(s):
    for word in ReservedWords:
        if word.value == s:
            return TokenType[word.name]
        
    return TokenType.ID

def line_colum_error(programa,pos):
    line_num = 1
    initial_line = 0

    for i in range (pos):
        if programa[i] == '\n':
            line_num += 1
            initial_line = i + 1
        
    last_line = pos
    
    while last_line < len(programa) and programa[last_line] not in '\n$':
        last_line += 1
    
    tex_line = programa[initial_line:last_line]
    colum = pos - initial_line

    return line_num,tex_line, colum

def printError(tipeError, pos):
    global programa
    line_num, tex_line, colum = line_colum_error(programa,pos)
    
    print(f"Línea {line_num}: Error {tipeError}:")
    print(tex_line)
    print(' ' * colum + '^')

def getToken(imprime = True):
    global programa, posicion, progLong
    estado = StateType.START
    tokenString = ""
    currentState = None
    token = None
    tabla = [
        # Letra             Digito          Simbolo              Blanco       EOF             OTRO
        [StateType.INID, StateType.INNUM, StateType.DONE, StateType.START,  StateType.DONE, StateType.DONE], #START
        [StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE], # INASSIGN
        [StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE], # INCOMMENT
        [StateType.DONE, StateType.INNUM, StateType.DONE, StateType.DONE,StateType.DONE, StateType.DONE], # INNUM
        [StateType.INID, StateType.INID, StateType.DONE, StateType.DONE, StateType.DONE,StateType.DONE],  # INID
        [StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE, StateType.DONE], # DONE
    ]

    while True : 
        c = programa[posicion]

        if c.isalpha(): # Letter
            col = 0
        elif c.isdigit(): # Digit
            col = 1
        elif c in ":+-();%,.'~&!<>*": # Symbol
            col = 2
        elif c in ' \t\n': # Space
            col = 3
        elif c == '$': # EOF
            col = 4
        else:
            col = 5 # Other

        currentState = tabla[estado.value][col]

        if estado == StateType.INID and currentState == StateType.DONE:
            token = reservedLookup(tokenString)

            if imprime:
                print(token, '=', tokenString)
            
            return token, tokenString
        
        elif estado == StateType.INNUM and currentState == StateType.DONE:
            if c.isalpha():
                initial_error = posicion - len(tokenString)

                while posicion < len(programa) and (programa[posicion].isalpha() or programa[posicion].isdigit()):
                    tokenString += programa[posicion]
                    posicion += 1
                
                token = TokenType.ERROR

                if imprime:
                    print(token, '=', tokenString)
                    printError("la formación de un entero", initial_error)
                
                return token,tokenString
            
            token = TokenType.NUM

            if imprime:
                print(token, '=', tokenString)

            return token, tokenString
        
        elif estado == StateType.START and currentState == StateType.DONE:
            tokenString = c

            if c == ':' and posicion + 1 < len(programa) and programa[posicion + 1] == '=':
                tokenString = ':='
                token = TokenType.ASSIGN
                posicion += 2

            else:
                tokenString = c
                
                if c == '+':
                    token = TokenType.PLUS
                elif c == '-':
                    token = TokenType.MINUS
                elif c == '(':
                    token = TokenType.LPAREN
                elif c == ')':
                    token = TokenType.RPAREN
                elif c == ';':
                    token = TokenType.SEMI
                elif c == ',':
                    token = TokenType.COMMA
                elif c == '%':
                    token = TokenType.PERCENT
                elif c == '.':
                    token = TokenType.DOT
                elif c == "'":
                    token = TokenType.QUOTE
                elif c == '~':
                    token = TokenType.TILDE
                elif c == '&':
                    token = TokenType.AMPERSAND
                elif c == '!':
                    token = TokenType.EXCLAMATION
                elif c == '<':
                    token = TokenType.LT
                elif c == '>':
                    token = TokenType.RT
                elif c == '*':
                    token = TokenType.TIMES
                elif c == '$':
                    token = TokenType.ENDFILE
                else:
                    token = TokenType.ERROR

                posicion += 1

            if imprime:
                print(token, '=', tokenString)
            return token, tokenString
        
        elif currentState == StateType.DONE and col == 5:
            token = TokenType.ERROR
            tokenString = c

            if imprime:
                print(token, '=', tokenString)
                printError('en la formación del token', posicion)

            posicion += 1
            return token, tokenString
        
        elif estado == StateType.START and currentState == StateType.START:
            posicion += 1

        else: 
            tokenString += c 
            posicion += 1
            estado = currentState
    
    return TokenType.ERROR, tokenString
