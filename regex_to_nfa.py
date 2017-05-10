'''
This file contains a Python 2.7 program that determines whether a series of strings 
is in the language described by the corresponding regular expression. 
A parse tree is used to convert the regular expression to an NFA. 
The NFA is converted into a DFA, which then runs the string, and accepts or rejects.

Authors: Alex Cameron, Eli Grady, Erick Perez
COMP 370, Dr. Glick, USD, Spring 17
'''

import sys

class Tree:

    def __init__(self, nodes, root):

        self.nodes = nodes
        self.root = root

class Node:

    def __init__(self, symbol, left, right):

        self.symbol = symbol
        self.left = left
        self.right = right


def main(input_file, output_file):

    parameters = readFile(input_file)

    alphabet = parameters['alphabet']
    regular_expression = parameters['regular_expression']
    input_strings = parameters['input_strings']

    parse_tree = make_parse_tree(regular_expression)


def find_concat(regular_expression):

    #these are the characters that you do not need to check if there is a concat following
    operators = ['|','(','concat']

    #these are the characters that you do not insert a concat in front of after a terminal
    f_operators = ['|', '*','concat', ')']

    i = 0
    length = len(regular_expression)
    while i < length:

        is_op = 0
        for op in operators:

            if regular_expression[i] is op:
                is_op = 1

        if is_op is 0:

            is_next_op = 0
            for op in f_operators:
                try:
                    if regular_expression[i+1] is op:
                        is_next_op = 1
                except:
                    is_next_op = 1

            if is_next_op is 0:
                regular_expression.insert(i+1, 'concat')
                length = length + 1

        i = i + 1

    return regular_expression

def readFile(input_file):

    parameters = {}

    f = open(input_file, 'r')

    parameters['alphabet'] = list(f.readline().strip("\n").replace(" ",""))

    parameters['regular_expression'] = list(f.readline().strip("\n").replace(" ",""))
    parameters['regular_expression'] = find_concat(parameters['regular_expression'])
    input_strings = {}

    f.readline()
    string = f.readline().strip("\n")

    i = 0
    while len(string) > 0:
        input_strings[i] = string
        string = f.readline().strip("\n")
        i = i + 1

    parameters['input_strings'] = input_strings

    return parameters


def make_parse_tree(regular_expression):

    parse_tree = []

    operators = []
    operands = []

    for symbol in regular_expression:

        if symbol is '(':

            operators = left_paren(symbol, operators)

        elif symbol is ')':

            right_paren(symbol, operators, operands)

        elif symbol is '*' :

           operator(symbol, operators)

        elif symbol is '|' :

           operator(symbol, operators)

        else:

            operands = operand(symbol, operands)

    return parse_tree

def left_paren(symbol, operators):

    operators.append(symbol)
    return operators


def right_paren(symbol, operators, operands):

    while until_empty_or_left(operators) :

        popped = operators.pop()

        if popped is '*':

            operand_pop = operands.pop()
            tmp = Node(popped, 0, operand_pop)
            operands.append(tmp)

        else:

            right_pop = operands.pop()
            left_pop = operands.pop()
            tmp = Node(popped,left_pop, right_pop)
            operands.append(tmp)


def until_empty_or_left(operators):

    if operators[0] is '(':
        return False
    if len(operators) is 0:
        return False
    return True

def operator(symbol, operator):

    if len(operator) is not 0:

        pass


def operand(symbol, operands):

    n = Node(symbol, 0, 0)
    operands.append(n)
    return operands

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])