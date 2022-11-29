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


# Function to typecast a value to a data type
# Returns typecasted value
def typecast_value(value, newDataType):
    #TODO update round to truncate to 2 decimal places
    #needs a special function

    dataTypeOfValue = return_data_type(value)
    
    #convert value
    if (newDataType == "TROOF"): #convert value to troof
        if (dataTypeOfValue == "NOOB"): #if from noob
            return TypecastResult(False, True)
        elif (dataTypeOfValue == "NUMBR" or dataTypeOfValue == "NUMBAR"): #if from numbr and numbar
            if (value != 0):
                return TypecastResult(True, True)
            else:
                return TypecastResult(False, True)
        elif (dataTypeOfValue == "YARN"): #if from yarn
            value = value[1:-1] #remove quotations
            if(len(value) == 0):
                return TypecastResult(False, True)
            else: 
                return TypecastResult(True, True)
        elif (dataTypeOfValue == "TROOF"):
            if(value == "WIN"):
                return TypecastResult(True, True)
            elif(value == "FAIL"):
                return TypecastResult(False, True)
            else:
                return TypecastResult(value, False)
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
                return TypecastResult(round(float(value), 2), True) #conver to float then round to 2 decimal places
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
    
# Function that checks grammar of print
# Returns GrammarResult
def grammar_print(lexemeList):
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    # if matched with output

    # else syntax error..? NO SYNTAX ERROR BECAUSE IT DIDNT MATCH FIRST KEYWORD FOR STATEMENT

