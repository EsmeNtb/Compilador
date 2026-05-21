from globalTypes import *
from symtab import * 


Error = False
current_fun_type = None

def semanticError(message, node=None):
    global Error
    Error = True

    if node is not None and getattr(node, "name", None) is not None:
        print(f"Error semántico: {message} -> {node.name}")
    else:
        print(f"Error semántico: {message}")

def traverse(t,preProc, postProc):
    """
        Procedure travarse is a generic recursive 
        syntax tree traversal rutine.
    """
    if t is not None:
        preProc(t)

        for i in range(MAXCHILDREN):
            traverse(t.child[i],preProc,postProc)
        postProc(t)

        traverse(t.sibling, preProc, postProc)

def null(t):
    """
        It's a do-nothing procedure to generate preorder-only
    """
    None
def tabla(tree, imprime = True):

    global Error

    st_clear()
    insert_predefined_function()

    check_program(tree)

    if imprime:
        printSymbtable()

def semantica(tree, imprime = True):
    """
        Main funtion for the semantic
        - El tree es lo que regresa el AST del parser
    """
    global Error
    Error = False
    tabla(tree,imprime)
    return Error

def insert_predefined_function():
    st_insert(
        name="input",
        kind="fun",
        type_v=TokenType.INT,
        node=None,
        scope="global"
    )

    st_insert(
        name="output",
        kind="fun",
        type_v=TokenType.VOID,
        node=None,
        scope="global"
    )

def lookfor_identifier(name, scope):
    """
        Auxiliar function
        Function to look for an identifier
    """
    entry = st_lookup(name,scope)

    if entry is not None:
        return entry
    
    return st_lookup(name, "global")

def check_program(tree):
    """
        Rule: program -> declaration-list
    """
    if tree is None:
        semanticError("The program expected at least one declaration")
        return 
    
    check_declaration_list(tree)
    check_main_last(tree) # The last declaration on the program should be a "main" funcion

def check_declaration_list(tree):
    """
        Rule:
        declaration-list -> declaration-list declaration | declaration
    """
    current = tree

    while current is not None:
        check_declaration(current)
        current = current.sibling

def check_declaration(node):
    if node.nodekind != NodeKind.DeclK:
        semanticError("Expected a declaration node", node)
        return
    
    elif node.decl == DeclKind.VarK:
        check_var_declaration(node)

    elif node.decl == DeclKind.FunK:
        check_fun_declaration(node)
    else:
        semanticError("Unknown declaraion kind", node)

def  check_main_last(tree):
    """
        Check the rule of the last declaration should be 'main'
    """
    current = tree
    while current is not None and current.sibling is not None:
        current = current.sibling

    if current is None:
        semanticError("The progam must contain a min function")
        return
    elif current.nodekind != NodeKind.DeclK or current.decl != DeclKind.FunK:
        semanticError("The last declaration must be funcion named 'main'", current)
        return
    elif current.name != 'main':
        semanticError("The last function declaration must be named 'main' " , current)


def check_var_declaration(node):
    """
        Rule 4 and 5:
        var-declaration -> type-specifier ID; | type- specifier ID [NUM] ;
        type-specifier -> int | void
    """
    if not check_type_specifier(node): # If the node hasn't a valid varaible, the program stop check that variable
        return
    
    elif not check_var_type(node): # Use AI to understrand why it's need to separate void
        return
    
    # Table symbols
    inserted = st_insert(
        name=node.name,
        kind="var",
        type_v=node.type,
        node=node,
        scope="global"
    )

    if not inserted: # Id st_insert = False, this means the name alreafy existed on the table
        semanticError(f"identifier '{node.name}' already declared in global scope", node)
        return


def check_type_specifier(node):
    if node.type != TokenType.INT and node.type != TokenType.VOID:
        semanticError("Expected 'int' or 'void'", node)
        return False
    return True

def check_var_type(node):
    """
        Semantic restringtion => VOID is for funcions, not for variables
    """
    if node.type == TokenType.VOID:
        semanticError("Variable cannot be declared as void", node)
        return False
    return True

def check_fun_declaration(node):
    """
        Rules 6-7
        fun-declaration -> type-specifier ID (params) compound-stmt
        params -> param-list | void
    """
    global current_fun_type

    if not check_type_specifier(node):
        return
    
    # Table symbols
    inserted = st_insert(
        name=node.name,
        kind="fun",
        type_v=node.type,
        node=node,
        scope="global"
    )

    if not inserted: # Id st_insert = False, this means the name alreafy existed on the table
        semanticError(f"function '{node.name}' already declared in global scope", node)
        return
    
    current_fun_type = node.type
    function_scope = node.name

    check_params(node.child[0], function_scope)
    check_compound_stmt(node.child[1], function_scope)

    current_fun_type = None


def check_params(node,scope):
    """
        Rule 7:
        params -> params-list | void

        If node is None, the function has no parameters
    """
    if node is None:
        return
    else:
        check_params_list(node, scope)

