from globalTypes import*

#print(TokenType.KALTXI)
#print(TokenType.FRAPO)
fileName = "prueba"
file = open(fileName + '' , '')
prog = file.read()
long = len(prog)
program = prog + '$'
pos = 0


class getToken(imprime = True):


globales(prog, pos, long) 


token,tokenString, _ = getToken()
while (token != TokenType.ENDFILE):
    token, tokenString,_ = getToken()
