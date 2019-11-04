from visitor import Visitor
from symbol_table import ScopedSymbolTable, VarSymbol, ProcedureSymbol, BuildinTypeSymbol
from astnodes import BinOp, Num, UnaryOp, Compound, Var, Assign, NoOp, Program, Block, VarDecl, Type, ProcedureDecl


class SemanticAnalyzer(Visitor):
    '''
    SemanticAnalyzer inherit from Visitor and it's work is
    build program's symbol table by given AST parsed by Parser
    '''

    def __init__(self):
        self.buildin_scope = ScopedSymbolTable(
            scope_name='buildin',
            scope_level=0,
        )
        self.__init_buildins()
        self.current_scope = self.buildin_scope

    def __init_buildins(self):
        print('init buildin scope\'s symbols')
        # initialize the built-in types when the symbol table instance is created.
        self.buildin_scope.define(BuildinTypeSymbol('INTEGER'))
        self.buildin_scope.define(BuildinTypeSymbol('REAL'))

    def scope(self) -> ScopedSymbolTable:
        return self.current_scope

    def visit_program(self, node: Program):
        # add global scoped symbol table
        global_scope = ScopedSymbolTable(
            scope_name='global',
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope)
        self.current_scope = global_scope
        print('enter scope: %s' % self.current_scope.scope_name)
        self.visit(node.block)
        print(global_scope)
        print('leave scope: %s' % self.current_scope.scope_name)
        self.current_scope = self.current_scope.enclosing_scope

    def visit_block(self, node: Block):
        for declaration in node.declarations:
            self.visit(declaration)
        self.visit(node.compound_statement)

    def visit_compound(self, node: Compound):
        for child in node.childrens:
            self.visit(child)

    def visit_binop(self, node):
        self.visit(node.left)
        self.visit(node.right)

    def visit_vardecl(self, node: VarDecl):
        type_name = node.type.type
        type_symbol = self.current_scope.lookup(type_name)

        # We have all the information we need to create a variable symbol.
        # Create the symbol and insert it into the symbol table.
        var_name = node.var.value
        # duplicate define check
        if self.current_scope.lookup(var_name, current_scope_only=True) is not None:
            raise Exception(
                "Error: Duplicate identifier '%s' found" % var_name
            )

        var_symbol = VarSymbol(var_name, type_symbol)
        self.current_scope.define(var_symbol)

    def visit_assign(self, node: Assign):
        # right-hand side
        self.visit(node.right)
        # left-hand side
        self.visit(node.left)

    def visit_var(self, node: Var):
        # judge if variable is not declared
        var_name = node.value
        var_symbol = self.current_scope.lookup(var_name)
        if var_symbol is None:
            raise Exception(
                "Error: Symbol(identifier) not found '%s'" % var_name
            )

    def visit_procdecl(self, node: ProcedureDecl):
        proc_name = node.proc_name
        proc_symbol = ProcedureSymbol(proc_name)
        if self.current_scope.lookup(proc_name, current_scope_only=True) is not None:
            raise Exception(
                "Error: Duplicate procedure '%s' found" % proc_name
            )
        self.current_scope.define(proc_symbol)

        # new scope include var declaration and formal params
        procedure_scope = ScopedSymbolTable(
            scope_name=proc_name,
            scope_level=self.current_scope.scope_level + 1,
            enclosing_scope=self.current_scope)
        self.current_scope = procedure_scope

        # then we shoud enter new scope
        print('enter scope: %s' % self.current_scope.scope_name)
        # intert params into the procedure scope
        for param in node.params:
            param_name = param.var.value
            param_type = self.current_scope.lookup(param.type.type)
            # build var symbol and append to proc_symbol
            var_symbol = VarSymbol(name=param_name, type=param_type)
            proc_symbol.params.append(var_symbol)
            # define symbol into current scope
            self.current_scope.define(var_symbol)

        self.visit(node.block)
        print(procedure_scope)
        print('leave scope: %s' % self.current_scope.scope_name)
        self.current_scope = self.current_scope.enclosing_scope
