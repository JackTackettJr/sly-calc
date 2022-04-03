# -----------------------------------------------------------------------------
# sly-calc.py
#	expanded calculator lexer/parser based on sly package. 
#	Includes real numbers, strings, and expaned math parsering.
# -----------------------------------------------------------------------------

from sly import Lexer, Parser
import os

class CalcLexer(Lexer):
    tokens = { IDENT, NUMBER, STRING, FLOOR,
               EQ, LT, LE, GT, GE, NE,
			   CLS,INFO,QUIT}

    ignore = ' \t'
    literals = { '=', '+', '-', '*', '/', '(', ')' , '{','}','^','%' }

    ignore_comment = r'\#.*'  

    LE      = r'<='
    GE      = r'>='
    EQ      = r'=='
    LT      = r'<'
    GT      = r'>'
    NE      = r'!='
    FLOOR    = r'//'
    STRING = r'\".*?\"'

    # Tokens
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    IDENT['cls'] = CLS
    IDENT['info'] = INFO
    IDENT['quit'] = QUIT


    @_(r'[-+]?[0-9]+(\.([0-9]+)?([eE][-+]?[0-9]+)?|[eE][-+]?[0-9]+)',
	    r'\d+')
    def NUMBER(self, t):
        if '.' in t.value:
            t.value = float(t.value)
        else:
            t.value = int(t.value)
        return t
		
    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
#        print("Illegal character '%s'" % t.value[0])
        print('Line %d: ILLEGAL character %r' % (self.lineno, t.value[0]))
        self.index += 1

class CalcParser(Parser):
    tokens = CalcLexer.tokens
 
    precedence = (
        ('left', '+', '-'),
        ('left', '*', '/','FLOOR','%'),
        ('right', 'UMINUS'),
        )

    def remove_quotes(self, text: str):
        if text.startswith('\"') or text.startswith('\''):
            return text[1:-1]
        return text
		
    def __init__(self):
        self.names = { }
        self.env = { }
        self.version = "0.4"

    @_('IDENT "=" STRING')
    def statement(self, p):
#        self.names[p.IDENT] = p.STRING
        self.names[p.IDENT] = self.remove_quotes(p.STRING)

    @_('IDENT "=" expr')
    def statement(self, p):
        self.names[p.IDENT] = p.expr

    @_('expr')
    def statement(self, p):
        print(p.expr)

    @_('expr "+" expr')
    def expr(self, p):
        return p.expr0 + p.expr1

    @_('expr "-" expr')
    def expr(self, p):
        return p.expr0 - p.expr1

    @_('expr "^" expr')
    def expr(self, p):
        return p.expr0 ** p.expr1

    @_('expr "*" expr')
    def expr(self, p):
        return p.expr0 * p.expr1

    @_('expr "/" expr')
    def expr(self, p):
        if p.expr1 == 0:
            print('ERR: Division by zero attempted.')
            return 0
        else:
            return p.expr0 / p.expr1

    @_('expr "%" expr')
    def expr(self, p):
        if p.expr1 == 0:
            print('ERR: Division by zero attempted.')
            return 0
        else:
            return p.expr0 % p.expr1

    @_('expr FLOOR expr')
    def expr(self, p):
        if p.expr1 == 0:
            print('ERR: Division by zero attempted.')
            return 0
        else:
            return p.expr0 // p.expr1

    @_('expr EQ expr')
    def expr(self, p):
        return p.expr0 == p.expr1

    @_('expr LT expr')
    def expr(self, p):
        return p.expr0 < p.expr1

    @_('expr LE expr')
    def expr(self, p):
        return p.expr0 <= p.expr1

    @_('expr GT expr')
    def expr(self, p):
        return p.expr0 > p.expr1

    @_('expr GE expr')
    def expr(self, p):
        return p.expr0 >= p.expr1

    @_('expr NE expr')
    def expr(self, p):
        return p.expr0 != p.expr1

    @_('"-" expr %prec UMINUS')
    def expr(self, p):
        return -p.expr

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('NUMBER')
    def expr(self, p):
        return p.NUMBER

    @_('IDENT')
    def expr(self, p):
        try:
            return self.names[p.IDENT]
        except LookupError:
            print("Undefined name '%s'" % p.IDENT)
            return 0

    @_('CLS')
    def expr(self, p):
        os.system('cls')
        
    @_('INFO')
    def expr(self, p):
        print('Version %s' % self.version)
		
    @_('QUIT')
    def expr(self, p):
        print('Good-Bye.')
        quit()

if __name__ == '__main__':

    lexer = CalcLexer()
    parser = CalcParser()
    env = { }
#    print(CalcLexer.__dict__)
#    print(CalcParser.__dict__)

    while True:
        try:
            text = input('calc > ')
        except EOFError:
            break
        if text:
 #           for tok in lexer.tokenize(text):
 #               print(tok)
            parser.parse(lexer.tokenize(text))
