from doctest import OutputChecker
import re

class Lexeme: #properties of a lexeme
    def __init__(self, string, classification, lineNumber):
        self.string = string #the string itself
        self.classification = classification #what the string is
        self.lineNumber = lineNumber #what line number it belongs to

ListOfLexemes = [] #array containing all registered lexemes

#regex for keywords
#code delimiters
CodeDelimiterStartRegex = "HAI\s" #regex to identify the starting code delimiter
CodeDelimiterEndRegex = "KTHX" #regex to identify the ending code delimiter

#variable declaration and assignment
VarDeclarationRegex = "I HAS A\s"
VarDeclarationAssignmentRegex = "ITZ\s"
VarAssignmentRegex = "R\s"

#operators
MathOperatorRegex = "(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF)\s"
ComparisonMathOperatorRegex = "(BIGGR OF|SMALLR OF)\s"
BoolOperatorRegex = "(BOTH OF|EITHER OF|WON OF)\s"
InfiniteBoolOperatorRegex = "(ANY OF|ALL OF)\s"
NotBoolOperatorRegex = "NOT\s"

#comments
InlineCommentDelimiterRegex = "BTW\s"
MultiCommentDelimiterStartRegex = "OBTW\s"
MultiCommentDelimiterEndRegex = "TLDR\s"

ComparisonOperatorRegex = "(BOTH SAEM|DIFFRINT)\s"
ConcatenationOperatorRegex = "SMOOSH\s"
ExpressionAndOperatorRegex = "AN\s"

#casting
CastingOperatorRegex = "IS NOW A\s"
TypecastOperatorStartRegex = "MAEK\s"
TypecastOperatorMidRegex = "A\s"

#output and input
OutputRegex = "VISIBLE\s"
InputRegex = "GIMMEH\s"

#condition
ConditionDelimiterIfElseStartRegex = "O RLY\?\s"
ConditionalIfRegex = "YA RLY\s"
ConditionalElifRegex = "MEBBE\s"
ConditionalElseRegex = "NO WAI\s"
ConditionalDelimiterEndRegex = "OIC\s"

#switch
ConditionalDelimiterSwitchStartRegex = "WTF\?\s"
ConditionalSwitchRegex = "OMG\s"
ConditionalSwitchLastRegex = "OMGWTF\s"

#loop
LoopDelimiterStartRegex = "IM IN YR\s"
ArgumentOperatorRegex = "YR\s"
LoopDelimiterEndRegex = "IM OUTTA YR\s"
LoopConditionRegex = "(TIL|WILE)\s"
LoopBreakOperatorRegex = "GTFO\s"

#unary
UnaryMathOperatorRegex = "(UPPIN|NERFIN)\s"
InfinityArityDelimiterEndRegex = "MKAY\s"

SoftbreakRegex = ","

#regex for all classifications
IdentifierRegex = "[A-Za-z]+[A-Za-z0-9_]*\s" #regex to identify variable names

#regex for literals
NumbrLiteralRegex = "(-[1-9][0-9]*|[1-9][0-9]*|[0])\s" #regex to identify integers
NumbarLiteralRegex = "-?[0-9]*)\.[0-9]*[1-9]\s" #regex to identify floats
TroofLiteralRegex = "(WIN|FAIL)\s" #regex for boolean values
TypeLiteralRegex = "(NOOB|NUMBR|NUMBAR|TROOF|YARN)\s" #regex for types
YarnLiteralRegex = "\".+\"\s" #regex to identify strings

NewLineRegex = "\n" #regex to identify new line
OtherRegex = ".*\s" #regex to identify any word that doesn't 

#next step, catch all tokens split by spaces and newlines

#Function that prints all lexemes in an array
#Accepts an array of lexemes
#Prints each lexeme
def print_lexeme_list(lexemeList):
    print("\n**********************\n")
    for counter in range(len(lexemeList)): #iterate over the length of the lexeme list
        lexeme = lexemeList[counter]
        print("\nCount: ", counter)
        print("String: ", lexeme.string)
        print("Classification: ", lexeme.classification)
        print("Line Number: ", lexeme.lineNumber)

#Function that adds a new lexeme to the list of lexemes
#Accepts regex, text string, line number and classification of lexeme
#Returns updated textString
def add_new_lexeme(regex, textString, lineNumber, classification):
    global ListOfLexemes

    textString = textString.replace(regex.group(), "", 1) #replace first occurence of the string
    cleanedTextString = regex.group().strip() #remove whitespaces from the string
    newLexeme = Lexeme(cleanedTextString, classification, lineNumber) #create a Lexeme class
    ListOfLexemes.append(newLexeme) #append new lexeme to list of lexemes
    return textString

#Function that reads text and classifies them
#Accepts a text string
#Sets the global variable
def return_list_of_lexemes(textString):
    global ListOfLexemes

    lineNumber = 1

    while len(textString) > 0:

        #check if matched with starting code delimiter
        codeDelimiterStartRegexMatch = re.match(CodeDelimiterStartRegex, textString)
        if(codeDelimiterStartRegexMatch):
            textString = add_new_lexeme(codeDelimiterStartRegexMatch, textString, lineNumber, 'Code Delimiter Start')
            continue

        #check if matched with new line
        newLineRegexMatch = re.match(NewLineRegex, textString)
        if(newLineRegexMatch):
            textString = add_new_lexeme(newLineRegexMatch, textString, lineNumber, 'New Line')
            lineNumber+=1
            continue

        #check if matched with identifiers
        identifierRegexMatch = re.match(IdentifierRegex, textString)
        if(identifierRegexMatch):
            textString = add_new_lexeme(identifierRegexMatch, textString, lineNumber, 'Identifier')
            continue

        #check if matched with yarn literal
        yarnLiteralRegexMatch = re.match(YarnLiteralRegex, textString)
        if(yarnLiteralRegexMatch):
            textString = add_new_lexeme(yarnLiteralRegexMatch, textString, lineNumber, 'Yarn Literal')
            continue

        #check if matched with anything else
        otherRegexMatch = re.match(OtherRegex, textString)
        if(otherRegexMatch):
            textString = add_new_lexeme(otherRegexMatch, textString, lineNumber, 'Other Literals')
            continue
        
        print("No match: ", textString)
        break
    

    print("Final: ",textString, "\nLength: ", len(textString))
    print(ListOfLexemes)

fileName = "F:\\2S A.Y. 2021-2022\\CMSC 124 Project JUST DO IT BY MARCH DAMIT\\a.lol"
file = open(fileName, "r")
fileText = file.read()
fileText = fileText.replace("\n", " \n")
# fileText += " "
# print(fileText)
# return_list_of_lexemes(fileText)
# print_lexeme_list(ListOfLexemes)