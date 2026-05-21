# Hash table
BucketList = {}

def st_insert(name, kind, type_v=None, node=None, scope='global'):
    """
    Insert an identifier into the symbol table.

    name   = identifier name
    kind   = 'var', 'fun' or 'param'
    type_v = TokenType.INT or TokenType.VOID
    node   = AST node where it was declared
    scope  = scope name, initially 'global'
    """

    key = (scope, name)

    if key in BucketList:
        return False

    BucketList[key] = {
        'name': name,
        'kind': kind,
        'type_v': type_v,
        'node': node,
        'scope': scope
    }

    return True


def st_lookup(name, scope='global'):
    """
    Looks up an identifier in the current scope.
    """
    key = (scope, name)

    if key in BucketList:
        return BucketList[key]

    return None


def st_clear():
    BucketList.clear()


def printSymbtable():
    """
    Prints a formatted listing of the symbol table content.
    """
    print("Symbol Table")
    print("-------------")
    print(f"{'Scope':15} {'Name':15} {'Kind':10} {'Type':10}")
    print("-" * 55)

    for key in BucketList:
        entry = BucketList[key]
        type_name = entry['type_v'].name if entry['type_v'] is not None else "None"
        print(f"{entry['scope']:15} {entry['name']:15} {entry['kind']:10} {type_name:10}")