import ast

def create_tree(formula):
    def recurse(node, temp):
        if isinstance(node, ast.BinOp):
            if isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
                temp.append(['('])
            if isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult):
                temp.append(['('])
            recurse(node.left, temp)
            recurse(node.op, temp)
            recurse(node.right, temp)
            if isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult):
                temp.append([')'])
            if isinstance(node.op, ast.Add) or isinstance(node.op, ast.Sub):
                temp.append([')'])
        elif isinstance(node, ast.Add):
            temp.append(['+'])
        elif isinstance(node, ast.Sub):
            temp.append(['-'])
        elif isinstance(node, ast.Mult):
            temp.append(['*'])
        elif isinstance(node, ast.Div):
            temp.append(['/'])
        elif isinstance(node, ast.Num):
            temp.append([str(node.n)])
        elif isinstance(node, ast.Name):
            temp.append([node.id])
        else:
            for child in ast.iter_child_nodes(node):
                recurse(child, temp)
                return temp
    temp = []        
    if formula is not None:
        recurse(formula, temp)
    return temp

def clean_formula(formula):
    def recurs_clean(node, temp):
        if isinstance(node, ast.BinOp):

            if isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult):
                if not isinstance(node.left, ast.Num) and not isinstance(node.left, ast.Name):
                    temp.append(['('])
                    
            elif isinstance(node.op, ast.Sub):
                if '-' in ''.join([i[0] for i in create_tree(node.left)]):
                    pass
                elif '-' in ''.join([i[0] for i in create_tree(node.right)]):
                    temp.append(['('])
                else:
                    pass
                    
            recurs_clean(node.left, temp)
            
            if isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult):
                if not isinstance(node.left, ast.Num) and not isinstance(node.left, ast.Name):
                    temp.append([')'])

            recurs_clean(node.op, temp)

            if isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult):
                if not isinstance(node.right, ast.Num) and not isinstance(node.right, ast.Name):
                    temp.append(['('])
                    
            recurs_clean(node.right, temp)
            
            if isinstance(node.op, ast.Div) or isinstance(node.op, ast.Mult):
                if not isinstance(node.right, ast.Num) and not isinstance(node.right, ast.Name):
                    temp.append([')'])
                    
            elif isinstance(node.op, ast.Sub):
                if '-' in ''.join([i[0] for i in create_tree(node.left)]):
                    pass
                elif '-' in ''.join([i[0] for i in create_tree(node.right)]):
                    temp.append(['('])
                else:
                    pass
                
        elif isinstance(node, ast.Add):
            temp.append(['+'])
        elif isinstance(node, ast.Sub):
            temp.append(['-'])
        elif isinstance(node, ast.Mult):
            temp.append(['*'])
        elif isinstance(node, ast.Div):
            temp.append(['/'])
        elif isinstance(node, ast.Num):
            temp.append([str(node.n)])
        elif isinstance(node, ast.Name):
            temp.append([node.id])
        else:
            for child in ast.iter_child_nodes(node):
                recurs_clean(child, temp)
                return temp

    return ''.join([i[0] for i in recurs_clean(ast.parse(formula, mode='eval'), [])])


def simplify(node, arr, function = None):
    if isinstance(node,dict):
        if node == {}:
            arr.append(['Null'])
        for key in node.keys():
            simplify(node[key], arr, key)
    elif isinstance(node,list) and not function:
        for item in node:
            simplify(item, arr)
    elif isinstance(node,list):
        
        if function in ['nvl', 'round', 'to_number']:
            simplify(node[0], arr)
            
        elif function == 'mul':
            arr.append(['('])
            for i, k in enumerate(node):
                simplify(k, arr)
                if i< len(node) -1:
                    arr.append(['*'])
            arr.append([')'])
            
        elif function == 'div':
            arr.append(['('])
            simplify(node[0], arr)
            arr.append(['/'])
            simplify(node[1], arr)
            arr.append([')'])
            
        elif function == 'sum' or function == 'add':
            arr.append(['('])
            for i, k in enumerate(node):
                simplify(k, arr)
                if i< len(node) -1:
                    arr.append(['+'])
            arr.append([')'])
            
        elif function == 'sub':
            arr.append(['('])
            for i, k in enumerate(node):
                simplify(k, arr)
                if i< len(node) -1:
                    arr.append(['-'])
            arr.append([')'])
                
        elif function.lower() == 'onlinestat.f_dev':
            arr.append(['('])
            simplify(node[0], arr)
            arr.append(['/'])
            simplify(node[1], arr)
            arr.append([')'])
  
            
    elif isinstance(node,str) or isinstance(node,int) or isinstance(node,float):
        arr.append([str(node)])
    else:
        pass
    return arr
