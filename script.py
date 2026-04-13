from globalTypes import*
from lexer import * 

#print(TokenType.KALTXI)
#print(TokenType.FRAPO)

fileName = "prueba"
f = open(fileName + '.c-' , 'r')
programa = f.read()
progLong = len(programa)
programa = programa + '$'
posicion = 0

# Función para pasar los valores iniciales de las variables globales
globales(programa, posicion, progLong)

token,tokenString = getToken()
while (token != TokenType.ENDFILE):
    token, tokenString = getToken()