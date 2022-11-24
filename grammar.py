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
        add_error_result_text(GrammarErrorEmptyLexemeList, ErrorLineNumber)
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
            return TypecastResult(value, True)
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
    print('print\n')
    # print_lexeme_list(lexemeList)
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    # if matched with output

    # else syntax error..? NO SYNTAX ERROR BECAUSE IT DIDNT MATCH FIRST KEYWORD FOR STATEMENT

# Function that checks grammar of multiline_cmt2
# Returns GrammarResult
#TODO change grammar in word, does not need linebreak
def grammar_multiline_cmt2(lexemeList):
    # print('multiline_cmt2\n')
    # print_lexeme_list(lexemeList)
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
    # print('multiline_cmt\n')
    # print_lexeme_list(lexemeList)
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
    # print('input\n')
    # print_lexeme_list(lexemeList)
    global ResultText
    global ErrorLineNumber

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
                symbol = ListOfSymbols(symbolCounter)
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

# Function that checks grammar of literal
# Returns GrammarResult
def grammar_literal(lexemeList):
    # print('literal')
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
            # print('yea?')
            grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, True)
        else:
            grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, True, True, False, False)

        lexemeList.pop(0)

        return grammarResult
    else:
        grammarResult = set_grammar("literal", ErrorLineNumber, lexemeList, False, False, False, None)
    
    return grammarResult

# Function that checks grammar of binary_math_operator
# Returns GrammarResult
def grammar_binary_math_operator(lexemeList):
    print('binary math')
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

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
            return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, False, False, False, None)
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
                        add_error_result_text(TypecastError, ErrorLineNumber)

                        return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)
                    
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
                            operationValue = typecast_value(operationValue, "NUMBR")

                    #return success
                    return set_grammar("binary_math_operator", ErrorLineNumber, lexemeList, True, True, False, operationValue)
    
    return grammarResult

# Function that checks grammar of binary_exp
# Returns GrammarResult
def grammar_binary_exp(lexemeList):
    print("binary exp")
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    #check if lexeme list is empty before checking for further matches
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("multiline_cmt", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = lexemeList[0].lineNumber

    #literal
    grammarLiteralResult: GrammarResult = grammar_literal(lexemeList)

    #if grammar fit literal
    if(if_grammar_has_error(grammarLiteralResult) or if_grammar_matched(grammarLiteralResult)): #if a syntax or symbol error occurred, or if successful
        return grammarLiteralResult

    #binary_math_op binary_exp "an" binary_exp
    grammarMathOperatorResult: GrammarResult = grammar_binary_math_operator(lexemeList)

    if(if_grammar_has_error(grammarMathOperatorResult) or if_grammar_matched(grammarMathOperatorResult)): #if a syntax or symbol error occurred, or if successful
        print('huwat')
        return grammarMathOperatorResult

    #binary_boolean_op binary_exp "an" binary_exp

    return grammarResult
    

# Function that checks grammar of expr
# Returns GrammarResult
def grammar_expr(lexemeList):
    print('1 run bois')
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

    #match with infinite arity expr


    #default error catch if it did not match any
    grammarResult = GrammarResult("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    return grammarResult

    


# Function that checks grammar of stmt2
# Returns GrammarResult
def grammar_stmt2(lexemeList):
    # print('stmt2\n')
    # print_lexeme_list(lexemeList)
    global ResultText
    global ErrorLineNumber

    grammarInputResult: GrammarResult = grammar_input(lexemeList)

    #if grammar fit input
    if(if_grammar_has_error(grammarInputResult) or if_grammar_matched(grammarInputResult)): #if a syntax or symbol error occurred, or if successful
        return grammarInputResult

    grammarMultilineCommentResult: GrammarResult = grammar_multiline_cmt(lexemeList)

    #if grammar fit multiline comment
    if(if_grammar_has_error(grammarMultilineCommentResult) or if_grammar_matched(grammarMultilineCommentResult)): #if a syntax or symbol error occured, or if successful
        return grammarMultilineCommentResult

    grammarExprResult: GrammarResult = grammar_expr(lexemeList)

    #if grammar fit expr
    if(if_grammar_has_error(grammarExprResult) or if_grammar_matched(grammarExprResult)): #if a syntax or symbol error occured, or if successful
        print('yea it matched here right?')
        return grammarExprResult

    print_grammar_result(grammarExprResult)

    print('No matched?')

    # else test other grammars

    #default grammar error result if it does NOT fit ANY abstractions at all for smt2
    grammarResult = GrammarResult("stmt2", ErrorLineNumber, lexemeList, False, False, False, None)
    add_error_result_text(GrammarErrorStmt2NoAbstractionMatch, ErrorLineNumber)
    return grammarResult

# Function that checks grammar of stmt
# Accepts a list
# Returns GrammarResult
def grammar_stmt(lexemeList: list):
    # print('stmt\n')
    # print_lexeme_list(lexemeList)
    global ResultText
    global ErrorLineNumber

    grammarStmt2Result: GrammarResult = grammar_stmt2(lexemeList)

    if(if_grammar_has_error(grammarStmt2Result) or if_grammar_matched(grammarStmt2Result)): #if it matched
        return grammarStmt2Result

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
    # print('prg\n')
    # print_lexeme_list(lexemeList)
    global ResultText
    global ErrorLineNumber

    grammarResult = GrammarResult("", -1, [], False, False, True, None)

    # check if lexeme list is empty before checking for code delimiter
    if(lexeme_list_is_empty(lexemeList)):
        return set_grammar("program", ErrorLineNumber, lexemeList, False, False, False, None)
    ErrorLineNumber = 0

    # check if it starts with the code delimiter
    if (lexemeList[0].classification == "Code Delimiter Start"):
        lexemeList.pop(0)

        # check if lexeme list is empty before checking for code delimiter end
        if(lexeme_list_is_empty(lexemeList)):
            return set_grammar("program", ErrorLineNumber, lexemeList, True, False, False, None)
        ErrorLineNumber = lexemeList[-1].lineNumber

        # check if it ends with the code delimiter
        if(lexemeList[-1].classification == "Code Delimiter End"):
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

    print_grammar_result(grammarProgramResult)
    
    return ResultText

# print('\n/////////////')
# print_typecast_result(typecast_value(1, "YARN"))
# print('\n/////////////')
# print_typecast_result(typecast_value(1.0, "YARN"))
# print('\n/////////////')
# print_typecast_result(typecast_value("1", "YARN"))
# print('\n/////////////')
# print_typecast_result(typecast_value("1.0", "YARN"))
# print('\n/////////////')
# print_typecast_result(typecast_value("\"1\"", "YARN"))
# print('\n/////////////')
# print_typecast_result(typecast_value("WIN", "YARN"))
# print('\n/////////////')
# print_typecast_result(typecast_value("FAIL", "YARN"))
# print('\n/////////////')

#LAST
#CHECK IF TYPECAST IS WORKING
