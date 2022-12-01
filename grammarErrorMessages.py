#TODO Separate in groups of grammar

# Grammar Error Codes
GrammarErrorNoCodeDelimiterStart = "Missing HAI at the start of the program"
GrammarErrorNoCodeDelimiterEnd = "Missing KTHX at the end of the program"
GrammarErrorPrintKeyword = "Missing VISIBLE keyword"
GrammarErrorPrintArgsNoIdentifier = "Missing Identifier"
GrammarErrorInputNoIdentifier = "Missing INPUT keyword"
GrammarErrorMultilineCommentNoDelimiterStart = "Missing OBTW at the start of the multiline comment"
GrammarErrorMultilineCommentNoDelimiterEnd = "Missing TLDR at the end of the multiline comment"
GrammarErrorIdentifierNoIdentifier = "Missing Identifier"
GrammarErrorIdentifierNoIdentifierInSymbolTable = "Identifier does not exist"
GrammarErrorStmt2NoAbstractionMatch = "Matched no valid abstractions for stmt2"
GrammarErrorStmtNoAbstractionMatch = "Matched no valid abstractions for stmt"
GrammarErrorVariableAssignmentKeywordMissing = "Missing R keyword"
GrammarErrorMissingValue = "Missing identifier, literal or expression"
GrammarBinaryExpNoValue = "Error in binary expression"
GrammarBinaryExpNoOperand = "No operands for expression"
GrammarInfiniteArityExpNoOperand = "No operands for infinite arity"
GrammarExprNoAnKeyword = "Missing AN keyword"
GrammarInfiniteArityMKAYKeyword = "Missing MKAY keyword"
GrammarComparisonOperationUnequalValue = "Unequal value for first operand"
GrammarComparisonOperationParseError = "Error in parsing expression"
GrammarCondStmtMissingElseKeyword = "Missing NO WAI keyword"
GrammarCondStmtMissingDelimiterEndKeyword = "Missing OIC keyword"


# Utility Error Codes
GrammarErrorEmptyLexemeList = "Lexeme list is empty"
GrammarErrorNewLineMissing = "Missing new line"

def typecast_error(value, dataType):
    return ("Error in typecasting " + str(value) + " to " + dataType)

def variable_error_already_existed(name):
    return (name + " variable already exists")

def variable_error_missing(name):
    return (name + " variable is missing")