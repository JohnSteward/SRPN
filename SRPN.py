from inFix import inFix
stack = [-2147483648]
operators = ['=', '^', '%', '/', '*', '+', '-', 'r', 'd']

# list of random numbers gotten from: https://www.mathstat.dal.ca/~selinger/random/
rNumbers = [1804289383, 846930886, 1681692777, 1714636915, 1957747793, 424238335, 719885386, 1649760492, 596516649,
            1189641421, 1025202362, 1350490027, 783368690, 1102520059, 2044897763, 1967513926, 1365180540, 1540383426,
            304089172, 1303455736, 35005211, 521595368, 294702567, 1726956429, 336465782, 861021530, 278722862,
            233665123, 2145174067, 468703135, 1101513929, 1801979802, 1315634022, 635723058, 1369133069, 1125898167,
            1059961393, 2089018456, 628175011, 1656478042, 1131176229, 1653377373, 859484421, 1914544919, 608413784,
            756898537, 1734575198, 1973594324, 149798315, 2038664370, 1129566413, 184803526, 412776091, 1424268980,
            1911759956, 749241873, 137806862, 42999170, 982906996, 135497281, 511702305, 2084420925, 1937477084,
            1827336327, 572660336, 1159126505, 805750846, 1632621729, 1100661313, 1433925857, 1141616124, 84353895,
            939819582, 2001100545, 1998898814, 1548233367, 610515434, 1585990364, 1374344043, 760313750, 1477171087,
            356426808, 945117276, 1889947178, 1780695788, 709393584, 491705403, 1918502651, 752392754, 1474612399,
            2053999932, 1264095060, 1411549676, 1843993368, 943947739, 1984210012, 855636226, 1749698586, 1469348094,
            1956297539]
total = 0
underflow = False
invalid = False
ignore = False
firstInt = True
reset = False
negativeP = False

# Checks saturation on the result of an operation
def saturate(total):
    if total > 2147483647:
        total = 2147483647
    elif total < -2147483648:
        total = -2147483648
    return total

# Generates a 'random' number when the 'r' command is used
def randomGenerate(stack):
    global firstInt
    global rIndex
    global reset
    overflow = stackOverflow(stack)
    if not overflow:
        if firstInt:
            stack.pop()
            firstInt = False
        stack.append(rNumbers[rIndex])
    rIndex += 1
    # Resets the random numbers once after 22 calls
    if (rIndex >= 22) and (reset == False):
        rIndex = 0
        reset = True
    if rIndex >= len(rNumbers):
        rIndex = 0


# Checks for invalid inputs
def unRecognised(inp):
    global ignore
    invalid = False
    # If the input is commented out, it skips the check
    if ignore:
        if inp == '#':
            ignore = False

        invalid = False
        return invalid

    else:
        try:
            inp = int(inp)
        except:
            # Checks for the start of a comment
            if inp == '#':
                ignore = True

            if not ignore:
                try:
                    inp = int(inp)
                except:
                    if (inp not in operators) and (inp != ' ') and (ignore == False):
                        invalid = True
                        return invalid
                    else:
                        invalid = False
                        return invalid
            return invalid
        return invalid


def operate(inp, total, underflow, stack, rIndex, printed):
    negativeP = False
    if not ignore:
        if inp == 'd':
            copyStack(stack)
        elif inp == 'r':
            randomGenerate(stack)
        # Does the operation corresponding with the input
        # on the last 2 elements in the stack
        else:
            if (inp != '=') and (inp != 'd'):
                underflow = stackUnderflow(stack)
            if not underflow:
                if inp == '+':
                    total = stack.pop()
                    total += stack.pop()
                    total = saturate(total)
                elif inp == '-':
                    total = stack[-2]
                    total -= stack.pop()
                    stack.pop()
                    total = saturate(total)
                elif inp == '^':
                    # Checks whether it is doing a number to a negative power
                    if stack[-1] < 0:
                        print("Negative power.")
                        negativeP = True
                        return None
                    else:
                        negativeP = False
                        total = stack[-2]
                        total **= stack.pop()
                        stack.pop()
                        total = saturate(total)
                elif inp == '*':
                    total = stack.pop()
                    total *= stack.pop()
                    total = saturate(total)
                elif inp == '/':
                    total = stack[-2]
                    dBZ = divideByZero(stack)
                    if not dBZ:
                        total //= stack.pop()
                        stack.pop()
                        total = saturate(total)
                elif inp == '%':
                    underflow = stackUnderflow(stack)
                    if not underflow:
                        total = stack[-2]
                        total = total % (stack.pop())
                        stack.pop()
                        total = saturate(total)

                elif inp == '=':
                    # Checks whether the stack is empty
                    if firstInt:
                        print("Stack empty.")
                    else:
                        if not printed:
                            print(stack[-1])
                            printed = True
                            return printed
                # Adds the total to the end of the stack after each operation
                if inp != '=':
                    stack.append(total)
        if not negativeP:
            return total


# Checks for a stack overflow
def stackOverflow(stack):
    if len(stack) >= 23:
        print("Stack overflow.")
        return True
    else:
        return False


# Checks for a stack underflow
def stackUnderflow(stack):
    if len(stack) <= 1:
        print("Stack underflow.")
        underflow = True
        return underflow
    else:
        underflow = False
        return underflow


