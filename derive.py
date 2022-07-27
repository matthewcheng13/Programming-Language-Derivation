'''
Matthew Cheng
Assignment 2

This python script will receive an input file from the command line
with the optional -d (show derivation) and -l (default 3; length of
derivations) arguments. It will output either the full derivations 
or just the finished derivations once there are no nonterminals.
'''

import sys

# this handles the command line arguments
# the default length of the derivations is 3
# the default output is to not show all steps
N = 3
deriv = False
for i in sys.argv:
    if i[0] == '-':
        if i[1] == 'l':
            N = int(i[2:])
        if i[1] == 'd':
            deriv = True
    else:
        filename = i

# create dictionary and work list
d = {}
w = []

delimeter = ''

# read in the file
for line in open(filename,'r'):
    # break up all of the components of the file
    # separate the nonterminal and determine the delimeter
    components = line.split()
    term = components.pop(0)
    delimeter = components.pop(0)
    # append the upper left nonterminal to the worklist
    if len(w) == 0:
        w.append([term,[term]])
    # if the term is already in the dictionary, add its components
    # if not, then add it to the dictionary along with its components
    if term in d:
        d[term] += [' '.join(components)]
    else:
        d[term] = [' '.join(components)]

# create a list of what has been output already to avoid repetition
# that results from ambiguity      
#ambig = []
ambig = set()

# create a counting variable to keep track of the amount of outputs
count = 0

# while loop that is responsible for taking each step in the derivation
while len(w) > 0:
    # work with the first item in the worklist (each one at a time)
    s =  w.pop(0)
    check = s[0].split()
    # as long as the derivation is short enough, we can take the next step
    if len(check) <= N:
        # set nonterminal to false by default
        NT = False
        # if any terminals are found, change to true
        for toCheck in check:
            if toCheck in d:
                NT = True
        # if none were found, then we go to the printing section
        if (NT == False):
            # make sure that anything not equal to length N gets lost as we
            # don't need it
            if (len(check) == N):
                # if -d was specified at the beginning, show complete derivation
                if deriv:
                    # as long as a derivation has not been printed before, print it
                    if s[0] not in ambig:
                        # ensure correct formatting
                        top = s[1][0] + ' '
                        indent = len(top) * ' '
                        print('\n' + top + delimeter + ' ' + s[1][1])
                        for der in s[1][2:]:
                            print(indent + delimeter + ' ' + der)
                        #ambig.append(s[0])
                        ambig.add(s[0])
                        count += 1
                # if -d not specified, print just the final derivation
                else:
                    if count == 0:
                        print('')
                    if s[0] not in ambig:
                        print(s[0])
                        #ambig.append(s[0])
                        ambig.add(s[0])
                        count += 1
        # if there were nonterminals...
        else:
            # find the first nonterminal
            for i in range(len(check)):
                if check[i] in d:
                    break
            # then replace it and create a new derivation for each
            # of its replacements
            for rhs in d[check[i]]:
                check[i] = rhs
                tmp = ' '.join(check)
                der_list = []
                # copy the derivation list and add the newest step
                for ele in s[1]:
                    der_list.append(ele)
                der_list.append(tmp)
                # add back to the end of the worklist
                w.append([tmp,der_list])

# once the final result has been printed, state the amount of strings                
print("\n# of strings generated:",count,"\n\n") 