#!/usr/bin/env python
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF = 'INTEGER', 'PLUS', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, MINUS or EOF
        self.type = type
        # token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]
        
    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        self.pos += 1
        if self.pos > len(self.text)-1:
            self.current_char = None
        else:
            self.current_char = self.text[self.pos]
            
    def get_int(self):
        int_str = []
        while self.pos < len(self.text) and self.current_char.isdigit():
            int_str.append(self.current_char)
            self.advance()
        return "".join(int_str)

    def ignore_whitespace(self):
        while self.pos < len(self.text) and self.current_char.isspace():
            self.advance()
            
    
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer"""
        text = self.text

        if self.pos >= len(text):
            return Token(EOF, None)
        
        if self.current_char.isspace():
            self.ignore_whitespace()
            if self.pos >= len(text):
                return Token(EOF, None)
        
        if self.current_char == '+':
            token = Token(PLUS, self.current_char)
            self.advance()
            return token

        if self.current_char == '-':
            token = Token(MINUS, self.current_char)
            self.advance()
            return token

        if self.current_char.isdigit():
            int_str = self.get_int()
            token = Token(INTEGER, int(int_str))
            return token


        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()
        
        # we expect the current token to be an integer
        left = self.current_token
        self.eat(INTEGER)
        
        # we expect the current token to be a '+' token
        op = self.current_token
        self.eat(PLUS)

        # we expect the current token to be a single-digit integer
        right = self.current_token
        self.eat(INTEGER)
        
        result = int(left.value) + int(right.value)
        return result


def main():
    while True:
        try:
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