def check_params_list(node,scope):
    """"
        Rule 8:
        params-list -> param-list, param | param

        Params ares stored as a sibling list
    """
    current = node

    while current is not None:
        check_param(current, scope)
        current = current.sibling

def check_param(node, scope):
    """ 
        Rule 9:
        param -> type-specifier ID | type-specifier ID[]

        Parameters cannot be declared as void
    """
    
    if not check_type_specifier(node):
        return
    
    if node.type == TokenType.VOID:
        semanticError("Parameters cannor be declared as void", node)
        return
    
    # Table symbols
    inserted = st_insert(
        name=node.name,
        kind="param",
        type_v=node.type,
        node=node,
        scope= scope
    )

    if not inserted: 
        semanticError(f"funtion '{node.name}' already declared in function {scope}", node)
        return
    

def check_compound_stmt(node, scope):
    """
        Rule 10:
        compound-smt -> {local-declaration statement-list}

    """
    if node is None:
        semanticError("Function must have a compound statement body")
        return
    
    else:
        check_local_declaration(node.child[0],scope)
        check_statement_list(node.child[1],scope)

def check_local_declaration(node,scope):
    """
        Rule 11:
        local-declaraations -> local-decalarations var-declaration | empty

        The local-declarations can be empy
    """
    if node is None:
        return 
    
    current = node

    while current is not None:
        check_local_var_declaration(current,scope)
        current = current.sibling

def check_local_var_declaration(node,scope):
    if not check_type_specifier(node):
        return
    if not check_var_type(node):
        return
    
    # Table symbols
    inserted = st_insert(
        name=node.name,
        kind="var",
        type_v=node.type,
        node=node,
        scope= scope
    )

    if not inserted: 
        semanticError(f"identifier '{node.name}' already declared in scope {scope}", node)
        return
    

def check_statement_list(node,scope):
    """
        Rule 12:
        statement_list -> statement-list statement | empty
    """
    if node is None:
        return
    
    current = node

    while current is not None:
        check_statement(current,scope)
        current = current.sibling

def check_statement(node,scope):
    """
        Rule 13:
        statement -> expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
    """
    if node is None:
        return
    
    if node.nodekind == NodeKind.ExpK:
        check_expression(node,scope)
        return
    
    elif node.nodekind != NodeKind.StmtK:
        semanticError("Expected statement node", node)
        return
    
    elif node.stmt == StmtKind.CompoundK:
        check_compound_stmt(node,scope)
    
    elif node.stmt == StmtKind.IfK:
        check_selection_stmt(node,scope)
    
    elif node.stmt == StmtKind.WhileK:
        check_iteration_stmt(node,scope)
    
    elif node.stmt == StmtKind.ReturnK:
        check_return_stmt(node,scope)
    
    else:
        semanticError("Unknown statement kind", node)


def check_expression_stmt(node,scope):
    """

        Checks expression nodes used inside expression statement and other 
        constructs.

        Rule 14:
        expression-stmt --> expression ; |;

        The parser already consumed the semicolon. Therefore, in the AST:
        - expression ; becomes an ExpK node

        Important: 
            AI was used as conceptual support to understand that expression-stmt

    """
    if node is None:
        return
    
    check_expression(node,scope)

def check_selection_stmt(node,scope):
    """
        Rule 15:
        selection-stmt -> if (expression) statement | if (expression) statement else statement
    """

    if node is None:
        return
    
    check_expression(node.child[0],scope)
    check_statement(node.child[1],scope)
    
    if node.child[2] is not None:
        check_statement(node.child[2],scope)

def check_iteration_stmt(node,scope):
    """
        Rule 16:
        iteration-stmt = while (expression) statement
    """
    if node is None:
        return
    
    check_expression(node.child[0],scope)
    check_statement(node.child[1],scope)

def check_return_stmt(node,scope):
    """
        Rule 17:
        return stmt -> return ; | return expression;
    """
    global current_fun_type 

    if node is None:
        return
    
    if current_fun_type == TokenType.VOID:
        if node.child[0] is not None:
            semanticError("Void function should not return a value", node)

    elif current_fun_type == TokenType.INT:
        if node.child[0] is None:
            semanticError("'Int' fucntion should return a value", node)
        else:
            check_expression(node.child[0],scope)


def check_expression(node,scope):
    """
        Rule 18:
        expression -> car = expression | simple-expression
         
        * AI was used as conceptual support to understand how expression-stmt,
            assignments, variable references, operations and calls are represented
            inside the AST.
    """
    if node is None:
        return

    if node.nodekind != NodeKind.ExpK:
        semanticError("Expected expression node", node)
        return

    if node.exp == ExpKind.AssignK:
        left = node.child[0]
        right = node.child[1]

        if left is None:
            semanticError("assignment must have a left side", node)
            return
        
        if left.nodekind != NodeKind.ExpK or left.exp != ExpKind.IdK:
            semanticError("left side of assignment must be a variable", node)
            return
        
        check_expression(left, scope)
        check_expression(right, scope)

    elif node.exp == ExpKind.OpK:
        check_op(node, scope)

    elif node.exp == ExpKind.IdK:
        check_var(node, scope)

    elif node.exp == ExpKind.ConstK:
        return

    elif node.exp == ExpKind.CallK:
        check_call(node, scope)
     
    
