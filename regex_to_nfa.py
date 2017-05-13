'''
This file contains a Python 2.7 program that determines whether a series of strings 
is in the language described by the corresponding regular expression. 
A parse tree is used to convert the regular expression to an NFA. 
The NFA is converted into a DFA, which then runs the string, and accepts or rejects.

Authors: Alex Cameron, Eli Grady, Erick Perez
COMP 370, Dr. Glick, USD, Spring 17
'''

import sys

class Node:

    def __init__(self, symbol, left, right):

        self.symbol = symbol
        self.left = left
        self.right = right

def main(input_file, output_file):

    alphabet, regular_expression, input_strings = readFile(input_file)
    print "Regular expression:\n", regular_expression,"\n"
    parse_tree = make_parse_tree(regular_expression)

    dfs_list = []
    a = [parse_tree]

    dfs_list = unpack_node_list(dfs(a , dfs_list))

    NFA_a = make_nfa(parse_tree, alphabet)

    print NFA_a.__dict__

def make_nfa(parse_tree, alphabet):

    tree = parse_tree
    print tree.symbol

    if symbol_in_alphabet(tree.symbol, alphabet):
        curr_nfa = make_nfa_leaf(tree.symbol, alphabet)

    elif tree.symbol is 'e':
        curr_nfa = make_nfa_epsilon(tree.symbol, alphabet)

    elif tree.sybmol is 'N':
        curr_nfa = make_nfa_empty_set(tree.symbol, alphabet)

    elif tree.symbol is '*':
        curr_nfa = star_nfa(make_nfa(tree.right, alphabet))

    elif tree.symbol is '|':
        curr_nfa = union_nfas(make_nfa(tree.left, alphabet), make_nfa(tree.right, alphabet))

    elif tree.symbol is 'concat':
        curr_nfa = concat_nfas(make_nfa(tree.left, alphabet), make_nfa(tree.right, alphabet))

    return curr_nfa

class NFA:
    def __init__(self, states, transitions, accepts, start, alphabet):
        self.states = states
        self.transitions = transitions
        self.accepts = accepts
        self.start = start
        self.alphabet = alphabet

def make_nfa_leaf(symbol, alphabet):
    states = [1,2]
    accepts = [2]
    start_state = [1]
    transitions = {}

    i = 1
    while i < len(states) + 1:
        transitions[i] = {}
        i = i + 1

    i = 1
    while i < len(states) + 1:
        for letter in alphabet:
            transitions[i][letter] = []
            transitions[i][letter].append(-1)
        transitions[i]['e'] = []
        transitions[i]['e'].append(-1)
        i = i + 1

    transitions[1][symbol] = []
    transitions[1][symbol].append(2)

    return NFA(states, transitions, accepts, start_state, alphabet)

def make_nfa_epsilon(symbol, alphabet):
    print alphabet
    states = [1]
    start = [1]
    accepts = [1]
    transitions = {}
    for state in states:
        transitions[state] = {}
        for letter in alphabet:
            transitions[state][letter] = [-1]
        transitions[state]['e'] = [1]
    return NFA(states, transitions, accepts, start, alphabet)

def make_nfa_empty_set(symbol, alphabet):
    states = [1]
    start = [1]
    accepts = []
    transitions = {}
    for state in states:
        transitions[state] = {}
        for letter in alphabet:
            transitions[state][letter] = [-1]
        transitions[state]['e'] = [-1]
    return NFA(states, transitions, accepts, start, alphabet)

def concat_nfas(nfa_a, nfa_b):

    new_states = []
    for x in range(1, len(nfa_b.states) + len(nfa_a.states) + 1):
        new_states.append(x)


    new_accepts = []
    for accept_b in nfa_b.accepts:
        new_accepts.append(accept_b + len(nfa_a.states))


    new_starts = []
    for start_a in nfa_a.start:
        new_starts.append(start_a)

    new_transitions = {}
    for state_index in new_states:
        new_transitions[state_index] = {}
        for symbol in nfa_a.transitions[1]:
            new_transitions[state_index][symbol] = []
            if state_index <= len(nfa_a.states):
                for trans_state in nfa_a.transitions[state_index][symbol]:
                    if trans_state is not -1:
                        new_transitions[state_index][symbol].append(trans_state)
                    else:
                        new_transitions[state_index][symbol].append(-1)

                if symbol is 'e':
                    for accept_a in nfa_a.accepts:
                        if state_index is accept_a:
                            for start_b in nfa_b.start:
                                new_transitions[state_index][symbol].append(start_b + len(nfa_a.states))

            else:
                for trans_state in nfa_b.transitions[state_index - len(nfa_a.states)][symbol]:
                    if trans_state is not -1:
                        new_transitions[state_index][symbol].append(trans_state + len(nfa_a.states))
                    else:
                        new_transitions[state_index][symbol].append(-1)


    return NFA(new_states, new_transitions, new_accepts, new_starts, nfa_a.alphabet)

