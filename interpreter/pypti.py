import ast
from interpreter.tokens import TokenType as TT
import interpreter.ast_nodes as AST
import interpreter.semantic as SEM
from interpreter.error import RunTimeError
from interpreter.object import RTFunction,Environment



class Interpreter(AST.Visitor):
    GLOBAL_MEMORY = "GLOBAL"
    LOCAL_MEMORY = "LOCAL"
    #something like null
    NONE_TYPE = "NONE"

    def __init__(self,program):

        self.program = program # Checked AST
        self.memory = Environment(Interpreter.GLOBAL_MEMORY)


    def interpret(self):
        self.execute(self.program)



    def execute(self,node,arg=None):
        node_class = type(node).__name__.lower()
        method_name = f"exec_{node_class}"
        visitor_method = getattr(self,method_name,self.generic_exec)
        if node_class == "block":
            return visitor_method(node,arg)
        return visitor_method(node)


    def resolve(self,node):
        node_class = type(node).__name__.lower()
        method_name = f"resolve_{node_class}"
        visitor_method = getattr(self,method_name,self.generic_exec)
        return visitor_method(node)


    def exec_program(self,node):
        for child in node.children:
            self.execute(child)

    def exec_block(self,node,environment=None):
        #Create new env for local scope
        if environment:
            self.memory = environment
        else:
            self.memory = Environment(Interpreter.LOCAL_MEMORY,self.memory)
        for child in node.children:
            self.execute(child)
        #restore previous env
        self.memory = self.memory.previous

    def exec_vardeclnode(self,node):
        name = node.id.lexeme
        type = node.type.lexeme
        if type == "int":
            self.memory.define(name,0)
        elif type == "real":
            self.memory.define(name,0.0)
        elif type == "texto":
            self.memory.define(name,"")
        else:
            self.memory.define(name,Interpreter.NONE_TYPE)
        if node.assign is not None:
            self.execute(node.assign)

    def exec_assignnode(self,node):
        value = self.execute(node.right)
        name = self.resolve(node.left)
        memory = self.memory.resolve_space(name)
        memory.define(name,value)
        return value

    def resolve_expnode(self,node):
        return node.token.lexeme



    def exec_binopnode(self,node):
        left = self.execute(node.left)
        right = self.execute(node.right)
        op = node.token.token
        if op == TT.PLUS:
            return left + right
        elif op == TT.MINUS:
            return left - right
        elif op == TT.STAR:
            return left * right
        elif op == TT.SLASH:
            if node.eval_type == SEM.Type.REAL:
                return left/right;
            else:
                return left//right;
        elif op == TT.MODULO:
            return left % right;
        elif op == TT.GREATER:
            return left > right
        elif op == TT.LESS:
            return left < right
        elif op == TT.GREATEREQ:
            return left >= right
        elif op == TT.LESSEQ:
            return left <= right
        elif op == TT.NOTEQUAL:
            return left != right
        elif op == TT.DOUBLEEQUAL:
            return left == right
        elif op == TT.AND:
            return left and right
        elif op == TT.OR:
            return left or right


    def exec_unaryopnode(self,node):
        value = self.execute(node.operand)
        if node.token.token == TT.MINUS:
            return -value
        elif node.token.token == TT.NOT:
            return not value
        return value

    def exec_expnode(self,node):
        if node.token.token == TT.IDENTIFIER:
            return self.memory.resolve(node.token.lexeme)
        else:
            type = node.prom_type
            if type == SEM.Type.VAZIO or type is None:
                type = node.eval_type
                if type == SEM.Type.INT:
                    return int(node.token.lexeme)
                elif type == SEM.Type.REAL:
                    return float(node.token.lexeme)
                elif type == SEM.Type.TEXTO:
                    #format the string lol
                    return ast.literal_eval(node.token.lexeme)
                elif type == SEM.Type.BOOL:
                    return True if node.token.token == TT.VERDADEIRO else False
            else:
                if type == SEM.Type.REAL:
                    return float(node.token.lexeme)
                elif type == SEM.Type.BOOL:
                    return bool(node.token.lexeme) #False: 0,0.0 and "" True: Everything else

    def exec_sestatement(self,node):
        condition = self.execute(node.condition)
        if bool(condition):
            self.execute(node.then_branch)
        elif node.else_branch is not None:
            self.execute(node.else_branch)

    def exec_whilestatement(self,node):
        if isinstance(node.statement,AST.Block):
            env = Environment(Interpreter.LOCAL_MEMORY,self.memory)
            while bool(self.execute(node.condition)):
                self.execute(node.statement,env)
        else:
            while bool(self.execute(node.condition)):
                self.execute(node.statement)

    def exec_statement(self,node):
        expr = self.execute(node.exp)
        if node.exp.eval_type == SEM.Type.BOOL:
            expr = "verdadeiro" if expr == True else "falso"
        token = node.token.token
        if token == TT.MOSTRA:
            print(expr,end="\n\n")


    def generic_exec(self,node):
        pass
