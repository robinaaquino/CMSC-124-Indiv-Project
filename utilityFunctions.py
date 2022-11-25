from objectDefinition import *

#Function that prints all lexemes in an array
#Accepts an array of lexemes
#Prints each lexeme
def print_lexeme_list(lexemeList):
    print("\n**********************\n")
    if(len(lexemeList) == 0):
        print("List is EMPTY\n")

    for counter in range(len(lexemeList)): #iterate over the length of the lexeme list
        lexeme = lexemeList[counter]
        print("\nCount: ", counter)
        print("String: ", lexeme.string)
        print("Classification: ", lexeme.classification)
        print("Line Number: ", lexeme.lineNumber)
    print("\n**********************\n")
        

# Function that prints lexeme properties
# Prints properties
def print_lexeme(lexeme: Lexeme):
    print("\n*******************\n")
    print("String: ", lexeme.string)
    print("Classification: ", lexeme.classification)
    print("Line Number: ", lexeme.lineNumber)

# Function that prints grammar result properties
# Prints properties
def print_grammar_result(grammarResult: GrammarResult):
    print("\n*******************\n")
    print("Grammar Identifier: ", grammarResult.grammarIdentifier)
    print("Line Number: ", grammarResult.lineNumber)
    print("Lexeme Length: ", len(grammarResult.lexemeList))
    print("ifFirstLexemeMatched: ", grammarResult.ifFirstLexemeMatched)
    print("ifOtherLexemeMatched: ", grammarResult.ifOtherLexemeMatched)
    print("symbolError: ", grammarResult.symbolError)
    print("value: ", grammarResult.value)

# Function that prints typecast result properties
# Prints properties
def print_typecast_result(typecastResult: TypecastResult):
    print("\n*******************\n")
    print("value: ", typecastResult.value)
    print("ifSuccess: ", typecastResult.ifSuccess)
    

# Function that sets a grammar's properties
# Returns grammar result
def set_grammar(grammarIdentifier, lineNumber, lexemeList, isMatched, syntaxError, symbolError, value):
    return GrammarResult(
        grammarIdentifier,
        lineNumber,
        lexemeList,
        isMatched,
        syntaxError,
        symbolError,
        value
    )
    
# Function that checks if a grammar resulted in a syntax or symbol error
# Returns a boolean value
def if_grammar_has_error(grammarResult: GrammarResult):
    syntaxError = grammarResult.ifFirstLexemeMatched == True and grammarResult.ifOtherLexemeMatched == False
    symbolError = grammarResult.symbolError
    if(syntaxError or symbolError):
        return True
    else:
        return False

# Function that checks if a grammar successfully matched
# Returns a boolean value
def if_grammar_matched(grammarResult: GrammarResult):
    if(grammarResult.ifFirstLexemeMatched == True and grammarResult.ifOtherLexemeMatched == True and grammarResult.symbolError == False):
        return True
    else:
        return False