# Function that checks grammar of multiline_cmt2
# Returns GrammarResult
#TODO change grammar in word, does not need linebreak
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

        #return success
        return set_grammar("multiline_cmt2", ErrorLineNumber, lexemeList, True, True, False, None)
    
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
                    UserInputValue = simpledialog.askstring("Input", "Input text")

                    #TODO check if this works when creating variables
                    ListOfSymbols[symbolCounter].value = UserInputValue

                    lexemeList.pop(0)

                    #return success for current grammar
                    return set_grammar("input", ErrorLineNumber, lexemeList, True, True, False, None)

            #if it found no identifier in the symbol table, return error
            grammarResult = set_grammar("input", ErrorLineNumber, lexemeList, True, True, True, None, None)

            add_error_result_text(GrammarErrorIdentifierNoIdentifierInSymbolTable, ErrorLineNumber)

        else:
            grammarResult = set_grammar("input", ErrorLineNumber, lexemeList, True, False, False, None, None)

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
        lexemeList.pop(0)

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
                print(identifierCounter)
                print(ListOfSymbols[0].value)
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
            grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, True)
        else:
            grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, False)

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

        # check if operator value is NOT
        if(operatorValue == "NOT"):
            grammarBinaryExp1Result = grammar_binary_exp(lexemeList)

            #if grammar fit binary_exp
            if (if_grammar_has_error(grammarBinaryExp1Result)): #if error
                return grammarBinaryExp1Result
            elif (if_grammar_matched(grammarBinaryExp1Result)): #if successful
                firstOperandType = return_data_type(grammarBinaryExp1Result.value)

                firstOperand = grammarBinaryExp1Result.value

                if(firstOperandType != "TROOF"):
                    firstOperand = typecast_value(firstOperand, "TROOF")

                if(firstOperand.ifSuccess == False):
                    add_error_result_text(typecast_error(grammarBinaryExp1Result.value, "TROOF"), ErrorLineNumber)

                    return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, True, operationValue)
                    #TODO changed to symbol error true due to error in typecast
                
                firstOperand = firstOperand.value

                operationValue = not firstOperand

                return set_grammar("binary_bool_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)
        else:
            grammarBinaryExp1Result = grammar_binary_exp(lexemeList)

            #if grammar fit binary_exp
            if (if_grammar_has_error(grammarBinaryExp1Result)): #if error
                return grammarBinaryExp1Result

            elif (if_grammar_matched(grammarBinaryExp1Result)): #if successful
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
                            #TODO changed to symbol error true due to error in typecast
                        
                        firstOperand = firstOperand.value
                        secondOperand = secondOperand.value
                            
                        #if no error in typecast, proceed with operation
                        if(operatorValue == "BOTH OF"):
                            operationValue = firstOperand and secondOperand
                        elif(operatorValue == "EITHER OF"):
                            operationValue = firstOperand or secondOperand
                        elif(operatorValue == "WON OF"):
                            operationValue = (firstOperand and not secondOperand) or (not firstOperand and secondOperand)

                        #return success
                        return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)

    return set_grammar("bool_operator", ErrorLineNumber, lexemeList, False, False, False, None)

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
                        #TODO check if symbol error is supposed to be false, this is an error
                        #changed to True
                    
                    firstOperand = firstOperand.value
                    secondOperand = secondOperand.value
                        
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
                                operationValue = result.value
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

    #return fail
    return set_grammar("binary_exp", ErrorLineNumber, lexemeList, False, False, False, None)
    

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

    #match with NOT lexeme
    if(lexemeList[0].classification == "Not Boolean Operator"):
        lexemeList.pop(0)

        #check if lexeme list is empty before checking for further matches
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("expr", ErrorLineNumber, lexemeList, False, False, False, None)
        ErrorLineNumber = lexemeList[0].lineNumber

        grammarExprResult = grammar_expr(lexemeList)

        #if grammar fit expr
        if(if_grammar_has_error(grammarExprResult) or if_grammar_matched(grammarExprResult)): #if a syntax or symbol error occurred, or if successful
            grammarResult = grammarExprResult
            grammarResult.value = not (grammarExprResult.value)

        return grammarResult
    else:
        grammarResult = set_grammar("expr", ErrorLineNumber, lexemeList, False, False, False, None)

    #match with binary_exp
    grammarBinaryExpResult: GrammarResult = grammar_binary_exp(lexemeList)

    #if grammar fit input
    if(if_grammar_has_error(grammarBinaryExpResult) or if_grammar_matched(grammarBinaryExpResult)): #if a syntax or symbol error occurred, or if successful
        return grammarBinaryExpResult

    #TODO match with infinite arity expr

    #default error catch if it did not match any
    grammarResult = GrammarResult("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    return grammarResult

    
# Function that checks grammar of stmt2
# Returns GrammarResult
def grammar_stmt2(lexemeList):
    global ResultText
    global ErrorLineNumber

    #check if grammar fit input
    grammarInputResult: GrammarResult = grammar_input(lexemeList)

    if(if_grammar_has_error(grammarInputResult) or if_grammar_matched(grammarInputResult)): #if a syntax or symbol error occurred, or if successful
        return grammarInputResult

    #check if grammar fit multiline comment
    grammarMultilineCommentResult: GrammarResult = grammar_multiline_cmt(lexemeList)

    if(if_grammar_has_error(grammarMultilineCommentResult) or if_grammar_matched(grammarMultilineCommentResult)): #if a syntax or symbol error occured, or if successful
        return grammarMultilineCommentResult

    #check if grammar fit variable assignment
    grammarVariableAssignmentResult: GrammarResult = grammar_variable_assignment(lexemeList)

    if(if_grammar_has_error(grammarVariableAssignmentResult) or if_grammar_matched(grammarVariableAssignmentResult)): #if a syntax or symbol error occured, or if successful
        return grammarVariableAssignmentResult

    # else test other grammars


    #check if grammar fit expr
    grammarExprResult: GrammarResult = grammar_expr(lexemeList)

    if(if_grammar_has_error(grammarExprResult) or if_grammar_matched(grammarExprResult)): #if a syntax or symbol error occured, or if successful
        return grammarExprResult

    #default grammar error result if it does NOT fit ANY abstractions at all for smt2
    grammarResult = GrammarResult("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    add_error_result_text(GrammarErrorStmt2NoAbstractionMatch, ErrorLineNumber)
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
        else:
            add_error_result_text(GrammarErrorNewLineMissing, ErrorLineNumber)

            return set_grammar("stmt", ErrorLineNumber, lexemeList, True, False, False, None)

    #TODO should we accept HAI THX only? change how error is parsed, based on grammar tho
    # change grammar if we'll accept HAI THX, for now don't accept HAI THX only


    #default grammar error result if it does NOT fit ANY abstractions at all for stmt
    grammarResult = GrammarResult("stmt", ErrorLineNumber, lexemeList, False, False, False, None)
    add_error_result_text(GrammarErrorStmtNoAbstractionMatch, ErrorLineNumber)
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

            #TODO Should we accept HAI THX only with no other code?

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

    grammarProgramResult = grammar_program(ListOfLexemes)
    print_lexeme_list(ListOfLexemes)
    print_grammar_result(grammarProgramResult)
    print_symbol_list(ListOfSymbols)
    
    return ResultText
