from globalTypes import *

# Clasificación de Caracteres de entrada para el DFA
LETRA = 0
DIGITO = 1
SIMBOL = 2
DELIM = 3
OTRO = 4
# Posibles entradas 

""" 
    ESTADOS DE DFA
        q0 = START
        q1 = INID
        q2 = INNUM
        q3 = DEAD
        q4 = DONE
"""

tabla = [ 
# -------------------------------------------------------
# TABLA DE TRANSICIONES DEL DFA
# Filas = estados actuales
# Columnas = tipo de carácter de entrada
#
#           Letra  Digito  Simbol  Delim  Otro
# -------------------------------------------------------
    [1,     2,      4,      0,      3], #qo
    [1,     3,      4,      4,      3], #q1
    [3,     2,      4,      4,      3], #q2
    [3,     3,      3,      3,      3], #q3 (dead)
    [4,     4,      4,      4,      4] #q4 (done) 
]


def globales(prog, pos, long):
    """
       Inicializa las variables globales del analizador léxico.

    Parámetros:
        prog : string completo del programa fuente
        pos  : posición inicial de lectura
        long : longitud del programa
    """

    global programa, posicion, progLong

    programa = prog
    posicion = pos 
    progLong = long


def reservedLookup(tokenString):
    """
        Revisa si el lexema recibido es una palabra reservada.

        Si coincide con alguna palabra en ReservedWords,
        regresa el TokenType correspondiente.
        En caso contrario, se clasifica como identificador (ID).
    """

    for w in ReservedWords:
        if tokenString == w.value:
            return TokenType[w.name]
    return TokenType.ID

def tipo_char(c):
    """
    Clasifica un carácter en una de las categorías del DFA.

    Retorna:
        LETRA   si es letra
        DIGITO  si es número
        SIMBOL  si es símbolo reconocido
        DELIM   si es espacio, tab o salto de línea
        OTRO    cualquier otro carácter no válido
    """
    
    if c.isalpha():
        return LETRA
    elif c.isdigit():
        return DIGITO
    elif c in "+-*/<>=;(),[]{}":
        return SIMBOL
    elif c in " \t\n":
        return DELIM
    else:
        return OTRO

def getSymbolToken(c):
    """
    Convierte un símbolo individual en su token correspondiente.

    Ejemplo:
        '+' -> TokenType.PLUS
        '(' -> TokenType.LPAREN
    Si el símbolo no existe en el mapa, devuelve ERROR.
    """

    mapa = {
        '+': TokenType.PLUS,
        '-': TokenType.MINUS,
        '*': TokenType.TIMES,
        '/': TokenType.OVER,
        '<': TokenType.LT,
        '>': TokenType.RT,
        '=': TokenType.ASSIGN,
        ';': TokenType.SEMI,
        ',': TokenType.COMMA,
        '(': TokenType.LPAREN,
        ')': TokenType.RPAREN,
        '[': TokenType.LBRACKET,
        ']': TokenType.RBRACKET,
        '{': TokenType.LBRACE,
        '}': TokenType.RBRACE,
    }

    return mapa.get(c, TokenType.ERROR)

# Detector de la posición del error
def line_colum_error(programa,pos):
    """
    Calcula la línea, el texto de la línea y la columna
    donde ocurrió un error léxico.

    Parámetros:
        programa : código fuente completo
        pos      : posición absoluta del error

    Retorna:
        line_num : número de línea
        tex_line : contenido completo de esa línea
        colum    : columna exacta del error
    """

    line_num = 1
    initial_line = 0

    # Recorre el programa hasta la posición del error
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

# Print the error
def printError(tipeError, pos):
    """
    Imprime un mensaje de error con formato visual,
    indicando la línea y marcando con '^' el punto exacto.
    """
     
    global programa
    line_num, tex_line, colum = line_colum_error(programa,pos)
    
    print(f"Línea {line_num}: Error {tipeError}:")
    print(tex_line)
    print(' ' * colum + '^')


