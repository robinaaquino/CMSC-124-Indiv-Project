from lex import *
from objectDefinition import *
from utilityFunctions import *
from grammarErrorMessages import *
from tkinter import *
from tkinter import simpledialog
from math import *
import re

ListOfSymbols = []
ResultText = ""
ErrorLineNumber = 0 #updated whenever lexeme list is modified and there are still elements inside lexeme list

# Function that sets result text
# Modifies global variable
def add_error_result_text(errorMessage, lineNumber):
    global ResultText

    ResultText = errorMessage + "\nError at " + str(lineNumber)

# Function that checks if the lexeme list is empty
# Returns True or False
def lexeme_list_is_empty(lexemeList):
    global ErrorLineNumber

    if(len(lexemeList) == 0):
        return True
    else:
        return False

# Function that returns the data type of the value
# Returns data type
def return_data_type(value):
    dataTypeOfValue = "NOOB"

    if(value == "WIN" or value == "FAIL"): #if value is a string with troof values
        dataTypeOfValue = "TROOF"
    elif (isinstance(value, str)): #if value is a string
        if(value[0] == "\"" and value[-1] == "\""):
            dataTypeOfValue = "YARN"
        elif (re.match("(-?[0-9]*)\.[0-9]+", value)):
            dataTypeOfValue = "NUMBAR"
            value = float(value)
        elif (re.match("(-[1-9][0-9]*|[1-9][0-9]*|[0])", value)):
            dataTypeOfValue = "NUMBR"
            value = int(value)
    elif(isinstance(value, int)):
        dataTypeOfValue = "NUMBR"
    elif(isinstance(value, float)):
        dataTypeOfValue = "NUMBAR"

    return dataTypeOfValue

# Function get actual value for python from a value
# Returns actual value
def get_actual_value(value):
    dataTypeOfValue = return_data_type(value)

    if(dataTypeOfValue == "TROOF"):
        if(value == "WIN"):
            return True
        else:
            return False
    elif(dataTypeOfValue == "YARN"):
        return value[1:-1]
    else:
        return value

# Function to typecast a value to a data type
# Returns typecasted value
def typecast_value(value, newDataType):
    dataTypeOfValue = return_data_type(value)
    
    #convert value
    if (newDataType == "TROOF"): #convert value to troof
        if (dataTypeOfValue == "NOOB"): #if from noob
            return TypecastResult("FAIL", True)
        elif (dataTypeOfValue == "NUMBR" or dataTypeOfValue == "NUMBAR"): #if from numbr and numbar
            if (value != 0):
                return TypecastResult("WIN", True)
            else:
                return TypecastResult("FAIL", True)
        elif (dataTypeOfValue == "YARN"): #if from yarn
            value = value[1:-1] #remove quotations
            if(len(value) == 0):
                return TypecastResult("FAIL", True)
            else: 
                return TypecastResult("WIN", True)
        elif (dataTypeOfValue == "TROOF"):
            if(value == "WIN"):
                return TypecastResult("WIN", True)
            elif(value == "FAIL"):
                return TypecastResult("FAIL", True)
            else:
                return TypecastResult(value, "FAIL")
    elif (newDataType == "NUMBAR"): #convert value to numbar
        if (dataTypeOfValue == "NOOB"):
            return TypecastResult(0.0, True)
        elif (dataTypeOfValue == "NUMBR"):
            return TypecastResult(value + 0.0, True)
        elif (dataTypeOfValue == "YARN"):
            value = value[1:-1]
            if(value.isdigit()):
                return TypecastResult(float(value), True)
        elif (dataTypeOfValue == "TROOF"):
            if (value == "WIN"):
                return TypecastResult(1.0, True)
            elif (value == "FAIL"):
                return TypecastResult(0.0, True)
        elif (dataTypeOfValue == "NUMBAR"):
            return TypecastResult(float(value), True)
    elif (newDataType == "NUMBR"): #convert value to numbr
        if (dataTypeOfValue == "NOOB"):
            return TypecastResult(0, True)
        elif (dataTypeOfValue == "NUMBAR"):
            return TypecastResult(trunc(value), True)
        elif (dataTypeOfValue == "YARN"):
            value = value[1:-1]
            if(value.isdigit()):
                return TypecastResult(int(round(float(value), 2)), True)
        elif (dataTypeOfValue == "TROOF"):
            if (value == "WIN"):
                return TypecastResult(1, True)
            elif (value == "FAIL"):
                return TypecastResult(0, True)
        elif (dataTypeOfValue == "NUMBR"):
            return TypecastResult(value, True)
    elif (newDataType == "YARN"): # convert value to yarn
        if (dataTypeOfValue == "NOOB"):
            return TypecastResult("\"\"", True)
        elif (dataTypeOfValue == "NUMBR"):
            return TypecastResult("\"" + str(value) + "\"", True)
        elif (dataTypeOfValue == "NUMBAR"):
            return TypecastResult("\"" + str(round(value, 2)) + "\"", True)
        elif (dataTypeOfValue == "TROOF"):
            if (value == "WIN" or value == "FAIL"):
                return TypecastResult(("\"" + value + "\""), True)
        elif (dataTypeOfValue == "YARN"):
            return TypecastResult(value, True)

    return TypecastResult(value, False)

