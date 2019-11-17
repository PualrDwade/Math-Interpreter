from tokenizer import Token
from typing import List


class AST(object):
    pass


class BinOp(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = op
        self.op = op
        self.right = right


class UnaryOp(AST):
    def __init__(self, op: Token, factor: AST):
        self.token = self.op = op
        self.factor = factor


class Num(AST):
    def __init__(self, token: Token):
        self.token = token


class Boolean(AST):
    def __init__(self, token: Token):
        self.token = token


class Compound(AST):
    def __init__(self):
        self.childrens = []  # use list to combine many compound


class Var(AST):
    def __init__(self, token: Token):
        self.token = token
        self.name = token.value  # self.value holds the variable's name


class Assign(AST):
    def __init__(self, left: AST, op: Token, right: AST):
        self.left = left
        self.token = self.op = op
        self.right = right


class Type(AST):
    def __init__(self, token: Token):
        self.token = token
        self.name = token.value


class VarDecl(AST):
    def __init__(self, var_node: Var, type_node: Type):
        self.var_node = var_node
        self.type_node = type_node


class Block(AST):
    def __init__(self, declarations: List[VarDecl], compound_statement: Compound):
        self.declarations = declarations
        self.compound_statement = compound_statement


class Program(AST):
    def __init__(self, name: str, block: Block):
        self.name = name
        self.block = block


class Param(AST):
    def __init__(self, var_node: Var, type_node: Type):
        self.var_node = var_node
        self.type_node = type_node


class ProcedureDecl(AST):
    def __init__(self, proc_token: Token, params: List[Param], block: Block):
        self.proc_token = proc_token
        self.block = block
        self.params = params


class ProcedureCall(AST):
    def __init__(self, proc_name: str, actual_params: List[AST], token: Token):
        self.proc_name = proc_name
        self.actual_params = actual_params  # a list of AST nodes
        self.token = token


class Then(AST):
    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child


class Else(AST):
    def __init__(self, token: Token, child: AST):
        self.token = token
        self.child = child


class Condition(AST):
    def __init__(self, token: Token, condition_node: AST, then_node: Then, else_node: Else):
        self.token = token
        self.condition_node = condition_node
        self.then_node = then_node
        self.else_node = else_node


class NoOp(AST):
    pass
