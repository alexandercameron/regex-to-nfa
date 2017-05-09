'''
This file contains a Python 2.7 program that determines whether a series of strings 
is in the language described by the corresponding regular expression. 
A parse tree is used to convert the regular expression to an NFA. 
The NFA is converted into a DFA, which then runs the string, and accepts or rejects.

Authors: Alex Cameron, Eli Grady, Erick Perez
COMP 370, Dr. Glick, USD, Spring 17
'''

import sys

def main(input_file, output_file):

    parameters = readFile(input_file)

    alphabet = parameters['alphabet']
    regular_expression = parameters['regular_expression']
    input_strings = parameters['input_strings']

def readFile(input_file):

    parameters = {}

    f = open(input_file, 'r')

    parameters['alphabet'] = list(f.readline().strip("\n"))

    parameters['regular_expression'] = list(f.readline().strip("\n"))

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

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])