# Splits a string of integers, operations, spaces and invalid inputs
def splitString(inp, total, ignore):
    firstOperator = False
    printed = False
    global firstInt
    number = ''
    if inp not in operators:
        # Checks for any comments at the start
        for i in range(len(inp)):
            if (ignore == False) and (i < (len(inp) - 1)):
                if inp[i] == '#':
                    ignore = True
            elif ignore and (i < (len(inp) - 1)):
                if inp[i] == '#':
                    ignore = False

            # splitting numbers separated by spaces
            if ((inp[i] == ' ') and (ignore == False)) or (
                    ((i == len(inp) - 1) and (inp[i] != '#')) and (inp[i] not in operators) and (
                    unRecognised(inp[i]) == False)):
                temp = i
                while (inp[i - 1] not in operators) and (i > 0) and (inp[i - 1] != ' '):
                    invalid = unRecognised(inp[i - 1])
                    if not invalid:
                        i -= 1
                    else:
                        break
                while i <= temp:
                    number += inp[i]
                    i += 1
                try:
                    number = int(number)
                except:
                    pass
                if type(number) == int:
                    if firstInt:
                        stack.pop()
                        firstInt = False
                    stack.append(number)
                # Prints the last thing in the stack before any operations
                # are done on the string
                if ('=' in inp) and (printed == False) and (firstOperator == True):
                    print(stack[-1])
                    printed = True
                number = ''

            # Checks for an operator and does the correct operation on the current stack
            elif inp[i] in operators:
                if (printed == False) and ('=' in inp):
                    printed = operate('=', total, underflow, stack, rIndex, printed)
                if not ignore:
                    if not firstOperator:
                        firstOperator = True
                    # Checks backwards in the string for any integers between
                    # the operator and, either a space or another operator
                    if (inp[i - 1] != ' ') and (inp[i - 1] not in operators):
                        temp = i - 1
                        while (inp[i - 1] not in operators) and (i > 0) and (inp[i - 1] != ' '):
                            invalid = unRecognised(inp[i])
                            if not invalid:
                                i -= 1
                        while i <= temp:
                            number += inp[i]
                            i += 1
                        try:
                            number = int(number)
                        except:
                            pass
                        if type(number) == int:
                            if firstInt:
                                stack.pop()
                                firstInt = False
                            stack.append(number)
                        number = ''
                    # Does an operation using inp[i] as the operator
                    total = operate(inp[i], total, underflow, stack, rIndex, printed)

            # Checks the string for integers behind invalid inputs
            elif inp[i] not in operators:
                if not ignore:
                    invalid = unRecognised(inp[i])
                    if invalid:
                        print('Unrecognised operator or operand "' + inp[i] + '"')
                        temp = i
                        while (inp[i - 1] not in operators) and (i > 0) and (inp[i - 1] != ' ') and (
                                unRecognised(inp[i - 1]) == False):
                            i -= 1
                        # Adds the integers to the number string in the correct order
                        while i < temp:
                            number += inp[i]
                            i += 1
                        try:
                            number = int(number)
                        except:
                            pass
                        if type(number) == int:
                            if firstInt == True:
                                stack.pop()
                                firstInt = False
                            stack.append(number)
                        number = ''


# Prints all elements in the stack when the input is 'd'
def copyStack(stack):
    for element in stack:
        print(element)


# Checks for a divide by zero error
def divideByZero(stack):
    if stack[-1] == 0:
        print("Divide by 0.")
        return True
    else:
        return False


rIndex = 0
while True:
    inFixed = False
    printed = False
    operating = True
    # Main loop that asks for each input and calls functions accordingly
    # depending on the type of input
    underflow = False
    inp = input()
    try:
        inp = int(inp)
    except:
        if len(inp) == 1:
            unRecognised(inp)
        # Checks for a string input(multiple commands)
        if (type(inp) != int) and (inp not in operators):
            inpList = []
            for i in inp:
                inpList.append(i)
            if (operating) and (' ' not in inpList):
                for i in operators:
                    if i in inpList:
                        operating = True
                        break
                    else:
                        operating = False
            else:
                operating = False

            try:
                inpList[0] = int(inpList[0])
                inpList[-1] = int(inpList[-1])
            except:
                pass
            # Checks whether the string can be interpreted as a normal mathematical expression
            while (' ' not in inp) and (type(inpList[0]) == int) and (type(inpList[-1]) == int) and (len(inpList) > 1):
                inFixedResult = inFix(operators, inpList, total)
                if firstInt:
                    stack.pop()
                    firstInt = False
                for i in inFixedResult[1]:
                    stack.append(i)
                if len(stack) > 2:
                    stack.pop(0)
                total = operate(inFixedResult[0], total, underflow, stack, rIndex, printed)
                inpList.insert(inFixedResult[2], total)
                inFixed = True

            if not inFixed:
                splitString(inp, total, ignore)
            # Checks if the input is an operator and calls operate() if it isn't part of a comment
            if (operating) and (not ignore):
                if inp in operators:
                    total = operate(inp, total, underflow, stack, rIndex, printed)
                    operating = False

    # Checks for a single integer input
    if type(inp) == int:
        if firstInt:
            stack.pop()
            firstInt = False
        stack.append(inp)

    # Checks for a single operator input
    elif inp in operators:
        total = operate(inp, total, underflow, stack, rIndex, printed)