# Function that checks grammar of output
# Returns GrammarResult
def grammar_output_args(lexemeList, operationValue):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("output_args", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #check if grammar fit expr
    grammarExprResult: GrammarResult = grammar_expr(lexemeList)

    if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occured
        return grammarExprResult
    elif(if_grammar_matched(grammarExprResult)):
        typecastedValue = typecast_value(grammarExprResult.value, "YARN")

        if(typecastedValue.ifSuccess):
            operationValue += typecastedValue.value[1:-1]
            
            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("output_args", ErrorLineNumber, lexemeList, True, True, False, operationValue)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "New Line"):
                return set_grammar("output_args", ErrorLineNumber, lexemeList, True, True, False, operationValue)
        else:
            return set_grammar("output_args", ErrorLineNumber, lexemeList, True, False, False, operationValue)

    #check if grammar fit output_args
    grammarOutputArgsResult: GrammarResult = grammar_output_args(lexemeList, operationValue)

    if(if_grammar_has_error(grammarOutputArgsResult) or if_grammar_matched(grammarOutputArgsResult)): #if a syntax or symbol error occured
        return grammarOutputArgsResult

    return set_grammar("output_args", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of output
# Returns GrammarResult
def grammar_output(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("output", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Output"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

            return set_grammar("output", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        #check if grammar fit output_args
        grammarOutputArgsResult: GrammarResult = grammar_output_args(lexemeList, "")

        if(if_grammar_has_error(grammarOutputArgsResult)): #if a syntax or symbol error occured, or success
            return grammarOutputArgsResult
        elif(if_grammar_matched(grammarOutputArgsResult)):
            ResultText += grammarOutputArgsResult.value + "\n"
            return grammarOutputArgsResult

    return set_grammar("output", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of multiline_cmt2
# Returns GrammarResult
def grammar_multiline_cmt2(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is not empty
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #should match multiple comment lexemes
    while(lexemeList[0].classification == "Comment"):
        lexemeList.pop(0)

        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

    #if not matched with a comment, check if multiline_cmt2 end delimiter is there
    if(lexemeList[0].classification == "Multi-line Comment Delimiter End"):
        lexemeList.pop(0)

        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, True, True, False, None)

        if(lexemeList[0].classification == "New Line"):
            return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, True, True, False, None)
        else:
            #return success
            return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, True, False, False, None)
    
    else: #should have multi line comment delimiter end
        add_error_result_text(GrammarErrorMultilineCommentNoDelimiterEnd, ErrorLineNumber)

        return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, True, False, False, None)

# Function that checks grammar of multiline_cmt
# Returns GrammarResult
def grammar_multiline_cmt(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("multiline_cmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Multi-line Comment Delimiter Start"):
        lexemeList.pop(0)

        # check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("multiline_cmt", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarMultilineCmt2Result = grammar_multiline_cmt2(lexemeList)

        return grammarMultilineCmt2Result
    else:
        #should syntax error be true if ifFirstLexemeMatched is false
        grammarResult = set_grammar("multiline_cmt", ErrorLineNumber, lexemeList, False, False, False, None)

    return grammarResult

# Function that checks grammar of an_yarn
# Returns GrammarResult
def grammar_an_yarn(lexemeList, operationValue):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("an_yarn", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Expression AND Operator"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("an_yarn", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        #check if grammar fit expr
        grammarExprResult: GrammarResult = grammar_expr(lexemeList)

        if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occured
            return grammarExprResult
        elif(if_grammar_matched(grammarExprResult)):
            typecastedValue = typecast_value(grammarExprResult.value, "YARN")

            if(typecastedValue.ifSuccess):
                operationValue += typecastedValue.value[1:-1]
                
                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("an_yarn", ErrorLineNumber, lexemeList, True, True, False, operationValue)
                ErrorLineNumber = lexemeList[0].lineNumber

                if(lexemeList[0].classification == "New Line"):
                    return set_grammar("an_yarn", ErrorLineNumber, lexemeList, True, True, False, operationValue)
            else:
                return set_grammar("an_yarn", ErrorLineNumber, lexemeList, True, False, False, operationValue)

    #check if grammar fit output_args
    grammarAnYarnResult: GrammarResult = grammar_an_yarn(lexemeList, operationValue)

    if(if_grammar_has_error(grammarAnYarnResult) or if_grammar_matched(grammarAnYarnResult)): #if a syntax or symbol error occured
        return grammarAnYarnResult

    return set_grammar("an_yarn", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of str_concat
# Returns GrammarResult
def grammar_str_concat(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("str_concat", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    operationValue = ""
    if(lexemeList[0].classification == "Concatenation Operator"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

            return set_grammar("str_concat", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        #check if grammar fit expr
        grammarExprResult: GrammarResult = grammar_expr(lexemeList)

        if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occured
            return grammarExprResult
        elif(if_grammar_matched(grammarExprResult)):
            typecastedValue = typecast_value(grammarExprResult.value, "YARN")

            if(typecastedValue.ifSuccess):
                operationValue += typecastedValue.value[1:-1]
                
                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("str_concat", ErrorLineNumber, lexemeList, True, True, False, operationValue)
                ErrorLineNumber = lexemeList[0].lineNumber

                if(lexemeList[0].classification == "New Line"):
                    return set_grammar("str_concat", ErrorLineNumber, lexemeList, True, True, False, operationValue)
            else:
                return set_grammar("str_concat", ErrorLineNumber, lexemeList, True, False, False, operationValue)

        #check if grammar fit output_args
        grammarAnYarnResult: GrammarResult = grammar_an_yarn(lexemeList, operationValue)

        if(if_grammar_has_error(grammarAnYarnResult)): #if a syntax or symbol error occured, or success
            return grammarAnYarnResult
        elif(if_grammar_matched(grammarAnYarnResult)):
            return set_grammar("str_concat", ErrorLineNumber, lexemeList, True, True, False, grammarAnYarnResult.value)

    return set_grammar("str_concat", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of typecast_stmt
# Returns GrammarResult
def grammar_typecast_stmt(lexemeList):
    global ResultText
    global ErrorLineNumber

    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    identifierName = ""
    variableValue = None
    newType = ""
    if(lexemeList[0].classification == "Typecast Operator Start"):
        lexemeList.pop(0)

        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        if(lexemeList[0].classification == "Identifier"):
            identifierName = lexemeList[0].string
            lexemeList.pop(0)

            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            foundIdentifier = False
            #check if identifier exists in symbol table
            for symbolCounter in range(len(ListOfSymbols)):
                symbol = ListOfSymbols[symbolCounter]

                #set the value of the previous identifier
                if(symbol.identifier == identifierName):
                    foundIdentifier = True
                    variableValue = symbol.value
                    break

            if(foundIdentifier == False): #if identifier not found, implement
                add_error_result_text(GrammarErrorIdentifierNoIdentifierInSymbolTable, ErrorLineNumber)

                return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, True, True, None)

            if(lexemeList[0].classification == "Typecast Operator Mid"):
                lexemeList.pop(0)

                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "Type Literal"):
                newType = lexemeList[0].string
                lexemeList.pop(0)

                typecastedValue = typecast_value(variableValue, newType)

                if(typecastedValue.ifSuccess):
                    return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, True, False, typecastedValue.value)
                elif(typecastedValue.ifSuccess == False):
                    return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, True, True, typecastedValue.value)

    #return fail
    return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, False, False, False, None)


# Function that checks grammar of recast_stmt
# Returns GrammarResult
def grammar_recast_stmt(lexemeList):
    global ResultText
    global ErrorLineNumber

    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    identifierName = ""
    variableValue = None
    newType = ""
    variableCounter = 0
    if(lexemeList[0].classification == "Identifier"):
        identifierName = lexemeList[0].string
        identifierDetails = lexemeList[0]
        lexemeList.pop(0)

        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        foundIdentifier = False
        #check if identifier exists in symbol table
        for symbolCounter in range(len(ListOfSymbols)):
            symbol = ListOfSymbols[symbolCounter]

            #set the value of the previous identifier
            if(symbol.identifier == identifierName):
                variableCounter = symbolCounter
                foundIdentifier = True
                variableValue = symbol.value
                break

        if(foundIdentifier == False): #if identifier not found, implement
            add_error_result_text(GrammarErrorIdentifierNoIdentifierInSymbolTable, ErrorLineNumber)

            return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, True, True, True, None)

        if(lexemeList[0].classification == "Casting Operator"):
            lexemeList.pop(0)

            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "Type Literal"):
                newType = lexemeList[0].string
                lexemeList.pop(0)

                typecastedValue = typecast_value(variableValue, newType)

                if(typecastedValue.ifSuccess):
                    ListOfSymbols[variableCounter] = Symbol(identifierName, typecastedValue.value)

                    return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, True, False, typecastedValue.value)
                elif(typecastedValue.ifSuccess == False):
                    return set_grammar("typecast_stmt", ErrorLineNumber, lexemeList, True, True, True, typecastedValue.value)
        elif(lexemeList[0].classification == "Variable Assignment"):
            lexemeList.pop(0)

            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            #check if grammar fit input
            grammarTypecastStmtResult: GrammarResult = grammar_typecast_stmt(lexemeList)

            if(if_grammar_has_error(grammarTypecastStmtResult)): #if a syntax or symbol error occurred, or if successful
                return grammarTypecastStmtResult
            elif(if_grammar_matched(grammarTypecastStmtResult)):
                ListOfSymbols[variableCounter] = grammarTypecastStmtResult.value

                return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, True, True, False, None) 
        else:
            lexemeList.insert(0, identifierDetails)

    return set_grammar("recast_stmt", ErrorLineNumber, lexemeList, False, False, False, None) 


# Function that checks grammar of input
# Returns GrammarResult
def grammar_input(lexemeList):
    global ResultText
    global ErrorLineNumber
    global ListOfSymbols

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("input", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #check if it matches with input keyword
    if (lexemeList[0].classification == "Input"):
        lexemeList.pop(0)

        # check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("input", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        if (lexemeList[0].classification == "Identifier"):

            # check if identifier exists in symbol table
            for symbolCounter in range(len(ListOfSymbols)):
                symbol = ListOfSymbols[symbolCounter]
                #if identifier matches with lexeme identifier
                if(symbol.identifier == lexemeList[0].string):
                    UserInputValue = simpledialog.askstring("Input", symbol.identifier)

                    ListOfSymbols[symbolCounter].value = "\"" + UserInputValue + "\""

                    lexemeList.pop(0)

                    #return success for current grammar
                    return set_grammar("input", ErrorLineNumber, lexemeList, True, True, False, None)

            #if it found no identifier in the symbol table, return error
            grammarResult = set_grammar("input", ErrorLineNumber, lexemeList, True, True, True, None)

            add_error_result_text(GrammarErrorIdentifierNoIdentifierInSymbolTable, ErrorLineNumber)

        else:
            grammarResult = set_grammar("input", ErrorLineNumber, lexemeList, True, False, False, None)

            add_error_result_text(GrammarErrorIdentifierNoIdentifier, ErrorLineNumber)
    else:
        grammarResult = set_grammar("input", ErrorLineNumber, lexemeList, False, False, False, None)

    return grammarResult

# Function that checks grammar of variable_assignment
# Returns Grammar Result
def grammar_variable_assignment(lexemeList):
    global ResultText
    global ErrorLineNumber
    global ListOfSymbols

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Variable Declaration"):
        lexemeList.pop(0)

        #check if lexeme list empty before checking for future matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarErrorIdentifierNoIdentifier, ErrorLineNumber)

            return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, False, None)
            
        ErrorLineNumber = lexemeList[0].lineNumber

        if (lexemeList[0].classification == "Identifier"):
            identifierName = lexemeList[0].string
            identifierCounter = 0
            lexemeList.pop(0)

            for symbolCounter in range(len(ListOfSymbols)):
                symbol = ListOfSymbols[symbolCounter]

                #check if identifier already existed in symbol table
                if(symbol.identifier == identifierName):
                    # return fail
                    add_error_result_text(variable_error_already_existed(identifierName), ErrorLineNumber)

                    return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, True, None)
            
            #if identifier haven't existed, add to symbol table
            ListOfSymbols.append(Symbol(identifierName, None))
            identifierCounter = len(ListOfSymbols) - 1

            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

            if(lexemeList[0].classification == "Variable Declaration Assignment"):
                lexemeList.pop(0)

                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                if (lexemeList[0].classification == "Identifier"):
                    identifierName = lexemeList[0].string
                    lexemeList.pop(0)

                    #check if identifier exists in symbol table
                    for symbolCounter in range(len(ListOfSymbols)):
                        symbol = ListOfSymbols[symbolCounter]

                        #set the value of the previous identifier
                        if(symbol.identifier == identifierName):
                            ListOfSymbols[identifierCounter].value = ListOfSymbols[symbolCounter].value

                            #return success for current grammar
                            return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

                    #if not symbol error
                    add_error_result_text(variable_error_missing(identifierName), ErrorLineNumber)
                    
                    return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)
                
                #check for match with literal
                grammarLiteralResult: GrammarResult = grammar_literal(lexemeList)

                #if grammar fit literal
                if(if_grammar_has_error(grammarLiteralResult)): #if a syntax or symbol error occurred
                    return grammarLiteralResult
                elif(if_grammar_matched(grammarLiteralResult)): #if successfully matched
                    ListOfSymbols[identifierCounter].value = grammarLiteralResult.value #update value

                    return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

                #check for match with expr
                grammarExprResult = grammar_expr(lexemeList)

                #if grammar fit expr
                if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occurred
                    return grammarExprResult
                elif(if_grammar_matched(grammarExprResult)): #if successfully matched
                    ListOfSymbols[identifierCounter].value = grammarExprResult.value #update value

                    return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

                #return grammar fail
                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, False, None)
            else: #if not matched
                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

        else:
            add_error_result_text(GrammarErrorIdentifierNoIdentifier, ErrorLineNumber)
            
            return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, False, None)

    elif(lexemeList[0].classification == "Identifier"):
        identifierName = lexemeList[0].string
        identifierCounter = 0
        doesExist = False
        identifierDetails = lexemeList.pop(0)

        for symbolCounter in range(len(ListOfSymbols)): #check if identifier exists in symbol table
            symbol = ListOfSymbols[symbolCounter]

            #check if identifier exists
            if(symbol.identifier == identifierName):
                doesExist = True
                identifierCounter = symbolCounter
                break
                
        if(doesExist == False): #if identifier doesn't exist in lexeme table, return fail
            add_error_result_text(variable_error_missing(identifierName), ErrorLineNumber)

            return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, True, None)

        #check if lexeme list empty before checking for future matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarErrorVariableAssignmentKeywordMissing, ErrorLineNumber)

            return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        if(lexemeList[0].classification == "Variable Assignment"):
            lexemeList.pop(0)

            #check if lexeme list empty before checking for future matches
            if(lexeme_list_is_empty(lexemeList)):
                add_error_result_text(GrammarErrorMissingValue, ErrorLineNumber)

                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, False, False, None)

            if (lexemeList[0].classification == "Identifier"):
                identifierName = lexemeList[0].string
                lexemeList.pop(0)

                #check if identifier exists in symbol table
                for symbolCounter in range(len(ListOfSymbols)):
                    symbol = ListOfSymbols[symbolCounter]

                    #set the value of the previous identifier
                    if(symbol.identifier == identifierName):
                        ListOfSymbols[identifierCounter].value = ListOfSymbols[symbolCounter].value

                        #return success for current grammar
                        return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

                #if not symbol error
                add_error_result_text(variable_error_missing(identifierName), ErrorLineNumber)
                
                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)
            
            #check for match with literal
            grammarLiteralResult: GrammarResult = grammar_literal(lexemeList)

            #if grammar fit literal
            if(if_grammar_has_error(grammarLiteralResult)): #if a syntax or symbol error occurred
                return grammarLiteralResult
            elif(if_grammar_matched(grammarLiteralResult)): #if successfully matched
                ListOfSymbols[identifierCounter].value = grammarLiteralResult.value #update value

                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

            #check for match with expr
            grammarExprResult = grammar_expr(lexemeList)

            #if grammar fit expr
            if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occurred
                return grammarExprResult
            elif(if_grammar_matched(grammarExprResult)): #if successfully matched
                ListOfSymbols[identifierCounter].value = grammarExprResult.value #update value

                return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)
        else:
            lexemeList.insert(0, identifierDetails)
    #return fail
    return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of literal
