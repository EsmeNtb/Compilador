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

    if token == TokenType.SEMI or token == TokenType.LBRACKET:
        return var_declaration(type_v, var)

    elif token == TokenType.LPAREN:
        return fun_declaration(type_v, var)
    
    else:
        SyntaxError("expected ';' or '[' or '(' after a declaration")
        return None
    
def var_declaration(type_v,var):
    
    if token == TokenType.SEMI:
        t = newDeclNode(DeclKind.VarK)
        t.type = type_v
        t.name = var

        match(TokenType.SEMI)
        return t
    
    elif token == TokenType.LBRACKET:
        t = newDeclNode(DeclKind.VarK)
        t.type = type_v
        t.name = var

        match(TokenType.LBRACKET)
        match(TokenType.NUM)
        match(TokenType.RBRACKET)
        match(TokenType.SEMI)
        return t
    else:
        SyntaxError("expected ';' or '[' after a declaration")
        return None

def fun_declaration(type_v, var):
    t = newDeclNode(DeclKind.FunK)
    t.type = type_v
    t.name = var

    match(TokenType.LPAREN)
    t.child[0] = params()
    match(TokenType.RPAREN)
    t.child[1] = compound_stmt()
    return t
    
    
def params():
    if token == TokenType.VOID:
        match(TokenType.VOID)
        return None
    else:
        return param_list()

def param_list():
        t = param()
        p = t  # puntero auxiliar

        while token == TokenType.COMMA:
            match(TokenType.COMMA)
            q = param() 

            if q is not None: # Si creó un nodo válido
                p.sibling = q  
                p = q  

        return t  

def param():
    type_v = type_specifier()
    var = tokenString
    match(TokenType.ID)

    t = newDeclNode(DeclKind.ParamK)
    t.type = type_v
    t.name = var    

    if token == TokenType.LBRACKET:

        match(TokenType.LBRACKET)
        # match() 
        match(TokenType.RBRACKET)
    return t


def compound_stmt():
    t = newStmtNode(StmtKind.CompoundK)
    match(TokenType.LBRACE)
    t.child[0] = local_declarations()
    t.child[1] = statement_list()
    match(TokenType.RBRACE) 
    return t

def local_declarations():
    t = None
    p = None

    while token == TokenType.INT or token == TokenType.VOID:
        type_v = type_specifier()
        var = tokenString
        q = var_declaration(type_v,var)

        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q

    return t

def statement_list():
    t = None
    p = None

    while token == TokenType.INT or token == TokenType.VOID:
        type_v = type_specifier()
        var = tokenString
        q = statament(type_v,var)

        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q

    return t

def statament():
    if token == TokenType.ID:
        t = expression_stmt()
    elif token == TokenType.LBRACE:
        t = compound_stmt()
    elif token == TokenType.IF:
        t = selection_stmt()
    elif token == TokenType.WHILE:
        t = iteration_stmt()
    elif token == TokenType.RETURN:
        t = return_stmt()


def expression_stmt():
    if ():
        match(TokenType.SEMI)
    elif token == TokenType.SEMI:
        match(TokenType.SEMI)
    else:
        SyntaxError("")

def selection_stmt():
    match(TokenType.IF)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    t.child[1] = statament()

    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        t = statament()
    else:
        SyntaxError("expected else after a declaration")
        

def iteration_stmt():
    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    t.child[1] = statament()
    return t

def return_stmt():
    match(TokenType.RETURN)
    if token == TokenType.SEMI:
        match(TokenType.SEMI)
    elif token == TokenType.ID:
        t = expression()
        match(TokenType.SEMI)
    else:
        SyntaxError("")

def expression():
    signs = (TokenType.LTEQ or TokenType.LT or TokenType.RT
             or TokenType.RTEQ or TokenType.EQ or TokenType.NEQ)
    
    if token == TokenType.ID:
        t.child[0] = var()
        match(TokenType.ASSIGN)
        t.child[1] = expression()
    elif token == signs or token == TokenType.PLUS or token == TokenType.MINUS:
        t = simple_expression()
    else:
        SyntaxError("")

def var():
    type_v = type_specifier()
    vari = tokenString
    match(TokenType.ID)
    t = newDeclNode(DeclKind.VarK)
    t.type = type_v
    t.name = vari
    
    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        t = expression()
        match(TokenType.RBRACKET)
        return t
    
    else:
        SyntaxError()

def simple_expression():
    signs = (TokenType.LTEQ or TokenType.LT or TokenType.RT
             or TokenType.RTEQ or TokenType.EQ or TokenType.NEQ)
    if token == signs:
        t = additive_expression()
    elif token ==TokenType.PLUS or token == TokenType.MINUS:
        t = additive_expression()
    else:
        SyntaxError("")

def relop():
    if token ==  TokenType.LTEQ:
        match(TokenType.LTEQ)
    elif token == TokenType.LT:
        match(TokenType.LT)
    elif token == TokenType.RL:
        match(TokenType.RL)
    elif token == TokenType.RTEQ:
        match(TokenType.RTEQ)
    elif token == TokenType.EQ:
        match(TokenType.EQ)
    elif token == TokenType.NEQ:
        match(TokenType.NEQ)
    else:
        SyntaxError("expected '<=' | '<' | '>' | '>=' | '==' | '!=' after a declaration")

def additive_expression():
    if token == TokenType.PLUS or token == TokenType.MINUS:
        t.child[0] = addop()
        t.child[1] = term()
    elif token == TokenType.TIMES or token == TokenType.OVER:
        t = term()
    else:
        SyntaxError("expected '+' | '-' | '*' | '/' after a declaration")


def addop():
    if token == TokenType.PLUS:
        match(TokenType.PLUS)
    elif token == TokenType.MINUS:
        match(TokenType.MINUS)
    else:
        SyntaxError("expected '+' or '-' after a declaration")

def term():
    if token == TokenType.TIMES or token == TokenType.OVER:
        t = factor()
    elif token == TokenType.LBRACE:
        t = factor()
    else:
        SyntaxError("expected '*' | '/'  | '(' after a declaration")

def mulop():
    if token == TokenType.TIMES:
        match(TokenType.TIMES)
    elif token == TokenType.OVER:
        match(TokenType.OVER)
    else:
        SyntaxError("expected '*' or '/' after a declaration")
    
def factor():
    if token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = expression()
        match(TokenType.RPAREN)
    elif token == TokenType.ID:
        t = var()
    elif token == TokenType.ID and token == TokenType.LPAREN:
        t = call()
    elif token == TokenType.NUM:
        match(TokenType.NUM)
    return t 

def call():
    if token == TokenType.ID:
        match(TokenType.ID)
        match(TokenType.LPAREN)
        t = args()
        match(TokenType.RPAREN)
    else:
        SyntaxError("expected ID after declaration")

def args():
    t = None
    p = None

    while token == TokenType.COMMA:
        q = arg_list()

        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q

    return t

def arg_list():
        t = expression()
        p = t  # puntero auxiliar

        while token == TokenType.COMMA:
            match(TokenType.COMMA)
            q = expression() 

            if q is not None: # Si creó un nodo válido
                p.sibling = q  
                p = q  

        return t  

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

