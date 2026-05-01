"""
    1. program -> declaration-list
    2. declaration-list -> declaration-list declaration | declaration
    3. declaration -> var-declaration | fun-declaration
    4. var_declaration -> type-specifier ID; | type-specifier ID [NUM] ; 
    5. type-specifier -> int | void
    6. fun-declaration -> type-specifier ID (params) compound-stmt
    7. params -> param-list | void
    8. param-list -> param-list, param | param
    9. param -> type-specifier ID | type-specifier ID []
    10. compound-stmt -> { local-declarations statement-list}
    11. local-declarations -> local-declarations var-declaration | empty
    12. statement-list -> statement-list statement | empty
    13. statement -> expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
    14. expression-stmt -> expression ;|;
    15. selection-stmt -> if (expression) statement| if (expression) statement else statement
    16. iteration-stmt -> while (expression) statement ;
    17. return-stmt -> return ; | return expression;
    18. expression -> var = expression | simple-expression
    19. var -> ID | ID [expression]
    20. simple-expression -> addictive-expression relop additive-expression | additive-expression
    21. relop -> <= | < | > | >= | == | !=
    22. additive-expression -> additive-expression addop term | term 
    23. addop -> +|-
    24. term -> term mulop factor | factor
    25. mulop -> *|/
    26. factor (expression) | var | call | NUM
    27. call -> ID (args)
    28. args -> arg-list | empty
    29. arg-list -> arg-list, expression | expression 

"""

from globalTypes import *
from globalTypes import TreeNode

global token, tokenString

def match(expected):
    global token, tokenString, nextline
    
    if (token == expected):
        #token, tokenString, nextline = getToken(imprimeScanner)
        return 
    else:
        SyntaxError("unexpected token -> ")
        print(token,tokenString)
        #print("      ")

def program():
    t =  declaration_list()
    # if token != TokenType.ENDFILE:
    #     SyntaxError("Code ends before file")
    return t

def declaration_list():
        t = declaration()
        p = t  # puntero auxiliar
        while token != TokenType.ENDFILE:
            q = declaration() # nuevo nodo leído

            if q is not None: # Si creó un nodo válido
                if t is None:
                     t = p = q # Si no existe un nodo inicial, crea el primer nodo de la lista
                else: # Si ya existe una lista, el nuevo nodo al final de la lista
                     p.sibling = q # conecta el nodo con el q 
                     p = q  # mueve al último node
        return t # cabeza de la lista

def type_specifier():
    if token == TokenType.INT:
        match(TokenType.INT)
        return TokenType.INT

    elif token == TokenType.VOID:
        match(TokenType.VOID)
        return TokenType.VOID
    
    else:
        SyntaxError("expected type specifier -> ")
        print(token, tokenString)

def declaration():
    type_v = type_specifier()
    var = tokenString
    match(TokenType.ID)

    # var_declaration
    if token == TokenType.SEMI:
        t = newDeclNode(DeclKind.Vark)

        t.type = type_v
        t.name = var
        match(TokenType.SEMI)
        return t
    
    elif token == TokenType.LBRACKET:
        t = newDeclNode(DeclKind.Vark)
        t.type = type_v
        t.name = var
        match(TokenType.LBRACKET)
        match(TokenType.NUM)
        match(TokenType.RBRACKET)
        match(TokenType.SEMI)
    
    # fun-declaration
    elif token == TokenType.LBRACE:
        t = newDeclNode(DeclKind.Funk)

        t.type = type_v
        t.name = var
        match(TokenType.LPAREN)
        t.child[0] = params()
        match(TokenType.RPAREN)
        t.child[1] = compound_stmt()
        return t
    
    else:
        SyntaxError("expected ';' or '[' or '(' after a declaration")
    #match(TokenType.ID)

def params():
    if t ==(): # hmmmmmm
    
    elif token == TokenType.VOID:
        match(TokenType.VOID)
        return TokenType.VOID

def param_list():
        t = param()
        p = t  # puntero auxiliar
        while token != TokenType.ENDFILE:
            q = param() # nuevo nodo leído

            if q is not None: # Si creó un nodo válido
                if t is None:
                    t = p = q # Si no existe un nodo inicial, crea el primer nodo de la lista
                else: 
                    p.sibling = q  
                    p = q  
        return t  

def param():
    type_v = type_specifier()
    var = tokenString
    t = newDeclNode(DeclKind.VarK)
    match(TokenType.ID)

    if token == TokenType.LBRACKET:
        t.type = type_v
        t.name = var
        match(TokenType.LBRACKET)
        # match() 
        match(TokenType.RBRACKET)
    
    else:
        SyntaxError("expected '(' after a declaration")

    return t


def compound_stmt():
    match(TokenType.LBRACKET)
    t.child[0] = local_declaration()
    t.child[1] = statement_list()
    match(TokenType.RBRACKET) 
    return t

def local_declaration():

def statement_list():

# Function newStmtNode creates a new statement
# node for syntax tree construction
# node for syntax tree construction     
def newDeclNode(kind):
    t = TreeNode();
    if (t==None):
        print("Out of memory error at line " + nextline)
    else:
        #for i in range(MAXCHILDREN):
        #    t.child[i] = None
        #t.sibling = None
        t.nodekind = NodeKind.DeclK
        t.decl = kind
        t.nextline = nextline
    return t



# Function newExpNode creates a new expression 
# node for syntax tree construction
def newStmtNode(kind):
    t = TreeNode();
    if (t==None):
        print("Out of memory error at line " + nextline)
    else:
        #for i in range(MAXCHILDREN):
        #    t.child[i] = None
        #t.sibling = None
        t.nodekind = NodeKind.StmtK
        t.stmt = kind
        t.nextline = nextline
    return t

# Function newExpNode creates a new expression 
# node for syntax tree construction
def newExpNode(kind):
    t = TreeNode()
    if (t==None):
        print("Out of memory error at line " + nextline)
    else:
        #for i in range(MAXCHILDREN):
        #    t.child[i] = None
        #t.sibling = None
        t.nodekind = NodeKind.ExpK
        t.exp = kind
        t.nextline = nextline
#        t.type = ExpType.Void
    return t

def parse(imprime = True):
    global token, tokenString, nextline
    #token, tokenString, nextline = getToken(imprimeScanner)
    t = program()
    if (token != TokenType.ENDFILE):
        SyntaxError("Code ends before file\n")
#    if imprime:
 #       printTree(t)
    return t, #Error

