import math
from chars import *




def DataFlowAnalysis(filepath):
    file = open(filepath, 'r')
    splits = []
    word = ''
    opr = ''
    codeBox = ''

    definite = int(input("This program has 2 paths:\n if you want possible live variable analysis, press 0.\n if you want definite live variable analysis,press 1\n"))

    lineNumber = 0
    variables = []

    for line in file:
        lineNumber += 1
        for char in line:
            codeBox += char
            if char in macro:
                break
            if char in separators:
                if word:
                    splits.append(word)
                if opr:
                    splits.append(opr)
                    opr = ''
                word = ''
            elif char in opers and char in doubleOpers:  # check for ++ or += or ....
                if word:
                    splits.append(word)
                opr += char
                word = ''
            elif char in opers:
                if word:
                    splits.append(word)
                splits.append(char)
                word = ''
            else:
                if opr:
                    splits.append(opr)
                    opr = ''
                word += char

    statements = {}
    statm = ""
    flag = 0
    statNum = 0
    braces = 0
    incrFor = ""
    incrSplit = []
    operationsSplit = []
    mappingDictionary = {}
    conditionIndex = 0
    ifIndex = 0
    incrIndex = 0
    currentBraces = 0

    reserved = 5

    for i in range(4, len(splits)):
        i = reserved
        if i >= len(splits) - 1:
            break
        if splits[i] in variables:
            while splits[i] != ';':
                statm = statm + splits[i]
                operationsSplit.append(splits[i])
                i += 1
            if splits[i + 1] in doubles:
                statm = statm + splits[i + 1]
                operationsSplit.append(splits[i + 1])
                i += 2
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            statNum += 1
            operationsSplit.append('~')
            statm = ""

        elif splits[i] in define:
            statm = splits[i] + " "
            # operationsSplit.append(splits[i])
            while splits[i] != ';':
                if splits[i] in define:
                    i += 1
                    continue
                if splits[i] == ',':
                    statm = statm + splits[i] + " "
                    # operationsSplit.append(splits[i])
                    i += 1
                    continue
                variables.append(splits[i])
                statm = statm + splits[i]
                # operationsSplit.append(splits[i])
                i += 1
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            statNum += 1
            i += 1
            # operationsSplit.append('~')
            statm = ""

        elif splits[i] in scanf:
            statm = "scan("
            operationsSplit.append(splits[i])
            while splits[i] != '&':
                i += 1
            i += 1
            statm = statm + splits[i] + ")"
            operationsSplit.append(splits[i])
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            statNum += 1
            operationsSplit.append('~')
            statm = ""
            i += 2

        elif splits[i] in printf:
            statm = "print("
            while splits[i] != ',' and splits[i] != ';':
                i += 1
            if splits[i] == ';':
                statm = ""
            else:
                i += 1
                operationsSplit.append("printf")
                operationsSplit.append(splits[i])
                statm = statm + splits[i] + ")"
                statements[statNum] = statm
                if statNum not in mappingDictionary:
                    mappingDictionary[statNum] = []
                mappingDictionary[statNum].append(statNum + 1)
                statNum += 1
                operationsSplit.append('~')
                statm = ""
                i += 2
                flag = 0

        elif splits[i] == "for":
            semicol = 0
            braces += 1
            i += 2
            while splits[i] != '{':
                if splits[i] == ';':
                    semicol += 1
                    operationsSplit.append('~')
                    statements[statNum] = statm
                    if statNum not in mappingDictionary:
                        mappingDictionary[statNum] = []
                    mappingDictionary[statNum].append(statNum + 1)
                    if semicol == 2:
                        conditionIndex = statNum
                        if statNum not in mappingDictionary:
                            mappingDictionary[statNum] = []
                    statNum += 1
                    statm = ""
                    if semicol == 1:
                        operationsSplit.append("if")
                    i += 1
                    continue
                if splits[i] == ')':
                    i += 1
                if semicol == 2:
                    incrFor = incrFor + splits[i]
                    incrSplit.append(splits[i])
                    i += 1
                else:
                    statm = statm + splits[i]
                    operationsSplit.append(splits[i])
                    i += 1
            i += 1

        elif splits[i] == "if":
            operationsSplit.append(splits[i])
            statm = "if("
            currentBraces = braces
            braces += 1
            i += 2
            while splits[i] != ')':
                statm = statm + splits[i]
                operationsSplit.append(splits[i])
                i += 1
            statm = statm + splits[i]
            statements[statNum] = statm
            if statNum not in mappingDictionary:
                mappingDictionary[statNum] = []
            mappingDictionary[statNum].append(statNum + 1)
            ifIndex = statNum
            statNum += 1
            operationsSplit.append('~')
            i += 2
            statm = ""

        elif splits[i] == '}':
            braces -= 1
            if braces == 0:
                if incrFor:
                    statements[statNum] = incrFor
                    if statNum not in mappingDictionary:
                        mappingDictionary[statNum] = []
                    mappingDictionary[statNum].append(conditionIndex)
                    mappingDictionary[conditionIndex].append(statNum + 1)
                    incrIndex = statNum
                    statNum += 1
                    incrFor = ""
                for x in incrSplit:
                    operationsSplit.append(x)
                operationsSplit.append('~')
            if currentBraces == braces:
                if ifIndex not in mappingDictionary:
                    mappingDictionary[ifIndex] = []
                nextInd = int(mappingDictionary[ifIndex][0])
                mappingDictionary[ifIndex].append(nextInd + 1)
            i += 1

        elif splits[i] == "return":
            mappingDictionary[statNum - 1] = "x"
            i += 2

        elif splits[i] == ';':
            if splits[i + 1] in doubles:
                i += 2
            i += 1

        reserved = i

    rows = len(statements)
    cols = 5
    liveVariable = [[0] * cols for _ in range(rows)]
    liveVariable[0][0] = "Statement"
    liveVariable[0][1] = "Define"
    liveVariable[0][2] = "Kill"
    liveVariable[0][3] = "Input"
    liveVariable[0][4] = "Output"

    opSplit = 0
    defines = ""
    kills = ""
    defDictionary = {}
    killDictionary = {}

    for key in statements.keys():
        if key != 0:
            if key not in defDictionary:
                defDictionary[key] = []
            if key not in killDictionary:
                killDictionary[key] = []
            if operationsSplit[opSplit] == "scanf":
                liveVariable[key][0] = str(key)
                liveVariable[key][1] = "{}"
                liveVariable[key][2] = "{" + operationsSplit[opSplit + 1] + "}"
                defDictionary[key].append("~")
                killDictionary[key].append(operationsSplit[opSplit + 1])

            elif operationsSplit[opSplit] == "printf":
                liveVariable[key][0] = str(key)
                liveVariable[key][1] = "{" + operationsSplit[opSplit + 1] + "}"
                liveVariable[key][2] = "{}"
                defDictionary[key].append(operationsSplit[opSplit + 1])
                killDictionary[key].append("~")

            elif operationsSplit[opSplit] in variables:
                liveVariable[key][0] = str(key)
                liveVariable[key][2] = "{" + operationsSplit[opSplit] + "}"
                killDictionary[key].append(operationsSplit[opSplit])
                while operationsSplit[opSplit] != '~':
                    opSplit += 1
                    if operationsSplit[opSplit] in doubles:
                        defDictionary[key].append(operationsSplit[opSplit - 1])
                        defines = defines + operationsSplit[opSplit - 1]
                        continue
                    if operationsSplit[opSplit] in variables:
                        if operationsSplit[opSplit] not in defines:
                            defDictionary[key].append(operationsSplit[opSplit])
                            if len(defines) == 0:
                                defines = defines + operationsSplit[opSplit]
                            else:
                                defines = defines + ", " + operationsSplit[opSplit]
                if len(defines) == 0:
                    defDictionary[key].append("~")
                liveVariable[key][1] = "{" + defines + "}"
                defines = ""

            elif operationsSplit[opSplit] == "if":
                liveVariable[key][0] = str(key)
                liveVariable[key][2] = "{}"
                killDictionary[key].append("~")
                while operationsSplit[opSplit] != '~':
                    opSplit += 1
                    if operationsSplit[opSplit] in variables:
                        if operationsSplit[opSplit] not in defines:
                            defDictionary[key].append(operationsSplit[opSplit])
                            if len(defines) == 0:
                                defines = defines + operationsSplit[opSplit]
                            else:
                                defines = defines + ", " + operationsSplit[opSplit]
                liveVariable[key][1] = "{" + defines + "}"
                defines = ""

            if opSplit >= len(operationsSplit) - 1:
                break
            while operationsSplit[opSplit] != '~':
                opSplit += 1
            if opSplit >= len(operationsSplit) - 1:
                break
            if operationsSplit[opSplit + 1] == '~':
                opSplit += 1
            opSplit += 1

    defs = []
    kills = []
    inputs = []
    outputs = []
    routes = []

    inputDictionary = {}
    outputDictionary = {}

    definiteList = []

    reservedKey = len(statements) - 1
    startKey = 0
    endKey = 0
    flag = 1
    iterationFlag = 0

    if definite == 1:
        print("================================================================================================")
        print("==============================Definite Live Variables analysis Started=========================")
        print("================================================================================================\n")
    else:
        print("================================================================================================")
        print("=============================Possible Live Variables analysis Started===========================")
        print("================================================================================================\n")

    while iterationFlag < 2:
        if iterationFlag == 1:
            print("****************************************First Iteration*****************************************")
            for row in liveVariable:
                formatted_row = ['{:<15}'.format(elem) for elem in row]
                print(formatted_row)
            reservedKey = startKey
            outputDictionary[reservedKey].remove("!")
        for key in reversed(sorted(statements.keys())):
            flag = 1
            key = reservedKey
            if iterationFlag == 1:
                if key == endKey - 1:
                    break
            if key > 0:
                if key not in inputDictionary:
                    inputDictionary[key] = []
                if key not in outputDictionary:
                    outputDictionary[key] = []
                if mappingDictionary[key] == "x":
                    liveVariable[key][3] = "{}"
                    inputDictionary[key].append("~")
                elif len(mappingDictionary[key]) > 1:
                    for route in mappingDictionary[key]:
                        if definite == 1:
                            if route not in outputDictionary:
                                for char in defDictionary[route]:
                                    if char in variables:
                                        if char in inputs:
                                            definiteList.append(char)
                                            continue
                                        else:
                                            inputs.append(char)
                            else:
                                for char in outputDictionary[route]:
                                    if char in variables:
                                        if char in inputs:
                                            definiteList.append(char)
                                            continue
                                        else:
                                            inputs.append(char)
                            if len(definiteList) != 0:
                                inputs.clear()
                                for item in definiteList:
                                    if item not in inputs:
                                        inputs.append(item)
                        else:
                            if route not in outputDictionary:
                                for char in defDictionary[route]:
                                    if char in variables:
                                        if char in inputs:
                                            definiteList.append(char)
                                            continue
                                        else:
                                            inputs.append(char)
                            else:
                                for char in outputDictionary[route]:
                                    if char in variables:
                                        if char in inputs:
                                            definiteList.append(char)
                                            continue
                                        else:
                                            inputs.append(char)
                    inString = ""
                    for ins in inputs:
                        inputDictionary[key].append(ins)
                        if len(inString) == 0:
                            inString = inString + ins
                        else:
                            inString = inString + ", " + ins
                    liveVariable[key][3] = "{" + inString + "}"
                else:
                    target = int(mappingDictionary[key][0])
                    if target in outputDictionary:
                        liveVariable[key][3] = liveVariable[target][4]
                        inputDictionary[key] = outputDictionary[target]
                        for char in inputDictionary[key]:
                            if char in variables:
                                inputs.append(char)
                    else:
                        outputDictionary[key].append("!")
                        reservedKey = mappingDictionary[key][0]
                        startKey = key
                        endKey = reservedKey + 1
                        flag = 0
                if flag:
                    for char in defDictionary[key]:
                        if char in variables:
                            defs.append(char)
                    for char in killDictionary[key]:
                        if char in variables:
                            kills.append(char)
                    for killed in kills:
                        if killed in inputs:
                            inputs.remove(killed)
                    for defined in defs:
                        if defined in inputs:
                            continue
                        else:
                            inputs.append(defined)
                    for outs in inputs:
                        outputs.append(outs)

                    outString = ""
                    for outs in outputs:
                        outputDictionary[key].append(outs)
                        if len(outString) == 0:
                            outString = outString + outs
                        else:
                            outString = outString + ", " + outs
                    liveVariable[key][4] = "{" + outString + "}"

                    defs.clear()
                    kills.clear()
                    inputs.clear()
                    outputs.clear()
                    reservedKey = key - 1
        if startKey == 0 and endKey == 0:
            break
        else:
            iterationFlag += 1

    print("\n======================================first Iteration===========================================")
    for row in liveVariable:
        formatted_row = ['{:<15}'.format(elem) for elem in row]
        print(formatted_row)


exampleFile = "test.c"
DataFlowAnalysis(exampleFile)