# Returns GrammarResult
def grammar_literal(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("multiline_cmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Numbr Literal"):
        grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, int(lexemeList[0].string))

        lexemeList.pop(0)

        #return success for current grammar
        return grammarResult
    elif (lexemeList[0].classification == "Numbar Literal"):
        grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, float(lexemeList[0].string))

        lexemeList.pop(0)

        #return success for current grammar
        return grammarResult
    elif(lexemeList[0].classification == "Yarn Literal"):
        grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, lexemeList[0].string)

        lexemeList.pop(0)

        #return success for current grammar
        return grammarResult
    elif(lexemeList[0].classification == "Troof Literal"):
        if(lexemeList[0].string == "WIN"):
            grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, "WIN")
        else:
            grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, "FAIL")

        lexemeList.pop(0)

        return grammarResult
    else:
        grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, False, False, False, None)
    
    return grammarResult

# Function that checks grammar of binary_bool_operator
# Returns GrammarResult
def grammar_binary_bool_operator(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Boolean Operator"):
        operationValue = None
        operatorValue = lexemeList[0].string

        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

            return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarBinaryExp1Result = grammar_binary_exp(lexemeList)

        #if grammar fit binary_exp
        if (if_grammar_has_error(grammarBinaryExp1Result)): #if error
            return grammarBinaryExp1Result

        elif (if_grammar_matched(grammarBinaryExp1Result)): #if successful
            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                add_error_result_text(GrammarExprNoAnKeyword, ErrorLineNumber)

                return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "Expression AND Operator"):
                lexemeList.pop(0)

                grammarBinaryExp2Result = grammar_binary_exp(lexemeList)

                #if grammar fit binary_exp
                if (if_grammar_has_error(grammarBinaryExp2Result)): #if error
                    return grammarBinaryExp2Result
                elif (if_grammar_matched(grammarBinaryExp2Result)): #if successful
                    #parse the results given the operator and the values of the operands
                    firstOperandType = return_data_type(grammarBinaryExp1Result.value)
                    secondOperandType = return_data_type(grammarBinaryExp2Result.value)

                    firstOperand = grammarBinaryExp1Result.value
                    secondOperand = grammarBinaryExp2Result.value

                    if(firstOperandType != "TROOF" or secondOperandType != "TROOF"):
                        firstOperand = typecast_value(firstOperand, "TROOF")
                        secondOperand = typecast_value(secondOperand, "TROOF")
                    
                    if(firstOperand.ifSuccess == False or secondOperand.ifSuccess == False):
                        if(firstOperand.ifSuccess == False):
                            add_error_result_text(typecast_error(grammarBinaryExp1Result.value, "TROOF"), ErrorLineNumber)
                        elif(secondOperand.ifSuccess == False):
                            add_error_result_text(typecast_error(grammarBinaryExp2Result.value, "TROOF"), ErrorLineNumber)

                        return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)
                    
                    firstOperand = get_actual_value(firstOperand.value)
                    secondOperand = get_actual_value(secondOperand.value)
                        
                    #if no error in typecast, proceed with operation
                    if(operatorValue == "BOTH OF"):
                        operationValue = firstOperand and secondOperand
                    elif(operatorValue == "EITHER OF"):
                        operationValue = firstOperand or secondOperand
                    elif(operatorValue == "WON OF"):
                        operationValue = (firstOperand and not secondOperand) or (not firstOperand and secondOperand)

                    #typecast value back to TROOF
                    operationValue = typecast_value(operationValue, "TROOF")

                    if(operationValue.ifSuccess == False):
                        add_error_result_text(typecast_error(operationValue.value, "TROOF"), ErrorLineNumber)
                        return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)
                    
                    operationValue = operationValue.value

                    #return success
                    return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)

    return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of binary_math_operator
# Returns GrammarResult
def grammar_binary_math_operator(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, False, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Arithmetic Math Operator" or lexemeList[0].classification == "Comparison Math Operator"):
        operationValue = None
        operatorValue = lexemeList[0].string

        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

            return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarBinaryExp1Result = grammar_binary_exp(lexemeList)

        #if grammar fit binary_exp
        if (if_grammar_has_error(grammarBinaryExp1Result)): #if error
            return grammarBinaryExp1Result
        elif (if_grammar_matched(grammarBinaryExp1Result)): #if successful
            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                add_error_result_text(GrammarExprNoAnKeyword, ErrorLineNumber)

                return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "Expression AND Operator"):
                lexemeList.pop(0)

                grammarBinaryExp2Result = grammar_binary_exp(lexemeList)

                #if grammar fit binary_exp
                if (if_grammar_has_error(grammarBinaryExp2Result)): #if error
                    return grammarBinaryExp2Result
                elif (if_grammar_matched(grammarBinaryExp2Result)): #if successful
                    #parse the results given the operator and the values of the operands
                    operationResultType = "NEITHER"

                    firstOperandType = return_data_type(grammarBinaryExp1Result.value)
                    secondOperandType = return_data_type(grammarBinaryExp2Result.value)

                    firstOperand = grammarBinaryExp1Result.value
                    secondOperand = grammarBinaryExp2Result.value

                    if(firstOperandType == "NUMBAR" or secondOperandType == "NUMBAR"):
                        operationResultType = "NUMBAR"
                        firstOperand = typecast_value(firstOperand, operationResultType)
                        secondOperand = typecast_value(secondOperand, operationResultType)
                    elif (firstOperandType == "NUMBR" and secondOperandType == "NUMBR"):
                        operationResultType = "NUMBR"
                        firstOperand = typecast_value(firstOperand, operationResultType)
                        secondOperand = typecast_value(secondOperand, operationResultType)
                    else:
                        firstOperand = typecast_value(firstOperand, "NUMBAR")
                        secondOperand = typecast_value(secondOperand, "NUMBAR")
                    
                    if(firstOperand.ifSuccess == False or secondOperand.ifSuccess == False):
                        if(firstOperand.ifSuccess == False):
                            add_error_result_text(typecast_error(grammarBinaryExp1Result.value, operationResultType), ErrorLineNumber)
                        elif(secondOperand.ifSuccess == False):
                            add_error_result_text(typecast_error(grammarBinaryExp2Result.value, operationResultType), ErrorLineNumber)

                        return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)
                    
                    firstOperand = get_actual_value(firstOperand.value)
                    secondOperand = get_actual_value(secondOperand.value)
                        
                    #if no error in typecast, proceed with operation
                    if(operatorValue == "SUM OF"):
                        operationValue = firstOperand + secondOperand
                    elif(operatorValue == "DIFF OF"):
                        operationValue = firstOperand - secondOperand
                    elif(operatorValue == "PRODUKT OF"):
                        operationValue = firstOperand * secondOperand
                    elif(operatorValue == "QUOSHUNT OF"):
                        operationValue = firstOperand / secondOperand
                    elif(operatorValue == "MOD OF"):
                        operationValue = firstOperand % secondOperand
                    elif(operatorValue == "BIGGR OF"):
                        operationValue = max(firstOperand, secondOperand)
                    elif(operatorValue == "SMALLR OF"):
                        operationValue = max(firstOperand, secondOperand)

                    if(operationResultType == "NEITHER"): #parse to numbr if possible
                        if(((operationValue * 10) % 10) == 0):
                            result = typecast_value(operationValue, "NUMBR")
                            if(result.ifSuccess):
                                operationValue = get_actual_value(result.value)
                            else:
                                add_error_result_text(typecast_error(result.value, operationResultType), ErrorLineNumber)

                                return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)

                    #return success

                    return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)

    return grammarResult

