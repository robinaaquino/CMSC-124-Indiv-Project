# This file holds all object definitions

class Lexeme: #properties of a lexeme
    def __init__(self, string, classification, lineNumber):
        self.string = string #the string itself
        self.classification = classification #what the string is
        self.lineNumber = lineNumber #what line number it belongs to

class Symbol:  # properties of a symbol
    def __init__(self, identifier, value):
        self.identifier = identifier  # the identifier itself
        self.value = value  # the value of the identifier

class GrammarResult:  # properties after checking if it fits a grammar
    def __init__(self, grammarIdentifier, lineNumber, lexemeList, ifFirstLexemeMatched, ifOtherLexemeMatched, symbolError, value):
        self.grammarIdentifier = grammarIdentifier  # the name of the grammar
        self.lineNumber = lineNumber  # last checked line for grammar
        self.lexemeList = lexemeList  # remaining lexeme list
        self.ifFirstLexemeMatched = ifFirstLexemeMatched # if the syntax matched with first lexeme in current grammar
        self.ifOtherLexemeMatched = ifOtherLexemeMatched # if the other lexemes for grammar matched as well
        self.symbolError = symbolError # if the syntax was matched sucessfully but there was an error during parsing the semantics
        self.value = value # the value from the aforementioned grammar after parsing
        
class TypecastResult: # properties after typecasting a value
    def __init__(self, value, ifSuccess):
        self.value = value # value
        self.ifSuccess = ifSuccess # if typecasting is a success