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
from lexer import *
from globalTypes import TreeNode

global token, tokenString


def match(expected):
    global token, tokenString
    
    if (token == expected):
        token, tokenString = getToken()
    else:
        syntaxisError(f"expected {expected}, got {token}")

def program():
    t =  declaration_list()
    # if token != TokenType.ENDFILE:
    #     SyntaxError("Code ends before file")
    return t

def declaration_list():
        t = declaration()
        p = t  # puntero auxiliar

        # Use of AI to understand the first sintaxis
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
        syntaxisError("expected type specifier -> ")
        print(token, tokenString)

def declaration():
    type_v = type_specifier()
    vari= tokenString
    match(TokenType.ID)

    # Use of AI for understanding the syntaxis of rule 3

    if token == TokenType.SEMI or token == TokenType.LBRACKET:
        return var_declaration(type_v, vari)

    elif token == TokenType.LPAREN:
        return fun_declaration(type_v, vari)
    
    else:
        syntaxisError("expected type specifier -> ")
        return None
    
def var_declaration(type_v,vari):
    
    if token == TokenType.SEMI:
        t = newDeclNode(DeclKind.VarK)
        t.type = type_v
        t.name = vari

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
        syntaxisError("expected ';' or '[' after a declaration")
        return None

def fun_declaration(type_v, vari):
    t = newDeclNode(DeclKind.FunK)
    t.type = type_v
    t.name = vari

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
    vari = tokenString
    match(TokenType.ID)

    t = newDeclNode(DeclKind.ParamK)
    t.type = type_v
    t.name = vari

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
    # Use of AI to understan what to do when we have empty
    t = None
    p = None

    while token == TokenType.INT or token == TokenType.VOID:
        type_v = type_specifier()
        vari = tokenString
        match(TokenType.ID)
        q = var_declaration(type_v,vari)

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

    while token in {
        TokenType.ID,
        TokenType.LBRACE,
        TokenType.IF,
        TokenType.WHILE,
        TokenType.RETURN,
        TokenType.SEMI
    }:
        q = statement()

        if q is not None:
            if t is None:
                t = p = q
            else:
                p.sibling = q
                p = q
    return t

def statement():
    if token == TokenType.ID or token == TokenType.SEMI:
        return expression_stmt()
    elif token == TokenType.LBRACE:
        return compound_stmt()
    elif token == TokenType.IF:
        return selection_stmt()
    elif token == TokenType.WHILE:
        return iteration_stmt()
    elif token == TokenType.RETURN:
        return return_stmt()
    else:
        syntaxisError("expected statement")
        return None


def expression_stmt():
    if token == TokenType.SEMI:
        match(TokenType.SEMI)
        return None
    
    else:
        t = expression()
        match(TokenType.SEMI)
        return t

def selection_stmt():
    t = newStmtNode(StmtKind.IfK)

    match(TokenType.IF)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    t.child[1] = statement()

    if token == TokenType.ELSE:
        match(TokenType.ELSE)
        t.child[2] = statement() 
    return t
        

def iteration_stmt():
    t = newStmtNode(StmtKind.WhileK)

    match(TokenType.WHILE)
    match(TokenType.LPAREN)
    t.child[0] = expression()
    match(TokenType.RPAREN)
    t.child[1] = statement()
    return t

def return_stmt():
    t = newStmtNode(StmtKind.ReturnK)

    match(TokenType.RETURN)
    if token == TokenType.SEMI:
        match(TokenType.SEMI)
    else: 
        t.child[0] = expression()
        match(TokenType.SEMI)
    return t

def expression():
    if token == TokenType.ID:
        t = var()

        if token == TokenType.ASSIGN:
            p = newExpNode(ExpKind.AssignK)
            p.child[0] = t
            match(TokenType.ASSIGN)
            p.child[1] = expression()
            return p
    else:
        return simple_expression()

def var():
    vari = tokenString
    match(TokenType.ID)
    t = newDeclNode(ExpKind.IdK)
    t.name = vari
    
    if token == TokenType.LBRACKET:
        match(TokenType.LBRACKET)
        t.child[0] = expression()
        match(TokenType.RBRACKET)
    return t

