
#Base class for all ASTNodes
class ASTNode:

    EVAL_TYPE = {
        "int":1,
        "real":2,
        "string":3
    }


    def __init__(self,token=None):
        self.token = token


class ExpNode(ASTNode):
    def __init__(self,token=None):
        super().__init(token)
        self.eval_type = None


# Class for all binary operations
class BinOpNode(ExpNode):
    def __init__(self,token,left=None,right=None):
        super().__init__(token)
        self.right = right
        self.left = left

class UnaryOpNode(ExpNode):
    def __init__(self,token,operand=None):
        super().__init__(token)
        self.operand = operand


class IntNode(ExpNode):
    def __init__(self,token):
        super().__init__(token)
        self.eval_type =ASTNode.EVAL_TYPE["int"]


class RealNode(ExpNode):
    def __init__(self,token):
        super().__init__(token)
        self.eval_type =ASTNode.EVAL_TYPE["real"]

class StringNode(ExpNode):
    def __init__(self,token):
        super().__init__(token)
        self.eval_type =ASTNode.EVAL_TYPE["string"]

class VarRefNode(ExpNode):
    def __init__(self,token):
        super().__init__(token)

class VarDeclNode(ASTNode):
    def __init__(self,token,type=None,identifier=None):
        super().__init__(token)
        self.type = type
        self.id = identifier

class ArrayDeclNode(ASTNode):
    def __init__(self,token,type=None,size=0):
        super().__init__(token)
        self.type = type
        self.id = self.token
        self.size = 0

class AssignNode(ASTNode):
    def __init__(self,token,left=None,right=None):
        super().__init__(token)
        self.left = left
        self.right = right

class Statement(ASTNode):
    def __init__(self,token,exp=None):
        super().__init__(token)
        self.exp = exp

class FunctionCall(ExpNode):
    def __init__(self,token=None,fargs=None):
        super().__init__(token)
        self.fargs = fargs

class FunctionDecl(ASTNode):
    def __init__(self,token,block=None,type=None,params=None):
        super().__init__(token)
        self.params = params
        self.type = type
        self.block = block

class ParamNode(ASTNode):
    def __init__(self,token,identifier=None):
        super().__init__(token)
        self.type = self.token
        self.id = identifier

class ArrayRef(ExpNode):
    def __init__(self,token,index=None):
        super().__init__(token)
        self.id = self.token
        self.index = index




class Block(ASTNode):
    def __init__(self):
        self.children = []

    def add_child(self,node):
        self.children.append(node)



#Base class for visitor objects
class Visitor:

    ''' Dispatcher method that chooses the correct
        visiting method'''

    def visit(self,node):
        node_class = type(node).__name__.lower
        method_name = f"visit_{node_class}"
        visitor_method = getattr(self,method_name,self.bad_visit)
        return visitor_method(node)

    def bad_visit(self,node):
        raise Exception("Unkwown node type")