def union_nfas(nfa_a, nfa_b):

    #FINDS THE NEW LIST OF STATES
    states = []
    for x in range(1, len(nfa_b.states) + len(nfa_a.states) + 2):
        states.append(x)

    #FINDS THE NEW LIST OF ACCEPTING STATES
    new_accepts = []
    for a_accepts in nfa_a.accepts:
        new_accepts.append(a_accepts + 1)
    for b_accepts in nfa_b.accepts:
        new_accepts.append(b_accepts + len(nfa_a.states) + 1)

    #THERE WILL BE A NEW START STATE
    new_start = [1]

    #FINDS THE NEW TRANSITIONS
    new_transitions = {}
    new_transitions[1] = {}

    #Defines transitions for the start state (epsilons to the start states of A and B)
    for symbol in nfa_a.transitions[1]:
        if symbol is not 'e':
            new_transitions[1][symbol] = []
            new_transitions[1][symbol].append(-1)
        else:
            new_transitions[1][symbol] = []
            for a_start in nfa_a.start:
                new_transitions[1][symbol].append(a_start + 1)
            for b_start in nfa_b.start:
                new_transitions[1][symbol].append(b_start + len(nfa_a.states) + 1)

    #Renumbers the transitions from NFAs A and B
    state_num = 2
    while state_num <= len(nfa_b.states) +len(nfa_a.states) + 1:
        new_transitions[state_num] = {}
        if state_num <= len(nfa_a.states) + 1:
            for symbol in nfa_a.transitions[state_num -1]:
                new_transitions[state_num][symbol] = []
                for trans_state in nfa_a.transitions[state_num-1][symbol]:
                    if trans_state is not -1:
                        new_transitions[state_num][symbol].append(trans_state +1)
                    else:
                        new_transitions[state_num][symbol].append(-1)
        else:
            for symbol in nfa_b.transitions[state_num -len(nfa_a.states) - 1]:
                new_transitions[state_num][symbol] = []
                for trans_state in nfa_b.transitions[state_num- len(nfa_a.states) -1][symbol]:
                    if trans_state is not -1:
                        new_transitions[state_num][symbol].append(trans_state +len(nfa_a.states)+1)
                    else:
                        new_transitions[state_num][symbol].append(-1)



        state_num = state_num + 1


    return NFA(states, new_transitions, new_accepts, new_start, nfa_a.alphabet)

def star_nfa(nfa_a):

    #the new start state will be 1
    new_start = [1]

    new_states = [1]
    for state in nfa_a.states:
        new_states.append(state + 1)

    new_accepts = [1]
    for accept_a in nfa_a.accepts:
        new_accepts.append(accept_a + 1)

    new_transitions = {}
    for state in new_states:
        new_transitions[state] = {}

    #Defines transitions for the start state
    for symbol in nfa_a.transitions[1]:
        new_transitions[1][symbol] = []
        if symbol is 'e':
            for start_a in nfa_a.start:
                new_transitions[1][symbol].append(start_a + 1)
        else:
            new_transitions[1][symbol].append(-1)

    #Defines transitions for the rest of the NFA
    for state_a in nfa_a.transitions:
        new_state = state_a + 1
        for symbol in nfa_a.transitions[1]:
            new_transitions[new_state][symbol] = []
            for trans_state in nfa_a.transitions[state_a][symbol]:
                if trans_state is not -1:
                    new_transitions[new_state][symbol].append(trans_state + 1)
                else:
                    new_transitions[new_state][symbol].append(-1)

    for accept_a in nfa_a.accepts:
        new_transitions[accept_a + 1] ['e'] = []
        for start_a in nfa_a.start:
            new_transitions[accept_a + 1]['e'].append(start_a + 1)
    return NFA(new_states, new_transitions, new_accepts, new_start, nfa_a.alphabet)

def symbol_in_alphabet(symbol, alphabet):
    for al in alphabet:
        if symbol is al:
            return True
    return False

def readFile(input_file):

    parameters = {}

    f = open(input_file, 'r')

    alphabet = list(f.readline().strip("\n").replace(" ",""))

    regular_expression = list(f.readline().strip("\n").replace(" ",""))
    regular_expression = find_concat(regular_expression)
    input_strings = {}

    f.readline()
    string = f.readline().strip("\n")

    i = 0
    while len(string) > 0:
        input_strings[i] = string
        string = f.readline().strip("\n")
        i = i + 1

    return alphabet, regular_expression, input_strings

