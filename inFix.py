def inFix(operators, inpList, total):
    operateList = []
    operateInOrderList = []
    inList = []
    operateInOrder = ""
    # Making inp into a list for easier manipulation
    for i in operators:
        if i in inpList:
            index = inpList.index(i)
            number1 = inpList[index - 1]
            number2 = inpList[index + 1]
            inList = [int(number1), int(number2)]
            inpList.pop(index)
            inpList.pop(index)
            inpList.pop(index - 1)
            return i, inList, (index - 1)
    return i, inList
