import re

class Lexeme:
    def __init__(self, string, classification, lineNumber):
        self.string = string
        self.classification = classification
        self.lineNumber = lineNumber

listOfLexemes = []

identifierRegex = "[A-Za-z]+[A-Za-z0-9_]*\s"

yarnLiteral = "\".*\"\s"

#next step, catch all tokens split by spaces and newlines

def PrintLexemeList(lexemeList):
    for counter in range(len(lexemeList)):
        lexeme = lexemeList[counter]
        print("\nCount: ", counter)
        print("String: ", lexeme.string)
        print("Classification: ", lexeme.classification)
        print("Line Number: ", lexeme.lineNumber)

def ReturnListOfLexemes(textString):
    global listOfLexemes

    #split via new lines
    print("Text: \n", textString, "\n")

    print("Lexemes: \n")
    lineNumber = 0
    while len(textString) > 0:
        #check if matched with identifiers
        identifierMatch = re.match(identifierRegex, textString)
        if(identifierMatch):
            textString = textString.replace(identifierMatch.group(), "")
            print("identifier match:", textString, ":")
            identifierLexeme = Lexeme(identifierMatch.group(), "Identifier", lineNumber)
            listOfLexemes.append(identifierLexeme)
            continue

        #check if matched with yarn literal
        yarnLiteralMatch = re.match(yarnLiteral, textString)
        if(yarnLiteralMatch):
            textString = textString.replace(yarnLiteralMatch.group(), "")
            identifierLexeme = Lexeme(yarnLiteralMatch.group(), "Yarn Literal", lineNumber)
            listOfLexemes.append(identifierLexeme)
            continue

        print(textString)
        break
    

fileName = "C:\\Users\\Arthur Aquino\\Documents\\School Documents\\2S A.Y. 2021-2022\\CMSC 124 Project JUST DO IT BY MARCH DAMIT\\a.lol"
file = open(fileName, "r")
ReturnListOfLexemes(file.read())
# PrintLexemeList(listOfLexemes)