# Function that checks grammar of binary_exp
# Returns GrammarResult
def grammar_binary_exp(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, False, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("binary_exp", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #if grammar fit literal
    grammarLiteralResult: GrammarResult = grammar_literal(lexemeList)

    if(if_grammar_has_error(grammarLiteralResult) or if_grammar_matched(grammarLiteralResult)): #if a syntax or symbol error occurred, or if successful
        return grammarLiteralResult

    if(lexemeList[0].classification == "Identifier"):
        identifierName = lexemeList[0].string
        lexemeList.pop(0)

        for symbolCounter in range(len(ListOfSymbols)):
            symbol = ListOfSymbols[symbolCounter]

            #check if identifier exists in symbolCounter
            if(symbol.identifier == identifierName):
                # return success
                return set_grammar("binary_exp", ErrorLineNumber, lexemeList, True, True, False, symbol.value)

    #if grammar fit binary_math_operator
    grammarMathOperatorResult: GrammarResult = grammar_binary_math_operator(lexemeList)

    if(if_grammar_has_error(grammarMathOperatorResult) or if_grammar_matched(grammarMathOperatorResult)): #if a syntax or symbol error occurred, or if successful
        return grammarMathOperatorResult

    #if grammar fit binary_bool_operator
    grammarBoolOperatorResult: GrammarResult = grammar_binary_bool_operator(lexemeList)

    if(if_grammar_has_error(grammarBoolOperatorResult) or if_grammar_matched(grammarBoolOperatorResult)): #if a syntax or symbol error occurred, or if successful
        return grammarBoolOperatorResult

    #match with comparison operations
    grammarComparisonOperationsResult: GrammarResult = grammar_comparison_operator(lexemeList)

    if(if_grammar_has_error(grammarComparisonOperationsResult) or if_grammar_matched(grammarComparisonOperationsResult)): #if a syntax or symbol error occurred, or if successful
        return grammarComparisonOperationsResult

    #return fail
    return set_grammar("binary_exp", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of infinite_arity_expr_end2
# Returns GrammarResult
def grammar_infinite_arity_expr_end2(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("infinite_arity_expr_end2", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    # match with an, then expr
    if (lexemeList[0].classification == "Expression AND Operator"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarInfiniteArityExpNoOperand, ErrorLineNumber)

            return set_grammar("infinite_arity_expr", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber
        
        grammarBoolExpResult = grammar_infinite_arity_expr_operand(lexemeList)

        #if grammar fit bool_expr
        if (if_grammar_has_error(grammarBoolExpResult) or if_grammar_matched(grammarBoolExpResult)): #if error or success
            return grammarBoolExpResult

    # return fail
    return set_grammar("infinite_arity_expr_end2", ErrorLineNumber, lexemeList, False, False, False, None)
    
# Function that checks grammar of infinite_arity_expr_end1 
# Returns GrammarResult
def grammar_infinite_arity_expr_end1(lexemeList, operatorValue, operationValue):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("infinite_arity_expr_end1", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    while True: #loop as long as it matches grammar for infinite_arity_expr_end2
        grammarInfiniteArityExprEnd2Result: GrammarResult = grammar_infinite_arity_expr_end2(lexemeList)

        if(if_grammar_matched(grammarInfiniteArityExprEnd2Result)): #if successful
            if(operatorValue == "ALL OF"): #update operation value
                operationValue = operationValue and grammarInfiniteArityExprEnd2Result.value
            elif(operatorValue == "AND OF"):
                operationValue = operationValue or grammarInfiniteArityExprEnd2Result.value
            continue

        break

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("infinite_arity_expr_end1", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if (lexemeList[0].classification == "Infinite Arity Delimiter End"): #check if ended with a delimiter
        lexemeList.pop(0)
        return set_grammar("infinite_arity_expr_end2", ErrorLineNumber, lexemeList, True, True, False, operationValue)
    else:
        add_error_result_text(GrammarInfiniteArityMKAYKeyword, ErrorLineNumber)

        # return fail
        return set_grammar("infinite_arity_expr_end1", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of infinite_arity_expr
# Returns GrammarResult
def grammar_infinite_arity_expr(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, False, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("infinite_arity_expr", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Infinite Boolean Operator"):
        operationValue = None
        operatorValue = lexemeList[0].string

        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

            return set_grammar("infinite_arity_expr", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarInfiniteArityExprOperand1Result = grammar_infinite_arity_expr_operand(lexemeList)

        #if grammar fit bool_expr
        if (if_grammar_has_error(grammarInfiniteArityExprOperand1Result)): #if error
            return grammarInfiniteArityExprOperand1Result
        elif (if_grammar_matched(grammarInfiniteArityExprOperand1Result)): #if successful
            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                add_error_result_text(GrammarInfiniteArityExpNoOperand, ErrorLineNumber)

                return set_grammar("infinite_arity_expr", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            lexemeList.pop(0)

            grammarInfiniteArityExprOperand2Result = grammar_infinite_arity_expr_operand(lexemeList)

            #if grammar fit binary_exp
            if (if_grammar_has_error(grammarInfiniteArityExprOperand2Result)): #if error
                return grammarInfiniteArityExprOperand2Result
            elif (if_grammar_matched(grammarInfiniteArityExprOperand2Result)): #if successful
                #parse the results given the operator and the values of the operands
                firstOperandType = return_data_type(grammarInfiniteArityExprOperand1Result.value)
                secondOperandType = return_data_type(grammarInfiniteArityExprOperand2Result.value)

                firstOperand = typecast_value(grammarInfiniteArityExprOperand1Result.value, "TROOF")
                secondOperand = typecast_value(grammarInfiniteArityExprOperand2Result.value, "TROOF")
                
                if(firstOperand.ifSuccess == False or secondOperand.ifSuccess == False):
                    if(firstOperand.ifSuccess == False):
                        add_error_result_text(typecast_error(grammarInfiniteArityExprOperand1Result.value, "TROOF"), ErrorLineNumber)
                    elif(secondOperand.ifSuccess == False):
                        add_error_result_text(typecast_error(grammarInfiniteArityExprOperand2Result.value, "TROOF"), ErrorLineNumber)

                    return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)
                
                firstOperand = get_actual_value(firstOperand.value)
                secondOperand = get_actual_value(secondOperand.value)
                    
                #if no error in typecast, proceed with operation
                if(operatorValue == "ALL OF"):
                    operationValue = firstOperand and secondOperand
                elif(operatorValue == "AND OF"):
                    operationValue = firstOperand or secondOperand

                #should match infinite_arity_expr_end1 or else fail
                grammarInfiniteArityExprEnd1Result: GrammarResult = grammar_infinite_arity_expr_end1(lexemeList, operatorValue, operationValue)

                if(if_grammar_has_error(grammarInfiniteArityExprEnd1Result)): #if a syntax or symbol error occurred 
                    #return fail
                    return grammarInfiniteArityExprEnd1Result
                
                if(if_grammar_matched(grammarInfiniteArityExprEnd1Result) and grammarInfiniteArityExprEnd1Result.value != None):
                    #if success, update operation value
                    operationValue = grammarInfiniteArityExprEnd1Result.value

                #typecast value back to TROOF
                operationValue = typecast_value(operationValue, "TROOF")

                if(operationValue.ifSuccess == False):
                    add_error_result_text(typecast_error(operationValue.value, "TROOF"), ErrorLineNumber)
                    return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)
                
                operationValue = operationValue.value

                return set_grammar("infinite_arity_expr", ErrorLineNumber, lexemeList, True, True, False, operationValue)
                    

    return set_grammar("infinite_arity_expr", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of comparison_operator
# Returns GrammarResult
def grammar_comparison_operator(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Comparison Operator"):
        operationValue = None
        operatorValue = lexemeList[0].string

        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

            #return error due to matching some lexeme but not all
            return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarExp1Result = grammar_expr(lexemeList)

        #if grammar fit exp
        if (if_grammar_has_error(grammarExp1Result)): #if error
            return grammarExp1Result
            
        elif (if_grammar_matched(grammarExp1Result)):

            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                add_error_result_text(GrammarExprNoAnKeyword, ErrorLineNumber)

                return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            #match with an
            if(lexemeList[0].classification == "Expression AND Operator"):
                lexemeList.pop(0)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

                    return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                if(lexemeList[0].classification == "Comparison Math Operator"): #parse as relational operations
                    relationalOperatorValue = lexemeList[0].string
                    lexemeList.pop(0)

                    #check if lexeme list is empty before checking for further matches
                    if(lexeme_list_is_empty(lexemeList)):
                        add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

                        return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)
                    ErrorLineNumber = lexemeList[0].lineNumber

                    #check for expr, should be equal to grammarExp1Result
                    grammarExp1RelationalResult = grammar_expr(lexemeList)

                    if (if_grammar_has_error(grammarExp1RelationalResult)): #if error
                        return grammarExp1RelationalResult
                    elif (if_grammar_matched(grammarExp1RelationalResult)):
                        #check if lexeme list is empty before checking for further matches
                        if(lexeme_list_is_empty(lexemeList)):
                            add_error_result_text(GrammarExprNoAnKeyword, ErrorLineNumber)

                            return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)
                        ErrorLineNumber = lexemeList[0].lineNumber

                        #if current value is not equivalent to previous value, return error
                        if(grammarExp1RelationalResult.value != grammarExp1Result.value):
                            add_error_result_text(GrammarComparisonOperationUnequalValue, ErrorLineNumber)
                            return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)

                        #if equal, check for AN
                        if(lexemeList[0].classification == "Expression AND Operator"):
                            lexemeList.pop(0)

                            #check if lexeme list is empty before checking for further matches
                            if(lexeme_list_is_empty(lexemeList)):
                                add_error_result_text(GrammarBinaryExpNoOperand, ErrorLineNumber)

                                return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)
                            ErrorLineNumber = lexemeList[0].lineNumber

                            #check for second operand
                            grammarExp2RelationalResult = grammar_expr(lexemeList)
                            
                            if (if_grammar_has_error(grammarExp2RelationalResult)): #if error
                                return grammarExp2RelationalResult
                            elif (if_grammar_matched(grammarExp2RelationalResult)): #parse the result
                                firstOperand = grammarExp1RelationalResult.value
                                secondOperand = grammarExp2RelationalResult.value

                                try:
                                    #check for comparison operator
                                    if(operatorValue == "BOTH SAEM"):
                                        #check for relational operations
                                        if(relationalOperatorValue == "BIGGR OF"):
                                            operationValue = firstOperand >= secondOperand
                                        elif(relationalOperatorValue == "SMALLR OF"):
                                            operationValue = firstOperand <= secondOperand
                                    elif(operatorValue == "DIFFRINT"):
                                        #check for relational operations
                                        if(relationalOperatorValue == "BIGGR OF"):
                                            operationValue = firstOperand > secondOperand
                                        elif(relationalOperatorValue == "SMALLR OF"):
                                            operationValue = firstOperand < secondOperand
                                except: #if error in value, return error
                                    add_error_result_text(GrammarComparisonOperationParseError, ErrorLineNumber)

                                    return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)

                                #return success
                                return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)
        
                        #return fail, expected an
                        else:
                            add_error_result_text(GrammarExprNoAnKeyword, ErrorLineNumber)

                            return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)

                else: #parse as equality or inequality
                    grammarExp2Result = grammar_expr(lexemeList)

                    if(if_grammar_matched(grammarExp2Result)): #if success, parse result with no typecasting
                        firstOperand = grammarExp1Result.value
                        secondOperand = grammarExp2Result.value

                        try:
                            if(operatorValue == "BOTH SAEM"):
                                operationValue = firstOperand == secondOperand
                            elif(operatorValue == "DIFFRINT"):
                                operationValue = firstOperand != secondOperand
                        except: #if error in value, return error
                            add_error_result_text(GrammarComparisonOperationParseError, ErrorLineNumber)

                            return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)

                        #return success
                        return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)

                    elif(if_grammar_has_error(grammarExp2Result)): #if there's an error
                        return grammarExp2Result

                
                return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, True, False, False, None)

    #return unmatched for current grammar  
    return set_grammar("comparison_operator", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of bool_expr
# Returns GrammarResult
def grammar_bool_expr(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("bool_expr", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #match with NOT lexeme
    if(lexemeList[0].classification == "Not Boolean Operator"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("bool_expr", ErrorLineNumber, lexemeList, False, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarExprResult = grammar_expr(lexemeList)

        #if grammar fit expr
        if(if_grammar_has_error(grammarExprResult)):
            return grammarExprResult
        elif(if_grammar_matched(grammarExprResult)):
            firstOperandType = return_data_type(grammarExprResult.value)

            firstOperand = grammarExprResult.value

            if(firstOperandType != "TROOF"):
                firstOperand = typecast_value(firstOperand, "TROOF")

            if(firstOperand.ifSuccess == False):
                add_error_result_text(typecast_error(grammarExprResult.value, "TROOF"), ErrorLineNumber)

                return set_grammar("bool_expr", ErrorLineNumber, lexemeList, True, True, True, operationValue)
            
            firstOperand = firstOperand.value

            operationValue = not firstOperand

            return set_grammar("bool_expr", ErrorLineNumber, lexemeList, True, True, False, operationValue)

    #match with binary_exp
    grammarBinaryExpResult: GrammarResult = grammar_binary_exp(lexemeList)

    #if grammar fit input
    if(if_grammar_has_error(grammarBinaryExpResult) or if_grammar_matched(grammarBinaryExpResult)): #if a syntax or symbol error occurred, or if successful
        return grammarBinaryExpResult

    #default error catch if it did not match any
    grammarResult = GrammarResult("bool_expr", ErrorLineNumber, lexemeList, False, False, False, None)
    return grammarResult

# Function that checks grammar of infinite_arity_expr_operand
# Returns GrammarResult
def grammar_infinite_arity_expr_operand(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("infinite_arity_expr_operand", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #match with binary_exp
    grammarBinaryExpResult: GrammarResult = grammar_binary_exp(lexemeList)

    #if grammar fit input
    if(if_grammar_has_error(grammarBinaryExpResult) or if_grammar_matched(grammarBinaryExpResult)): #if a syntax or symbol error occurred, or if successful
        return grammarBinaryExpResult

    #match with NOT lexeme
    if(lexemeList[0].classification == "Not Boolean Operator"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("infinite_arity_expr_operand", ErrorLineNumber, lexemeList, False, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarInfiniteArityExprOperandResult = grammar_infinite_arity_expr_operand(lexemeList)

        #if grammar fit expr
        if(if_grammar_has_error(grammarInfiniteArityExprOperandResult)):
            return grammarInfiniteArityExprOperandResult
        elif(if_grammar_matched(grammarInfiniteArityExprOperandResult)):
            firstOperandType = return_data_type(grammarInfiniteArityExprOperandResult.value)

            firstOperand = grammarInfiniteArityExprOperandResult.value

            if(firstOperandType != "TROOF"):
                firstOperand = typecast_value(firstOperand, "TROOF")

            if(firstOperand.ifSuccess == False):
                add_error_result_text(typecast_error(grammarInfiniteArityExprOperandResult.value, "TROOF"), ErrorLineNumber)

                return set_grammar("infinite_arity_expr_operand", ErrorLineNumber, lexemeList, True, True, True, operationValue)
            
            firstOperand = firstOperand.value

            operationValue = not firstOperand

            return set_grammar("infinite_arity_expr_operand", ErrorLineNumber, lexemeList, True, True, False, operationValue)

    #default error catch if it did not match any
    grammarResult = GrammarResult("infinite_arity_expr_operand", ErrorLineNumber, lexemeList, False, False, False, None)
    return grammarResult

# Function that checks grammar of expr
# Returns GrammarResult
def grammar_expr(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("expr", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #match with str_concat
    grammarStrConcatResult: GrammarResult = grammar_str_concat(lexemeList)

    if(if_grammar_has_error(grammarStrConcatResult) or if_grammar_matched(grammarStrConcatResult)): #if a syntax or symbol error occurred, or if successful
        return grammarStrConcatResult

    #match with typecast_stmt
    grammarTypecastStmt: GrammarResult = grammar_typecast_stmt(lexemeList)

    if(if_grammar_has_error(grammarTypecastStmt) or if_grammar_matched(grammarTypecastStmt)): #if a syntax or symbol error occurred, or if successful
        return grammarTypecastStmt

    #match with binary_exp
    grammarBoolExpResult: GrammarResult = grammar_bool_expr(lexemeList)

    if(if_grammar_has_error(grammarBoolExpResult) or if_grammar_matched(grammarBoolExpResult)): #if a syntax or symbol error occurred, or if successful
        return grammarBoolExpResult

    #match with infinite arity expr
    grammarInfiniteArityExpr: GrammarResult = grammar_infinite_arity_expr(lexemeList)

    if(if_grammar_has_error(grammarInfiniteArityExpr) or if_grammar_matched(grammarInfiniteArityExpr)): #if a syntax or symbol error occurred, or if successful
        return grammarInfiniteArityExpr

    #default error catch if it did not match any
    grammarResult = GrammarResult("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    return grammarResult

# Function that checks grammar of cond_stmt
# Returns Grammar Result
def grammar_cond_stmt(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    exprLexemeList = [] #use a temporary list in case it is not a conditional statement
    for item in lexemeList:
        exprLexemeList.append(item)

    #check if grammar fit expr
    grammarExprResult: GrammarResult = grammar_expr(exprLexemeList)


    if(if_grammar_has_error(grammarExprResult)): #if resulted in error, return result
        return grammarExprResult

    if(if_grammar_matched(grammarExprResult)): #if success
        #save value to IT
        typecastToTroof = typecast_value(grammarExprResult.value, "TROOF")
        troofValue = typecastToTroof.value

        if(typecastToTroof.ifSuccess == False): #return error if error in typecasting
            add_error_result_text(typecast_error(grammarExprResult.value, "TROOF"), ErrorLineNumber)
            return set_grammar("cond_stmt", ErrorLineNumber, exprLexemeList, True, True, True, None)

        foundIdentifier = False
        #check if identifier exists in symbol table
        for symbolCounter in range(len(ListOfSymbols)):
            symbol = ListOfSymbols[symbolCounter]

            #set the value of the previous identifier
            if(symbol.identifier == "IT"):
                ListOfSymbols[symbolCounter].value = troofValue
                foundIdentifier = True

        if(foundIdentifier == False): #if identifier not found, implement
            ListOfSymbols.append(Symbol("IT", troofValue))

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(exprLexemeList)): #no error, since expr can stand alone
            return set_grammar("cond_stmt", ErrorLineNumber, exprLexemeList, False, False, False, None)
        ErrorLineNumber = exprLexemeList[0].lineNumber

        if(exprLexemeList[0].classification == "New Line"):
            exprLexemeList.pop(0)

            #check if lexeme list is empty before checking for further matches, go back since it should match with expr not cond_stmt
            if(lexeme_list_is_empty(exprLexemeList)):
                return set_grammar("cond_stmt", ErrorLineNumber, exprLexemeList, False, False, False, None)
            ErrorLineNumber = exprLexemeList[0].lineNumber


            if(exprLexemeList[0].classification == "Conditional Delimiter If Else Start"): #start of cond_stmt
                lexemeList.clear() #recopy the modified list back to original list
                for item in exprLexemeList:
                    lexemeList.append(item)

                lexemeList.pop(0)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                if(lexemeList[0].classification == "New Line"):
                    lexemeList.pop(0)

                    #check if lexeme list is empty before checking for further matches
                    if(lexeme_list_is_empty(lexemeList)):
                        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                    ErrorLineNumber = lexemeList[0].lineNumber

                    if(lexemeList[0].classification == "Conditional If"):
                        lexemeList.pop(0)

                        #check if lexeme list is empty before checking for further matches
                        if(lexeme_list_is_empty(lexemeList)):
                            return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                        ErrorLineNumber = lexemeList[0].lineNumber

                        if(lexemeList[0].classification == "New Line"):
                            lexemeList.pop(0)

                            #check if lexeme list is empty before checking for further matches
                            if(lexeme_list_is_empty(lexemeList)):
                                return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                            ErrorLineNumber = lexemeList[0].lineNumber

                            ifListOfLexeme = []
                            while(lexeme_list_is_empty(lexemeList) == False):
                                if(lexemeList[0].classification == "Conditional Else"): 

                                    #check if lexeme list is empty before checking for further statements, still a success for grammar
                                    if(lexeme_list_is_empty(lexemeList)):
                                        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                                    ErrorLineNumber = lexemeList[0].lineNumber

                                    break
                                elif(lexemeList[0].classification == "Conditional Delimiter End"): 
                                    lexemeList.pop(0)

                                    #check if lexeme list is empty before checking for further statements, still a success for grammar
                                    if(lexeme_list_is_empty(lexemeList)):
                                        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, True, False, None)
                                    ErrorLineNumber = lexemeList[0].lineNumber

                                    return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, True, False, None)

                                ifListOfLexeme.append(lexemeList[0])
                                lexemeList.pop(0)
                                
                            if(troofValue == "WIN"):
                                grammarIfStmtResult: GrammarResult = grammar_stmt(ifListOfLexeme)

                                if(if_grammar_has_error(grammarIfStmtResult)): #if a syntax or symbol error occurred, or if successful
                                    return grammarIfStmtResult

                            if(lexemeList[0].classification == "Conditional Else"):
                                lexemeList.pop(0)

                                #check if lexeme list is empty before checking for further matches
                                if(lexeme_list_is_empty(lexemeList)):
                                    return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                                ErrorLineNumber = lexemeList[0].lineNumber

                                if(lexemeList[0].classification == "New Line"):
                                    lexemeList.pop(0)

                                    #check if lexeme list is empty before checking for further matches
                                    if(lexeme_list_is_empty(lexemeList)):
                                        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                                    ErrorLineNumber = lexemeList[0].lineNumber
                                        
                                    elseListOfLexeme = []
                                    while(lexeme_list_is_empty(lexemeList) == False):
                                        if(lexemeList[0].classification == "Conditional Delimiter End"): 

                                            #check if lexeme list is empty before checking for further statements
                                            if(lexeme_list_is_empty(lexemeList)):
                                                return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                                            ErrorLineNumber = lexemeList[0].lineNumber

                                            break

                                        elseListOfLexeme.append(lexemeList[0])
                                        lexemeList.pop(0)
                                    
                                    if(troofValue == "FAIL"):
                                        grammarElseStmtResult: GrammarResult = grammar_stmt(elseListOfLexeme)

                                        if(if_grammar_has_error(grammarElseStmtResult)): #if a syntax or symbol error occurred, or if successful
                                            return grammarElseStmtResult
                                    
                                    if(lexemeList[0].classification == "Conditional Delimiter End"):
                                        lexemeList.pop(0)

                                        #return success
                                        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, True, False, None)
                                    else:
                                        add_error_result_text(GrammarCondStmtMissingDelimiterEndKeyword, ErrorLineNumber)
                                        return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)    

                                else:
                                    add_error_result_text(GrammarErrorNewLineMissing, ErrorLineNumber)
                                    return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)    
                            else:
                                add_error_result_text(GrammarCondStmtMissingElseKeyword, ErrorLineNumber)
                                return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)  
                        else:
                            add_error_result_text(GrammarErrorNewLineMissing, ErrorLineNumber)
                            return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)   
                else:
                    add_error_result_text(GrammarErrorNewLineMissing, ErrorLineNumber)
                    return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, True, False, False, None)                                 
            else:
                return set_grammar("cond_stmt", ErrorLineNumber, exprLexemeList, False, False, False, None)
    return set_grammar("cond_stmt", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of omg_stmt_end
# Returns Grammar Result
def grammar_omg_stmt_end(lexemeList, runDefault):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Conditional Delimiter End"):
        lexemeList.pop(0)

        #return success
        return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, True, False, None)
    elif(lexemeList[0].classification == "Conditional Switch Last"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        if(lexemeList[0].classification == "New Line"):
            lexemeList.pop(0)

            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            switchListOfLexeme = []
            while(lexeme_list_is_empty(lexemeList) == False):
                if(lexemeList[0].classification == "Conditional Switch" or lexemeList[0].classification == "Conditional Switch Last" or lexemeList[0].classification == "Conditional Delimiter End" ): 
                    break

                switchListOfLexeme.append(lexemeList[0])
                lexemeList.pop(0)
            
            if(runDefault):
                #check if grammar fit stmt
                grammarStmtResult: GrammarResult = grammar_stmt(switchListOfLexeme)

                if(if_grammar_has_error(grammarStmtResult)): #if a syntax or symbol error occurred, or if successful
                    return grammarStmtResult
            
            if(lexemeList[0].classification == "Conditional Delimiter End"):
                lexemeList.pop(0)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                #return success
                return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, True, False, None)

            return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, True, False, None)

    return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of omg_stmt
# Returns Grammar Result
def grammar_omg_stmt(lexemeList, runDefault):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("switch_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Conditional Delimiter End" or lexemeList[0].classification == "Conditional Switch Last"):
        grammarOmgStmtEnd: GrammarResult = grammar_omg_stmt_end(lexemeList, runDefault)

        if(if_grammar_has_error(grammarOmgStmtEnd) or if_grammar_matched(grammarOmgStmtEnd)): #if a syntax or symbol error occurred, or if successful
            return grammarOmgStmtEnd

    if(lexemeList[0].classification == "Conditional Switch"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        literalValue = None
        grammarLiteralResult: GrammarResult = grammar_literal(lexemeList)
        
        #if grammar fit literal
        if(if_grammar_has_error(grammarLiteralResult)): #if a syntax or symbol error occurred
            return grammarLiteralResult

        elif(if_grammar_matched(grammarLiteralResult)):
            literalValue = grammarLiteralResult.value

            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "New Line"):
                lexemeList.pop(0)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("omg_stmt_end", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                ifRunStmt = False
                #check if identifier exists in symbol table
                for symbolCounter in range(len(ListOfSymbols)):
                    symbol = ListOfSymbols[symbolCounter]

                    #set the value of the previous identifier
                    if(symbol.identifier == "IT"):
                        ifRunStmt = symbol.value == literalValue
                        break

                switchListOfLexeme = []
                while(lexeme_list_is_empty(lexemeList) == False):
                    if(lexemeList[0].classification == "Conditional Switch" or lexemeList[0].classification == "Conditional Switch Last" or lexemeList[0].classification == "Conditional Delimiter End" ): 
                        break

                    switchListOfLexeme.append(lexemeList[0])
                    lexemeList.pop(0)
                        
                if(ifRunStmt):
                    runDefault = False

                    #check if grammar fit stmt
                    grammarStmtResult: GrammarResult = grammar_stmt(switchListOfLexeme)

                    if(if_grammar_has_error(grammarStmtResult)): #if a syntax or symbol error occurred, or if successful
                        return grammarStmtResult

                    lexemeList.clear() #recopy the modified list back to original list
                    for item in switchListOfLexeme:
                        lexemeList.append(item)

                #check if grammar fit omg_stmt
                grammarOmgStmtResult: GrammarResult = grammar_omg_stmt(lexemeList, runDefault)

                if(if_grammar_has_error(grammarOmgStmtResult) or if_grammar_matched(grammarOmgStmtResult)): #if a syntax or symbol error occurred, or if successful
                    return grammarOmgStmtResult

    return set_grammar("omg_stmt", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of switch_stmt
# Returns Grammar Result
def grammar_switch_stmt(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("switch_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Conditional Delimiter Switch Start"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("switch_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        if(lexemeList[0].classification == "New Line"):
            lexemeList.pop(0)

            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("switch_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "Conditional Switch"):
                lexemeList.pop(0)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("omg_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                literalValue = None
                grammarLiteralResult: GrammarResult = grammar_literal(lexemeList)
                
                #if grammar fit literal
                if(if_grammar_has_error(grammarLiteralResult)): #if a syntax or symbol error occurred
                    return grammarLiteralResult

                elif(if_grammar_matched(grammarLiteralResult)):
                    literalValue = grammarLiteralResult.value

                    #check if lexeme list is empty before checking for further matches
                    if(lexeme_list_is_empty(lexemeList)):
                        return set_grammar("omg_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                    ErrorLineNumber = lexemeList[0].lineNumber

                    if(lexemeList[0].classification == "New Line"):
                        lexemeList.pop(0)

                        #check if lexeme list is empty before checking for further matches
                        if(lexeme_list_is_empty(lexemeList)):
                            return set_grammar("omg_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                        ErrorLineNumber = lexemeList[0].lineNumber

                        ifRunStmt = False
                        #check if identifier exists in symbol table
                        for symbolCounter in range(len(ListOfSymbols)):
                            symbol = ListOfSymbols[symbolCounter]

                            #set the value of the previous identifier
                            if(symbol.identifier == "IT"):
                                ifRunStmt = symbol.value == literalValue
                                break

                        switchListOfLexeme = []
                        while(lexeme_list_is_empty(lexemeList) == False):
                            if(lexemeList[0].classification == "Conditional Switch" or lexemeList[0].classification == "Conditional Switch Last" or lexemeList[0].classification == "Conditional Delimiter End" ): 
                                break

                            switchListOfLexeme.append(lexemeList[0])
                            lexemeList.pop(0)

                        #check if list has loop break operator, copy modified list to lexeme list
                        ifEncounteredBreak = False
                        for item in switchListOfLexeme:
                            if(item.classification == "Loop Break Operator"):
                                ifEncounteredBreak = True
                                break
                        
                        runDefault = True
                        if(ifRunStmt):
                            runDefault = False
                            #check if grammar fit stmt
                            grammarStmtResult: GrammarResult = grammar_stmt(switchListOfLexeme)

                            if(if_grammar_has_error(grammarStmtResult)): #if a syntax or symbol error occurred, or if successful
                                return grammarStmtResult

                        #check if grammar fit omg_stmt
                        grammarOmgStmtResult: GrammarResult = grammar_omg_stmt(lexemeList, runDefault)

                        if(if_grammar_has_error(grammarOmgStmtResult) or if_grammar_matched(grammarOmgStmtResult)): #if a syntax or symbol error occurred, or if successful
                            return grammarOmgStmtResult

    return set_grammar("switch_stmt", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of loop_condition
# Returns Grammar Result
def grammar_loop_condition(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("loop_condition", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].string == "TIL"):
        lexemeList.pop(0)

        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("loop_condition", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        #check if grammar fit expr
        grammarExprResult: GrammarResult = grammar_expr(lexemeList)

        if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occured
            return grammarExprResult
        elif(if_grammar_matched(grammarExprResult)): #if successful
            if(grammarExprResult.value == False):
                return set_grammar("loop_condition", ErrorLineNumber, lexemeList, True, True, False, True)
    elif(lexemeList[0].string == "WILE"):
        lexemeList.pop(0)

        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("loop_condition", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        #check if grammar fit expr
        grammarExprResult: GrammarResult = grammar_expr(lexemeList)

        if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occured
            return grammarExprResult
        elif(if_grammar_matched(grammarExprResult)): #if successful
            if(grammarExprResult.value == True):
                return set_grammar("loop_condition", ErrorLineNumber, lexemeList, True, True, False, True)

    return set_grammar("loop_condition", ErrorLineNumber, lexemeList, False, False, False, False)
    
# Function that checks grammar of loop_condition
# Returns Grammar Result
def grammar_loop_stmt(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    loopName = ""
    variableName = ""
    variableCounter = 0
    counterUpdateOperator = ""
    if(lexemeList[0].classification == "Loop Delimiter Start"): #check fpr loop delimiter start
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, False, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        if(lexemeList[0].classification == "Identifier"): ##check for identifier (for loop)
            loopName = lexemeList[0].string
            lexemeList.pop(0)

            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[0].classification == "Unary Math Operator"): #check for loop operator
                counterUpdateOperator = lexemeList[0].string
                lexemeList.pop(0)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

                if(lexemeList[0].classification == "Argument Operator"): #check for YR
                    lexemeList.pop(0)

                    #check if lexeme list is empty before checking for further matches
                    if(lexeme_list_is_empty(lexemeList)):
                        return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                    ErrorLineNumber = lexemeList[0].lineNumber

                    if(lexemeList[0].classification == "Identifier"): #check for variable name
                        variableName = lexemeList[0].string
                        
                        identifierIsFound = False
                        #check if variable exists
                        for symbolCounter in range(len(ListOfSymbols)):
                            symbol = ListOfSymbols[symbolCounter]
                            
                            #set the value of the previous identifier
                            if(symbol.identifier == variableName):
                                variableCounter = symbolCounter
                                identifierIsFound = True
                                break
                        
                        #if identifier does not exist
                        if(identifierIsFound == False):
                            #if not symbol error
                            add_error_result_text(variable_error_missing(variableName), ErrorLineNumber)
                            
                            return set_grammar("variable_assignment", ErrorLineNumber, lexemeList, True, True, False, None)

                        lexemeList.pop(0)

                        #check if lexeme list is empty before checking for further matches
                        if(lexeme_list_is_empty(lexemeList)):
                            return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                        ErrorLineNumber = lexemeList[0].lineNumber

                        # match grammar for loop_condition
                        loopConditionListLexeme = []
                        while(lexeme_list_is_empty(lexemeList) == False):
                            if(lexemeList[0].classification == "New Line"): 
                                lexemeList.pop(0)
                                break
                            loopConditionListLexeme.append(lexemeList[0])
                            lexemeList.pop(0)

                        # get the statements for repetition
                        loopListOfLexeme = []
                        while(lexeme_list_is_empty(lexemeList) == False):
                            if(lexemeList[0].classification == "Loop Delimiter End"): 
                                break

                            loopListOfLexeme.append(lexemeList[0])
                            lexemeList.pop(0)

                        while True: #loop set up
                            repeatingListOfLexeme = []
                            for item in loopListOfLexeme:
                                repeatingListOfLexeme.append(item)

                            repeatingExpressionCondition = []
                            for item in loopConditionListLexeme:
                                repeatingExpressionCondition.append(item)

                            #check for loop condition result
                            grammarLoopConditionResult: GrammarResult = grammar_loop_condition(repeatingExpressionCondition)
                            
                            if(if_grammar_has_error(grammarLoopConditionResult)): #if a syntax or symbol error occured
                                return grammarLoopConditionResult

                            if(grammarLoopConditionResult.value == True):
                                # run grammar for stmt
                                grammarStmtResult: GrammarResult = grammar_stmt(repeatingListOfLexeme)

                                if(if_grammar_has_error(grammarStmtResult)): #if a syntax or symbol error occurred, or if successful
                                    return grammarStmtResult

                                if(counterUpdateOperator == "UPPIN"): #update variable in symbol table
                                    ListOfSymbols[variableCounter].value = ListOfSymbols[variableCounter].value + 1
                                    
                                elif(counterUpdateOperator == "NERFIN"): #update variable in symbol table
                                    ListOfSymbols[variableCounter].value = ListOfSymbols[variableCounter].value - 1
                            else: #break if loop condition showed fail
                                break
                        
                        #check if lexeme list is empty before checking for further matches
                        if(lexeme_list_is_empty(lexemeList)):
                            return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                        ErrorLineNumber = lexemeList[0].lineNumber

                        if(lexemeList[0].classification == "Loop Delimiter End"):
                            lexemeList.pop(0)

                            #check if lexeme list is empty before checking for further matches
                            if(lexeme_list_is_empty(lexemeList)):
                                return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)
                            ErrorLineNumber = lexemeList[0].lineNumber

                            if(lexemeList[0].classification == "Identifier"):
                                if(loopName != lexemeList[0].string):
                                    add_error_result_text(GrammarLoopStmtIncorrectLabel, ErrorLineNumber)
                                    return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, False, False, None)

                                lexemeList.pop(0)

                                #check if lexeme list is empty before checking for further matches
                                if(lexeme_list_is_empty(lexemeList)):
                                    return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, True, False, None)
                                ErrorLineNumber = lexemeList[0].lineNumber

                                return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, True, True, False, None)
    
    return set_grammar("loop_stmt", ErrorLineNumber, lexemeList, False, False, False, None)

# Function that checks grammar of stmt2
# Returns GrammarResult
def grammar_stmt2(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    if(lexemeList[0].classification == "Loop Break Operator"):
        lexemeList.pop(0)

        if(lexemeList[0].classification == "New Line"): #remove new line after loop break operator if any
            lexemeList.pop(0)

        #return success
        return set_grammar("stmt2", ErrorLineNumber, lexemeList, True, True, False, None)

    #check if grammar fit input
    grammarInputResult: GrammarResult = grammar_input(lexemeList)

    if(if_grammar_has_error(grammarInputResult) or if_grammar_matched(grammarInputResult)): #if a syntax or symbol error occurred, or if successful
        return grammarInputResult

    #check if grammar fit output
    grammarOutputResult: GrammarResult = grammar_output(lexemeList)

    if(if_grammar_has_error(grammarOutputResult) or if_grammar_matched(grammarOutputResult)): #if a syntax or symbol error occurred, or if successful
        return grammarOutputResult

    # check if grammar fit multiline comment
    grammarMultilineCommentResult: GrammarResult = grammar_multiline_cmt(lexemeList)

    if(if_grammar_has_error(grammarMultilineCommentResult) or if_grammar_matched(grammarMultilineCommentResult)): #if a syntax or symbol error occured, or if successful
        return grammarMultilineCommentResult

    #check if grammar fit variable assignment
    grammarVariableAssignmentResult: GrammarResult = grammar_variable_assignment(lexemeList)

    if(if_grammar_has_error(grammarVariableAssignmentResult) or if_grammar_matched(grammarVariableAssignmentResult)): #if a syntax or symbol error occured, or if successful
        return grammarVariableAssignmentResult

    #check if grammar fit recast_stmt
    grammarRecastStmtResult: GrammarResult = grammar_recast_stmt(lexemeList)

    if(if_grammar_has_error(grammarRecastStmtResult) or if_grammar_matched(grammarRecastStmtResult)): #if a syntax or symbol error occured, or if successful
        return grammarRecastStmtResult

    #check if grammar fit loop_stmt
    grammarLoopStmtResult: GrammarResult = grammar_loop_stmt(lexemeList)

    if(if_grammar_has_error(grammarLoopStmtResult) or if_grammar_matched(grammarLoopStmtResult)): #if a syntax or symbol error occured, or if successful
        return grammarLoopStmtResult

    #check if grammar fit switch_stmt
    grammarSwitchStmtResult: GrammarResult = grammar_switch_stmt(lexemeList)

    if(if_grammar_has_error(grammarSwitchStmtResult) or if_grammar_matched(grammarSwitchStmtResult)): #if a syntax or symbol error occured, or if successful
        return grammarSwitchStmtResult

    #check if grammar fit cond_stmt
    grammarCondStmtResult: GrammarResult = grammar_cond_stmt(lexemeList)

    if(if_grammar_has_error(grammarCondStmtResult) or if_grammar_matched(grammarCondStmtResult)): #if a syntax or symbol error occured, or if successful
        return grammarCondStmtResult

    #check if grammar fit expr
    grammarExprResult: GrammarResult = grammar_expr(lexemeList)

    if(if_grammar_has_error(grammarExprResult)): #if a syntax or symbol error occured
        return grammarExprResult
    elif(if_grammar_matched(grammarExprResult)): #if it matched as lone statement
        foundIdentifier = False
        #check if identifier exists in symbol table
        for symbolCounter in range(len(ListOfSymbols)):
            symbol = ListOfSymbols[symbolCounter]

            #set the value of the previous identifier
            if(symbol.identifier == "IT"):
                ListOfSymbols[symbolCounter].value = grammarExprResult.value
                foundIdentifier = True

        if(foundIdentifier == False): #if identifier not found, implement
            ListOfSymbols.append(Symbol("IT", grammarExprResult.value))

        return grammarExprResult

    #default grammar error result if it does NOT fit ANY abstractions at all for smt2
    grammarResult = GrammarResult("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    # add_error_result_text(GrammarErrorStmt2NoAbstractionMatch, ErrorLineNumber)
    return grammarResult

# Function that checks grammar of stmt
# Accepts a list
# Returns GrammarResult
def grammar_stmt(lexemeList: list):
    global ResultText
    global ErrorLineNumber

    grammarStmt2Result: GrammarResult = grammar_stmt2(lexemeList)

    # if(if_grammar_has_error(grammarStmt2Result) or if_grammar_matched(grammarStmt2Result)): #if it resulted in error
    #     return grammarStmt2Result

    if(if_grammar_has_error(grammarStmt2Result)): #if it resulted in error
        if(ResultText == ""):
            add_error_result_text(GrammarErrorStmt2NoAbstractionMatch, ErrorLineNumber)

        return grammarStmt2Result
    elif(if_grammar_matched(grammarStmt2Result)): #if it matched with stmt2, check for other abstractions
        if(lexeme_list_is_empty(lexemeList)): #no error if no more lexemes
            return grammarStmt2Result
        ErrorLineNumber = lexemeList[0].lineNumber

        #match with inline comment

        #check if it still has other statements
        if(lexemeList[0].classification == "New Line"):
            lexemeList.pop(0)

            grammarStmtResult: GrammarResult = grammar_stmt(lexemeList)

            if(if_grammar_has_error(grammarStmtResult) or if_grammar_matched(grammarStmtResult)): #if it matched
                return grammarStmtResult

    #default grammar error result if it does NOT fit ANY abstractions at all for stmt
    grammarResult = GrammarResult("stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    return grammarResult

# Function that checks grammar of program
# Accepts a list
# Returns GrammarResult
def grammar_program(lexemeList: list):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    # check if lexeme list is empty before checking for code delimiter
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("program", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = 0

    #remove all inline comments
    for counter in range(len(lexemeList)):
        if(lexemeList[counter].classification == "Inline Comment Delimiter"):
            previousCounter = counter
            lexemeList.pop(counter)

            #check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("stmt", ErrorLineNumber, lexemeList, False, False, False, None)
            ErrorLineNumber = lexemeList[0].lineNumber

            if(lexemeList[counter].classification == "Comment"):
                lexemeList.pop(previousCounter)

                #check if lexeme list is empty before checking for further matches
                if(lexeme_list_is_empty(lexemeList)):
                    return set_grammar("stmt", ErrorLineNumber, lexemeList, False, False, False, None)
                ErrorLineNumber = lexemeList[0].lineNumber

            break

    # check if it starts with the code delimiter
    if (lexemeList[0].classification == "Code Delimiter Start"):
        lexemeList.pop(0) #remove delimiter and new line
        lexemeList.pop(0)

        # check if lexeme list is empty before checking for code delimiter end
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("program", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[-1].lineNumber

        # check if it ends with the code delimiter
        if(lexemeList[-1].classification == "Code Delimiter End"):
            lexemeList.pop(-1) #remove delimiter and new line
            lexemeList.pop(-1)

            # check if lexeme list is empty before checking for further matches
            if(lexeme_list_is_empty(lexemeList)):
                return set_grammar("program", ErrorLineNumber, lexemeList, True, False, False, None)

            ErrorLineNumber = lexemeList[0].lineNumber
            
            return grammar_stmt(lexemeList) #check if it fulfills stmt
        else:
            grammarResult = set_grammar("program", ErrorLineNumber, lexemeList, True, False, False, None)

            add_error_result_text(GrammarErrorNoCodeDelimiterEnd, ErrorLineNumber)
    else:
        grammarResult = set_grammar("program", ErrorLineNumber, lexemeList, False, False, False, None)

        add_error_result_text(GrammarErrorNoCodeDelimiterStart, ErrorLineNumber)

    return grammarResult

# Function that reads text and prepares a symbol table for value of variables as well as the contents of the console
# Sets the global variable
def return_list_of_symbols():
    global ListOfSymbols
    global ListOfLexemes
    global ResultText

    ResultText = ""

    grammarProgramResult = grammar_program(ListOfLexemes)
    # print_lexeme_list(ListOfLexemes)
    # print_grammar_result(grammarProgramResult)
    # print_symbol_list(ListOfSymbols)

    return ResultText