def check_var(node,scope):
    """
        Rule 19:
        var -> ID | ID [expression]
    """
    entry = lookfor_identifier(node.name, scope) # Looks the identifier

    if entry is None:
        semanticError(f"identifier '{node.name}' was not declared", node)
        return
    
    if node.child[0] is not None:
        check_expression(node.child[0],scope)


def check_simple_expression(node, scope):
    """
        Rule 20:
        simple-expression -> additive-expression relop additivve, expression | additive-expression
    """
    if node is None:
        return

    if node.nodekind != NodeKind.ExpK or node.exp != ExpKind.OpK:
        semanticError("Expected simple expression", node)
        return

    if not check_relop(node.op):
        semanticError("Expected relational operator", node)
        return

    check_expression(node.child[0], scope)
    check_expression(node.child[1], scope)

def check_relop(op):
    """
        Rule 21:
        relop -> <= | < | > | < | >= | == | != 
    """
    return op in {
        TokenType.LTEQ,
        TokenType.LT,
        TokenType.RT,
        TokenType.RTEQ,
        TokenType.EQ,
        TokenType.NEQ
    }

def check_additive_expression(node, scope):
    """"
        Rule 22:
        additive-expression -> additive-expression addop term | term
    """
    if node is None:
        return
    
    if node.nodekind != NodeKind.ExpK or node.exp != ExpKind.OpK:
        semanticError("Expected addictive expression", node)
        return

    if not check_addop(node.op):
        semanticError("Expected additive operator '+' or '-' ", node)
        return
    
    check_expression(node.child[0],scope)
    check_expression(node.child[1],scope)

def check_addop(op):
    """
        Rule 23:
        addop -> + | -
    """
    return op in {
        TokenType.PLUS,
        TokenType.MINUS,
    }

def check_term(node, scope):
    """
        Rule 24:
        term -> term mulop factor | factor
    """
    if node is None:
        return
    
    if node.nodekind != NodeKind.ExpK or node.exp != ExpKind.OpK:
        semanticError("Expected a term expression", node)
        return
    
    if not check_mulop(node.op):
        semanticError("Expetec a mulop operator '*' or '/'", node)
        return
    
    check_expression(node.child[0],scope)
    check_expression(node.child[1],scope)


def check_mulop(op):
    """
        Rule 25:
        mulop -> * | /
    """

    return op in {
        TokenType.TIMES,
        TokenType.OVER
    }

def check_op(node,scope):
    """
        * Auxilizar function to check operatos expression

    """
    if node is None:
        return
    
    if node. nodekind != NodeKind.ExpK or node.exp != ExpKind.OpK:
        semanticError("Expected operator expression" , node)
        return

    if check_relop(node.op):
        check_simple_expression(node,scope)

    elif check_addop(node.op):
        check_additive_expression(node,scope)
    
    elif check_mulop(node.op):
        check_term(node,scope)

    else: 
        semanticError("Unkown operator", node)


def check_factor(node,scope):
    """
        Rule 26
        factor -> (expression) | var | call | NUM
    """
    if node is None:
        return
    
    if node.nodekind != NodeKind.ExpK:
        semanticError("Expected factor expression", node)
        return

    if node.exp == ExpKind.IdK:
        check_var(node, scope)

    elif node.exp == ExpKind.CallK:
        check_call(node, scope)

    elif node.exp == ExpKind.ConstK:
        return

    elif node.exp == ExpKind.OpK:
        check_op(node, scope)

    elif node.exp == ExpKind.AssignK:
        check_expression(node, scope)

    else:
        semanticError("Unknown factor kind", node)

def check_call(node, scope):
    """
        Rule 27:
        call -> ID (args)
    """
    if node is None:
        return

    if node.nodekind != NodeKind.ExpK or node.exp != ExpKind.CallK:
        semanticError("Expected function call", node)
        return

    entry = lookfor_identifier(node.name, scope)

    if entry is None:
        semanticError(f"function '{node.name}' was not declared", node)
    elif entry["kind"] != "fun":
        semanticError(f"identifier '{node.name}' is not a function", node)

    check_args(node.child[0], scope)

def check_args(node,scope):
    """
        Rule 28:
        args -> args-list | empty
    """
    if node is None:
        return
    
    check_arg_list(node,scope)
 

def check_arg_list(node, scope):
    current = node
    while current is not None:
        check_expression(current, scope)
        current = current.sibling