def find_concat(regular_expression):

    #these are the characters that you do not need to check if there is a concat following
    dont_check = ['|','(','concat']

    #these are the characters that you do not insert a concat in front
    not_in_front = ['|', '*','concat', ')']

    #This code checks if the symbol could need a concat following,
    #and checks the next symbol to see if concat is needed
    i = 0
    length = len(regular_expression)
    while i < length:

        is_op = 0
        for op in dont_check:

            if regular_expression[i] is op:
                is_op = 1

        #If the symbol may need a concat, we check the next symbol...
        if is_op is 0:

            is_next_op = 0
            for op in not_in_front:
                try:
                    if regular_expression[i+1] is op:
                        is_next_op = 1
                except:
                    is_next_op = 1

            #If we need to concat, we insert a concat symbol
            if is_next_op is 0:
                regular_expression.insert(i+1, 'concat')
                length = length + 1

        i = i + 1

    return regular_expression

def unpack_node_list(node_list):
    new_list = []
    for x in node_list:
        new_list.append(x.symbol)
    return new_list

def make_parse_tree(regular_expression):

    parse_tree = []

    operators = []
    operands = []
    i = 1
    for symbol in regular_expression:

        if symbol is '(':

            operators = left_paren(symbol, operators)

        elif symbol is ')':

            operands, operators = right_paren(symbol, operators, operands)

        elif symbol == 'concat':

            operators, operands = operator(symbol, operators, operands)

        elif symbol is '|':

            operators, operands = operator(symbol, operators, operands)

        elif symbol is '*':

            operators, operands = operator(symbol, operators, operands)

        else:

            operands = operand(symbol, operands)


    operators, operands = empty_operator(operators, operands)

    q = []
    for x in operands:
        q.append(x)

    return operands[0]

def dfs(q, dfs_list):

    x = q.pop()
    dfs_list.append(x)
    #print "symbol" , x.symbol
    try:
        a = x.right.symbol
        q.append(x.right)
        #print "right symbol", x.right.symbol
    except:
        #print "right", x.right
        pass

    try:
        a = x.left.symbol
        q.append(x.left)
        #print "left symbol", x.left.symbol
    except:
        #print "left", x.left
        pass

    if len(q) is not 0:
        dfs_list = dfs(q, dfs_list)

    return dfs_list

def empty_operator(operators, operands):
    while len(operators) > 0:
        popped_op = operators.pop()
        right_pop = operands.pop()
        if popped_op is '*':
            tmp = Node(popped_op, -1, right_pop)
        else:
            left_pop = operands.pop()
            tmp = Node(popped_op, left_pop, right_pop)

        operands.append(tmp)
    return operators, operands

#if a left paren if encountered, put it on the stack
#this is done
def left_paren(symbol, operators):

    operators.append(symbol)
    return operators

#i think this is done? need to do operator to check...
def right_paren(symbol, operators, operands):

    while until_empty_or_left(operators) is True :

        popped = operators.pop()

        if popped is '*':

            operand_pop = operands.pop()
            tmp = Node(popped, -1, operand_pop)
            operands.append(tmp)

        else:

            right_pop = operands.pop()
            left_pop = operands.pop()
            tmp = Node(popped,left_pop, right_pop)
            operands.append(tmp)

    if len(operators) > 0:
        operators.pop()


    return operands, operators

def until_empty_or_left(operators):

    if len(operators) is 0:
        return False
    if operators[len(operators)-1] is '(':
        return False
    return True

def operator(symbol, operators, operands):

    #as long as the stack is not empty, and the top of the stack
    #is an operator whose precedence is >= the precedence of
    #the operator just scanned...
    if not_empty_and_precedence(symbol, operators) :
        #pop the operator off the stack and create a syntax
        #tree node from it (popping its operands off the operand stack)
        #and push the new syntax tree node back onto the operand stack
        popped = operators.pop()
        right_pop = operands.pop()
        if popped is '*':
            tmp = Node(popped, -1, right_pop)
        else:
            left_pop = operands.pop()
            tmp = Node(popped, left_pop, right_pop)
        operands.append(tmp)

        operators.append(symbol)

    #when either the stack is empty or the top of the stack is not
    #an operator with precedence >= precedence of operator just
    #scanned, push operator just scanned onto the operator stack
    else:

        operators.append(symbol)


    return operators, operands

def not_empty_and_precedence(symbol, operator):

    if len(operator) is 0:
        return False
    if precedence_ge(symbol, operator[len(operator) - 1]) is False:
        return False
    return True

#returns true if top of stack is greater or eq the precedence of scanned
def precedence_ge(symbol, top_of_stack):
    p = {}
    p['*'] = 3
    p['concat'] = 2
    p['|'] = 1
    p['('] = 0

    if p[top_of_stack] >= p[symbol]:
        return True
    return False

#push operand onto stack
#this is done
def operand(symbol, operands):

    n = Node(symbol, -1, -1)

    operands.append(n)

    return operands

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
