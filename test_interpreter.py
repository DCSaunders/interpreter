#!/usr/bin/env python

import unittest


class LexerTestCase(unittest.TestCase):
    def makeLexer(self, text):
        from spi9 import Lexer
        lexer = Lexer(text)
        return lexer

    def test_lexer_integer(self):
        from spi9 import INTEGER
        lexer = self.makeLexer('234')
        token = lexer.get_next_token()
        self.assertEqual(token.type, INTEGER)
        self.assertEqual(token.value, 234)

    def test_lexer_mul(self):
        from spi9 import MUL
        lexer = self.makeLexer('*')
        token = lexer.get_next_token()
        self.assertEqual(token.type, MUL)
        self.assertEqual(token.value, '*')

    def test_lexer_div(self):
        from spi9 import DIV
        lexer = self.makeLexer('DIV')
        token = lexer.get_next_token()
        self.assertEqual(token.type, DIV)
        self.assertEqual(token.value, 'DIV')

    def test_lexer_plus(self):
        from spi9 import PLUS
        lexer = self.makeLexer('+')
        token = lexer.get_next_token()
        self.assertEqual(token.type, PLUS)
        self.assertEqual(token.value, '+')

    def test_lexer_minus(self):
        from spi9 import MINUS
        lexer = self.makeLexer('-')
        token = lexer.get_next_token()
        self.assertEqual(token.type, MINUS)
        self.assertEqual(token.value, '-')

    def test_lexer_lparen(self):
        from spi9 import LPAREN
        lexer = self.makeLexer('(')
        token = lexer.get_next_token()
        self.assertEqual(token.type, LPAREN)
        self.assertEqual(token.value, '(')

    def test_lexer_rparen(self):
        from spi9 import RPAREN
        lexer = self.makeLexer(')')
        token = lexer.get_next_token()
        self.assertEqual(token.type, RPAREN)
        self.assertEqual(token.value, ')')

    def test_lexer_new_tokens(self):
        from spi9 import ASSIGN, DOT, ID, SEMI, BEGIN, END
        records = (
            (':=', ASSIGN, ':='),
            ('.', DOT, '.'),
            ('NUMBER', ID, 'NUMBER'),
            (';', SEMI, ';'),
            ('BEGIN', BEGIN, 'BEGIN'),
            ('END', END, 'END'),
        )
        for text, tok_type, tok_val in records:
            lexer = self.makeLexer(text)
            token = lexer.get_next_token()
            self.assertEqual(token.type, tok_type)
            self.assertEqual(token.value, tok_val)


class InterpreterTestCase(unittest.TestCase):
    def makeInterpreter(self, text):
        from spi9 import Lexer, Parser, Interpreter
        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        return interpreter

    def test_arithmetic_expressions(self):
        for expr, result in (
            ('3', 3),
            ('2 + 7 * 4', 30),
            ('7 - 8 DIV 4', 5),
            ('14 + 2 * 3 - 6 DIV 2', 17),
            ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1))', 22),
            ('7 + 3 * (10 DIV (12 DIV (3 + 1) - 1)) DIV (2 + 3) - 5 - 3 + (8)', 10),
            ('7 + (((3 + 2)))', 12),
            ('- 3', -3),
            ('+ 3', 3),
            ('5 - - - + - 3', 8),
            ('5 - - - + - (3 + 4) - +2', 10),
        ):
            interpreter = self.makeInterpreter('BEGIN a := %s END.' % expr)
            interpreter.interpret()
            globals = interpreter.GLOBAL_SCOPE
            self.assertEqual(globals['A'], result)

    def test_expression_invalid_syntax1(self):
        interpreter = self.makeInterpreter('BEGIN a := 10 * ; END.')
        with self.assertRaises(Exception):
            interpreter.interpret()

    def test_expression_invalid_syntax2(self):
        interpreter = self.makeInterpreter('BEGIN a := 1 (1 + 2); END.')
        with self.assertRaises(Exception):
            interpreter.interpret()

    def test_statements(self):
        text = """\
BEGIN
    BEGIN
        number := 2;
        a := number;
        b := 10 * a + 10 * number DIV 4;
        c := a - - b
    END;
    x := 11;
END.
"""
        interpreter = self.makeInterpreter(text)
        interpreter.interpret()

        globals = interpreter.GLOBAL_SCOPE
        self.assertEqual(len(globals.keys()), 5)
        self.assertEqual(globals['NUMBER'], 2)
        self.assertEqual(globals['A'], 2)
        self.assertEqual(globals['B'], 25)
        self.assertEqual(globals['C'], 27)
        self.assertEqual(globals['X'], 11)


if __name__ == '__main__':
    unittest.main()
