# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis(tokenizer)
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF = 'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', 'LPAREN', 'RPAREN', 'EOF'


class Token(object):
    '''
    Token is base unit for gamma
    '''

    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Tokenizer(object):
    '''
    Tokenizer analysis given text and parse it to tokens
    it also names Lexer
    '''

    def __init__(self, text: str):
        # client string input, e.g. "3 + 5", "12 - 5 + 3", etc
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        self.current_char.isspace()
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self) -> int:
        """Return a (multidigit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self) -> Token:
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())

            if self.current_char is '+':
                self.advance()
                return Token(PLUS, '+')

            if self.current_char is '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char is '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char is "/":
                self.advance()
                return Token(DIV, '/')

            if self.current_char is '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char is ')':
                self.advance()
                return Token(RPAREN, ')')

            self.error()

        return Token(EOF, None)


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


class Parser(object):
    '''
    Parser parse given tokens to AST
    '''

    def __init__(self, tokenizer: Tokenizer):
        self.tokenizer = tokenizer
        self.current_token = self.tokenizer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type: str):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.tokenizer.get_next_token()
        else:
            self.error()

    def factor(self) -> AST:
        token = self.current_token
        if token.type is PLUS:
            self.eat(PLUS)
            return UnaryOp(op=token, factor=self.factor())
        elif token.type is MINUS:
            self.eat(MINUS)
            return UnaryOp(op=token, factor=self.factor())
        elif token.type is INTEGER:
            self.eat(INTEGER)
            return Num(token=token)
        elif token.type is LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self) -> AST:
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            else:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self) -> AST:
        """expr: term((PLUS | MINUS) term)*"""
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            else:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node

    def parse(self) -> AST:
        return self.expr()


class Visitor(object):
    '''
    Visitor is common base class to visit abstract syntax tree
    each concrete visitor should implement its visit method
    '''

    def visit(self, node: AST) -> int:
        if isinstance(node, BinOp):
            return self.visit_binop(node)
        elif isinstance(node, Num):
            return self.visit_num(node)

    def visit_binop(self, node: BinOp) -> int:
        pass

    def visit_num(self, node: Num) -> int:
        pass

    def visit_unaryop(self, node: UnaryOp) -> int:
        pass


class Interpreter(Visitor):
    '''
    Interpreter inherit from Visitor and interpret it when visiting the abstract syntax tree 
    '''

    def __init__(self, parser: Parser):
        self.parser = parser

    def visit_binop(self, node: BinOp) -> int:
        if node.op.type is PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type is MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type is MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type is DIV:
            return self.visit(node.left) // self.visit(node.right)

    def visit_num(self, node: Num) -> int:
        return node.token.value

    def visit_unaryop(self, node: UnaryOp) -> int:
        return +self.visit(node.factor) if node.op.type is PLUS else -self.visit(node.factor)

    def interpret(self) -> int:
        ast = self.parser.parse()
        return self.visit(ast)


def main():
    while True:
        try:
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        tokenizer = Tokenizer(text)
        parser = Parser(tokenizer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()
        print(result)


if __name__ == '__main__':
    main()