# Función principal del Analizador Léxico
def getToken(imprime = True):
    """
    Obtiene el siguiente token del programa fuente.

    Parámetro:
        imprime : si es True, imprime el token encontrado

    Retorna:
        (token, tokenString)
    """

    global programa, posicion, progLong 

    while posicion < len(programa):
        c = programa[posicion]

        # Fin del archivo
        if c == '$':
            token = TokenType.ENDFILE
            tokenString= '$'

            if imprime:
                print(token, '=', tokenString)
            return token,tokenString
        
        # Ignora los delimitadores
        elif c in ' \t\n':
            posicion += 1
            continue
        
         # 3. OPERADORES DE DOS CARACTERES
        elif programa[posicion:posicion+2] == '==':
            token = TokenType.EQ
            tokenString = '=='
            posicion += 2

            if imprime:
                print(token, '=', tokenString)
            return token, tokenString
        
        elif programa[posicion:posicion+2] == '!=':
            token = TokenType.NEQ
            tokenString = '!='
            posicion += 2

            if imprime:
                print(token, '=', tokenString)
            return token, tokenString
        
        elif programa[posicion:posicion+2] == '<=':
            token = TokenType.LTEQ
            tokenString = '<='
            posicion += 2

            if imprime:
                print(token, '=', tokenString)
            return token, tokenString
        
        elif programa[posicion:posicion+2] == '>=':
            token = TokenType.RTEQ
            tokenString = '>='
            posicion += 2

            if imprime:
                print(token, '=', tokenString)
            return token, tokenString
        
        # 4. MANEJO DE COMENTARIOS BLOQUE: /* ... */
        elif programa[posicion:posicion+2] == '/*':
            ini_comment = posicion
            posicion += 2

            while posicion < len(programa) -1 and programa[posicion:posicion+2] != '*/':
                posicion +=1
            
            if posicion >= len(programa) -1:
                token = TokenType.ERROR
                tokenString = '/*'
                
                if imprime:
                    print(token, '=', tokenString)
                    printError("Comentario sin cerrar", ini_comment)

                return token, tokenString
            
            posicion += 2
            continue

        # Procesamiento con el DFA
        estado = 0
        tokenString = "" # String for storing token
        start = posicion

        while posicion < len(programa):
            c = programa[posicion]

            if c ==  '$':
                col = DELIM
            else: 
                col = tipo_char(c)

            nuevoEstado = tabla[estado][col]

            if nuevoEstado == 0:
                posicion += 1
                break

            elif nuevoEstado == 1 or nuevoEstado == 2:
                tokenString += c
                estado = nuevoEstado
                posicion += 1
                continue

            elif nuevoEstado == 4:
                if estado == 0:
                    token = getSymbolToken(c)
                    tokenString = c
                    posicion += 1
                elif estado == 1:
                    token = reservedLookup(tokenString)
                elif estado == 2:
                    token = TokenType.NUM
                else:
                    token = TokenType.ERROR
                
                if imprime:
                    print(token, '=', tokenString)
                return token, tokenString

            # Estado de error léxicco
            elif nuevoEstado == 3:
                if estado == 0:
                    tokenString = c
                    posicion += 1
                
                else:
                    while posicion < len(programa) and (programa[posicion].isalpha() or programa[posicion].isdigit()):
                        tokenString += programa[posicion]
                        posicion += 1

                token = TokenType.ERROR

                if imprime:
                    print(token, '=', tokenString)
                    if tokenString and tokenString[0].isdigit():
                        printError("la formación de un entero", start)
                    else:
                        printError("en la formación del token", start)
                
                return token,tokenString
            # Cualquier otro caso inesperado
            else:
                token = TokenType.ERROR

                if imprime:
                    print(token, '=', tokenString)
                
                return token, tokenString
        
    return TokenType.ENDFILE, '$'