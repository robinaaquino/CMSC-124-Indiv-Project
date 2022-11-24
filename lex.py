from objectDefinition import *
from utilityFunctions import *
import re

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
ArithmeticMathOperatorRegex = "(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF)\s"
ComparisonMathOperatorRegex = "(BIGGR OF|SMALLR OF)\s"
BoolOperatorRegex = "(BOTH OF|EITHER OF|WON OF)\s"
InfiniteBoolOperatorRegex = "(ANY OF|ALL OF)\s"
NotBoolOperatorRegex = "NOT\s"

ComparisonOperatorRegex = "(BOTH SAEM|DIFFRINT)\s"
ConcatenationOperatorRegex = "SMOOSH\s"
ExpressionAndOperatorRegex = "AN\s"

#comments
InlineCommentDelimiterRegex = "BTW\s"
MultiCommentDelimiterStartRegex = "OBTW\s"
MultiCommentDelimiterEndRegex = "TLDR\n"

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
LoopDelimiterEndRegex = "IM OUTTA YR\s"
ArgumentOperatorRegex = "YR\s"
LoopConditionRegex = "(TIL|WILE)\s"
LoopBreakOperatorRegex = "GTFO\s"

#unary
UnaryMathOperatorRegex = "(UPPIN|NERFIN)\s"
InfinityArityDelimiterEndRegex = "MKAY\s"

SoftbreakRegex = "\,"

#regex for all classifications
IdentifierRegex = "[A-Za-z]+[A-Za-z0-9_]*\s" #regex to identify variable names

#regex for literals
NumbrLiteralRegex = "(-[1-9][0-9]*|[1-9][0-9]*|[0])\s" #regex to identify integers
NumbarLiteralRegex = "(-?[0-9]*)\.[0-9]*[1-9]\s" #regex to identify floats
#TODO (-?[0-9]*)\.([0-9]+)\s change to this? allow 1.0000 and 1.01000 when converted to int and float, is parsed automatically
#if not check typecast_value

TroofLiteralRegex = "(WIN|FAIL)\s" #regex for boolean values
TypeLiteralRegex = "(NOOB|NUMBR|NUMBAR|TROOF|YARN)\s" #regex for types
YarnLiteralRegex = "\".+\"\s" #regex to identify strings

NewLineRegex = "\n" #regex to identify new line
OtherRegex = ".*" #regex to identify any word that doesn't 
MultiLineCommentRegex = ".+(\s)?" #regex to identify any comment separated by whitespace
CommentRegex = ".+" #regex to identify any comment not separated by whitespace