def simple_expression():
    relop_var = {
    TokenType.LTEQ,
    TokenType.LT,
    TokenType.RT,
    TokenType.RTEQ,
    TokenType.EQ,
    TokenType.NEQ
    }

    t = additive_expression()
 
    if token in relop_var:
        p = newExpNode(ExpKind.OpK)
        p. child[0] = t
        p.op = token     # Use of AI to understand that the operator must be save before it consume it by the function
        relop()
        p.child[1] = additive_expression
        t = p
    return t 

def relop():
    if token ==  TokenType.LTEQ:
        match(TokenType.LTEQ)

    elif token == TokenType.LT:
        match(TokenType.LT)

    elif token == TokenType.RT:
        match(TokenType.RT)

    elif token == TokenType.RTEQ:
        match(TokenType.RTEQ)

    elif token == TokenType.EQ:
        match(TokenType.EQ)

    elif token == TokenType.NEQ:
        match(TokenType.NEQ)

    else:
        syntaxisError("expected '<=' | '<' | '>' | '>=' | '==' | '!=' after a declaration")

def additive_expression():
    t = term()

    while token == TokenType.PLUS or token == TokenType.MINUS:
        p = newExpNode(ExpKind.OpK)
        p.child[1] = term()
        p.op = token

        addop()
        p.child[1] = term ()
        t = p
    return t

def addop():
    if token == TokenType.PLUS:
        match(TokenType.PLUS)

    elif token == TokenType.MINUS:
        match(TokenType.MINUS)

    else:
        syntaxisError("expected '+' or '-' after a declaration")

def term():
    t = factor()

    while token == TokenType.TIMES or token == TokenType.OVER:
        p = newExpNode(ExpKind.OpK)
        p.child[0] = t 
        p.op = token
        mulop()
        p.child[1] = factor()
        t = p
    return t

def mulop():
    if token == TokenType.TIMES:
        match(TokenType.TIMES)

    elif token == TokenType.OVER:
        match(TokenType.OVER)

    else:
        syntaxisError("expected '*' or '/' after a declaration")
    
def factor():
    if token == TokenType.LPAREN:
        match(TokenType.LPAREN)
        t = expression()
        match(TokenType.RPAREN)
        return t
    
    elif token == TokenType.NUM:
        t = newExpNode(ExpKind.ConstK)

        t.val = int(tokenString)
        match(TokenType.NUM)
        return t
    
    elif token == TokenType.ID:
        vari = tokenString
        match(TokenType.ID)

        if token== TokenType.LPAREN:
            t = newExpNode(ExpKind.CallK)

            t.name = vari
            match(TokenType.LPAREN)
            t.child[0] = args()
            match(TokenType.RPAREN)
            return t
        else:
            t = newExpNode(ExpKind.IdK)
            t.name = vari

            if token == TokenType.LBRACKET:
                match(TokenType.LBRACKET)
                t.child[0] = expression()
                match(TokenType.RBRACKET)

            return t
    else:
        syntaxisError("expected factor")
        return None

def call():
    if token == TokenType.ID:
        vari = tokenString
        t = newExpNode(ExpKind.CallK)
        t.name = vari

        match(TokenType.ID)
        match(TokenType.LPAREN)
        t.child[0] = args()
        match(TokenType.RPAREN)

        return t
    else:
        syntaxisError("expected ID after declaration")
        return None

# Chat
def args():
    if token == TokenType.RPAREN:
        return None
    else: return arg_list()

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

# Function newStmtNode creates a declaration
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



# Function newExpNode creates a new statement
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

def syntaxisError(message):
    global Error

    print(f"Sintáctico: {message}")
    print("Token actual: ", token, tokenString)
    Error = True


def parse(imprime = True):
    global token, tokenString, Error
    Error =  False
    token, tokenString = getToken()
    
    t = program()
    if (token != TokenType.ENDFILE):
        SyntaxError("Code ends before file\n")
#    if imprime:
 #       printTree(t)
    return t, Error