#next step, catch all tokens split by spaces and newlines


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
    #TODO maybe add a way to strip the lines? no, maybe just remove whitespaces at the end and start of the text yea

    global ListOfLexemes

    lineNumber = 1

    while len(textString) > 0:

        #check if matched with code delimiters
        codeDelimiterStartRegexMatch = re.match(CodeDelimiterStartRegex, textString)
        if(codeDelimiterStartRegexMatch):
            textString = add_new_lexeme(codeDelimiterStartRegexMatch, textString, lineNumber, 'Code Delimiter Start')
            continue

        codeDelimiterEndRegexMatch = re.match(CodeDelimiterEndRegex, textString)
        if(codeDelimiterEndRegexMatch):
            textString = add_new_lexeme(codeDelimiterEndRegexMatch, textString, lineNumber, 'Code Delimiter End')
            continue

        #check if matched with variable declaration and assignment
        varDeclarationRegexMatch = re.match(VarDeclarationRegex, textString)
        if(varDeclarationRegexMatch):
            textString = add_new_lexeme(varDeclarationRegexMatch, textString, lineNumber, 'Variable Declaration')
            continue

        varDeclarationAssignmentRegexMatch = re.match(VarDeclarationAssignmentRegex, textString)
        if(varDeclarationAssignmentRegexMatch):
            textString = add_new_lexeme(varDeclarationAssignmentRegexMatch, textString, lineNumber, 'Variable Declaration Assignment')
            continue

        varAssignmentRegexMatch = re.match(VarAssignmentRegex, textString)
        if(varAssignmentRegexMatch):
            textString = add_new_lexeme(varAssignmentRegexMatch, textString, lineNumber, 'Variable Assignment')
            continue

        #check if matched with operators
        mathOperatorRegexMatch = re.match(ArithmeticMathOperatorRegex, textString)
        if(mathOperatorRegexMatch):
            textString = add_new_lexeme(mathOperatorRegexMatch, textString, lineNumber, 'Arithmetic Math Operator')
            continue

        comparisonMathOperatorRegexMatch = re.match(ComparisonMathOperatorRegex, textString)
        if(comparisonMathOperatorRegexMatch):
            textString = add_new_lexeme(comparisonMathOperatorRegexMatch, textString, lineNumber, 'Comparison Math Operator')
            continue

        boolOperatorRegexMatch = re.match(BoolOperatorRegex, textString)
        if(boolOperatorRegexMatch):
            textString = add_new_lexeme(boolOperatorRegexMatch, textString, lineNumber, 'Boolean Operator')
            continue

        infiniteBoolOperatorRegexMatch = re.match(InfiniteBoolOperatorRegex, textString)
        if(infiniteBoolOperatorRegexMatch):
            textString = add_new_lexeme(infiniteBoolOperatorRegexMatch, textString, lineNumber, 'Infinite Boolean Operator')
            continue

        notBoolOperatorRegexMatch = re.match(NotBoolOperatorRegex, textString)
        if(notBoolOperatorRegexMatch):
            textString = add_new_lexeme(notBoolOperatorRegexMatch, textString, lineNumber, 'Not Boolean Operator')
            continue

        comparisonOperatorRegexMatch = re.match(ComparisonOperatorRegex, textString)
        if(comparisonOperatorRegexMatch):
            textString = add_new_lexeme(comparisonOperatorRegexMatch, textString, lineNumber, 'Comparison Operator')
            continue

        concatenationOperatorRegexMatch = re.match(ConcatenationOperatorRegex, textString)
        if(concatenationOperatorRegexMatch):
            textString = add_new_lexeme(concatenationOperatorRegexMatch, textString, lineNumber, 'Concatenation Operator')
            continue

        expressionAndOperatorRegexMatch = re.match(ExpressionAndOperatorRegex, textString)
        if(expressionAndOperatorRegexMatch):
            textString = add_new_lexeme(expressionAndOperatorRegexMatch, textString, lineNumber, 'Expression AND Operator')
            continue

        #TODO NO HANDLER FOR COMMENTS AFTER INLINE COMMENT DELIMITER LEL

        #check if matched with comments
        inlineCommentDelimiterRegexMatch = re.match(InlineCommentDelimiterRegex, textString)
        if(inlineCommentDelimiterRegexMatch):
            textString = add_new_lexeme(inlineCommentDelimiterRegexMatch, textString, lineNumber, 'Inline Comment Delimiter')

            while len(textString) > 0:
                newLineRegexMatch = re.match(NewLineRegex, textString)
                if(newLineRegexMatch):
                    textString = add_new_lexeme(newLineRegexMatch, textString, lineNumber, 'New Line')
                    lineNumber+=1
                    break

                CommentRegexMatch = re.match(CommentRegex, textString)
                if(CommentRegexMatch):
                    textString = add_new_lexeme(CommentRegexMatch, textString, lineNumber, 'Comment')
                    continue

            continue

        multiCommentDelimiterStartRegexMatch = re.match(MultiCommentDelimiterStartRegex, textString)
        if(multiCommentDelimiterStartRegexMatch):
            textString = add_new_lexeme(multiCommentDelimiterStartRegexMatch, textString, lineNumber, 'Multi-line Comment Delimiter Start')

            # loop until there's the end delimiter
            while len(textString) > 0:
                multiCommentDelimiterEndRegexMatch = re.match(MultiCommentDelimiterEndRegex, textString)
                if(multiCommentDelimiterEndRegexMatch):
                    textString = add_new_lexeme(multiCommentDelimiterEndRegexMatch, textString, lineNumber, 'Multi-line Comment Delimiter End')
                    break

                MultiLineCommentRegexMatch = re.match(MultiLineCommentRegex, textString)
                if(MultiLineCommentRegexMatch):
                    textString = add_new_lexeme(MultiLineCommentRegexMatch, textString, lineNumber, 'Comment')
                    continue
                print(len(textString))
                print(textString)
            continue
        
        multiCommentDelimiterEndRegexMatch = re.match(MultiCommentDelimiterEndRegex, textString)
        if(multiCommentDelimiterEndRegexMatch):
            textString = add_new_lexeme(multiCommentDelimiterEndRegexMatch, textString, lineNumber, 'Multi-line Comment Delimiter End')
            continue

        #check if matched with casting
        castingOperatorRegexMatch = re.match(CastingOperatorRegex, textString)
        if(castingOperatorRegexMatch):
            textString = add_new_lexeme(castingOperatorRegexMatch, textString, lineNumber, 'Casting Operator')
            continue

        typecastOperatorStartRegexMatch = re.match(TypecastOperatorStartRegex, textString)
        if(typecastOperatorStartRegexMatch):
            textString = add_new_lexeme(typecastOperatorStartRegexMatch, textString, lineNumber, 'Typecast Operator Start')
            continue

        typecastOperatorMidRegexMatch = re.match(TypecastOperatorMidRegex, textString)
        if(typecastOperatorMidRegexMatch):
            textString = add_new_lexeme(typecastOperatorMidRegexMatch, textString, lineNumber, 'Typecast Operator Mid')
            continue

        #check if matched with output and input
        outputRegexMatch = re.match(OutputRegex, textString)
        if(outputRegexMatch):
            textString = add_new_lexeme(outputRegexMatch, textString, lineNumber, 'Output')
            continue

        inputRegexMatch = re.match(InputRegex, textString)
        if(inputRegexMatch):
            textString = add_new_lexeme(inputRegexMatch, textString, lineNumber, 'Input')
            continue

        #check if matched with condition
        conditionalDelimiterIfElseStartRegexMatch = re.match(ConditionDelimiterIfElseStartRegex, textString)
        if(conditionalDelimiterIfElseStartRegexMatch):
            textString = add_new_lexeme(conditionalDelimiterIfElseStartRegexMatch, textString, lineNumber, 'Conditional Delimiter If Else Start')
            continue

        conditionalIfRegexMatch = re.match(ConditionalIfRegex, textString)
        if(conditionalIfRegexMatch):
            textString = add_new_lexeme(conditionalIfRegexMatch, textString, lineNumber, 'Conditional If')
            continue

        conditionalElifRegexMatch = re.match(ConditionalElifRegex, textString)
        if(conditionalElifRegexMatch):
            textString = add_new_lexeme(conditionalElifRegexMatch, textString, lineNumber, 'Conditional Elif')
            continue

        conditionalElseRegexMatch = re.match(ConditionalElseRegex, textString)
        if(conditionalElseRegexMatch):
            textString = add_new_lexeme(conditionalElseRegexMatch, textString, lineNumber, 'Conditional Else')
            continue

        conditionalDelimiterEndRegexMatch = re.match(ConditionalDelimiterEndRegex, textString)
        if(conditionalDelimiterEndRegexMatch):
            textString = add_new_lexeme(conditionalDelimiterEndRegexMatch, textString, lineNumber, 'Conditional Delimiter End')
            continue

        #check if matched with switch
        conditionalDelimiterSwitchStartRegexMatch = re.match(ConditionalDelimiterSwitchStartRegex, textString)
        if(conditionalDelimiterSwitchStartRegexMatch):
            textString = add_new_lexeme(conditionalDelimiterSwitchStartRegexMatch, textString, lineNumber, 'Conditional Delimiter Switch Start')
            continue

        conditionalSwitchRegexMatch = re.match(ConditionalSwitchRegex, textString)
        if(conditionalSwitchRegexMatch):
            textString = add_new_lexeme(conditionalSwitchRegexMatch, textString, lineNumber, 'Conditional Switch')
            continue

        conditionalSwitchLastRegexMatch = re.match(ConditionalSwitchLastRegex, textString)
        if(conditionalSwitchLastRegexMatch):
            textString = add_new_lexeme(conditionalSwitchLastRegexMatch, textString, lineNumber, 'Conditional Switch Last')
            continue

        #check if matched with loop
        loopDelimiterStartRegexMatch = re.match(LoopDelimiterStartRegex, textString)
        if(loopDelimiterStartRegexMatch):
            textString = add_new_lexeme(loopDelimiterStartRegexMatch, textString, lineNumber, 'Loop Delimiter Start')
            continue

        loopDelimiterEndRegexMatch = re.match(LoopDelimiterEndRegex, textString)
        if(loopDelimiterEndRegexMatch):
            textString = add_new_lexeme(loopDelimiterEndRegexMatch, textString, lineNumber, 'Loop Delimiter End')
            continue

        argumentOperatorRegexMatch = re.match(ArgumentOperatorRegex, textString)
        if(argumentOperatorRegexMatch):
            textString = add_new_lexeme(argumentOperatorRegexMatch, textString, lineNumber, 'Argument Operator')
            continue

        loopConditionRegexMatch = re.match(LoopConditionRegex, textString)
        if(loopConditionRegexMatch):
            textString = add_new_lexeme(loopConditionRegexMatch, textString, lineNumber, 'Loop Condition')
            continue

        loopBreakOperatorRegexMatch = re.match(LoopBreakOperatorRegex, textString)
        if(loopBreakOperatorRegexMatch):
            textString = add_new_lexeme(loopBreakOperatorRegexMatch, textString, lineNumber, 'Loop Break Operator')
            continue

        #check if matched with unary
        unaryMathOperatorRegexMatch = re.match(UnaryMathOperatorRegex, textString)
        if(unaryMathOperatorRegexMatch):
            textString = add_new_lexeme(unaryMathOperatorRegexMatch, textString, lineNumber, 'Unary Math Operator')
            continue

        infiniteArityDelimiterEndRegexMatch = re.match(InfinityArityDelimiterEndRegex, textString)
        if(infiniteArityDelimiterEndRegexMatch):
            textString = add_new_lexeme(infiniteArityDelimiterEndRegexMatch, textString, lineNumber, 'Infinite Arity Delimiter End')
            continue

        #check if matched with softbreak
        softbreakRegexMatch = re.match(SoftbreakRegex, textString)
        if(softbreakRegexMatch):
            textString = add_new_lexeme(softbreakRegexMatch, textString, lineNumber, 'Softbreak')
            continue

        #check if matched with new line
        newLineRegexMatch = re.match(NewLineRegex, textString)
        if(newLineRegexMatch):
            textString = add_new_lexeme(newLineRegexMatch, textString, lineNumber, 'New Line')
            lineNumber+=1
            continue

        #check if matched with numbar literal
        NumbarLiteralRegexMatch = re.match(NumbarLiteralRegex, textString)
        if(NumbarLiteralRegexMatch):
            print(NumbarLiteralRegexMatch)
            textString = add_new_lexeme(NumbarLiteralRegexMatch, textString, lineNumber, 'Numbar Literal')
            continue

        #check if matched with numbar literal
        NumbrLiteralRegexMatch = re.match(NumbrLiteralRegex, textString)
        if(NumbrLiteralRegexMatch):
            textString = add_new_lexeme(NumbrLiteralRegexMatch, textString, lineNumber, 'Numbr Literal')
            continue
        
        #check if matched with yarn literal
        yarnLiteralRegexMatch = re.match(YarnLiteralRegex, textString)
        if(yarnLiteralRegexMatch):
            textString = add_new_lexeme(yarnLiteralRegexMatch, textString, lineNumber, 'Yarn Literal')
            continue

        #check if matched with troof literal
        troofLiteralRegexMatch = re.match(TroofLiteralRegex, textString)
        if(troofLiteralRegexMatch):
            textString = add_new_lexeme(troofLiteralRegexMatch, textString, lineNumber, 'Troof Literal')
            continue

        #check if matched with type literal
        typeLiteralRegexMatch = re.match(TypeLiteralRegex, textString)
        if(typeLiteralRegexMatch):
            textString = add_new_lexeme(typeLiteralRegexMatch, textString, lineNumber, 'Type Literal')
            continue

        #check if matched with identifiers
        identifierRegexMatch = re.match(IdentifierRegex, textString)
        if(identifierRegexMatch):
            textString = add_new_lexeme(identifierRegexMatch, textString, lineNumber, 'Identifier')
            continue

        #check if matched with anything else
        otherRegexMatch = re.match(OtherRegex, textString)
        if(otherRegexMatch):
            textString = add_new_lexeme(otherRegexMatch, textString, lineNumber, 'Other Literals')
            continue
        
        print("No match: ", textString)
        break
    

    # print("Final: ",textString, "\nLength: ", len(textString))
    # print(ListOfLexemes)

# fileName = "F:\\2S A.Y. 2021-2022\\CMSC 124 Project JUST DO IT BY MARCH DAMIT\\a.lol"
# file = open(fileName, "r")
# fileText = file.read()
# fileText = fileText.replace("\n", " \n")
# fileText += " "
# print(fileText)
# return_list_of_lexemes(fileText)
# print_lexeme_list(ListOfLexemes)