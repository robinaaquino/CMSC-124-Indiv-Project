# Robina Rhamz M. Aquino
# CMSC 124 <section>
#
# This program is an individual implementation of the LOL interpreter

# Code Conventions
# Functions in snake_case
# Variables in camelCase
# Global variables in PascalCase
# Constant variables in ALLCAPS

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from lex import *
from grammar import *
from objectDefinition import *
from utilityFunctions import *

N = 1
# create main window
MainWindow = Tk()

# create a title for the window
MainWindow.title("LOL Interpreter vers. CMSC124")
# MainWindow.geometry("900x400")
MainWindow.config(bg='skyblue')

# TODO
# Switch from pack to grid

# key binds
# alt + k + 0 collapse
# alt + k + j expand

# bookmarks
# cltr + alt + k bookmark
# ctrl + alt + l next
# ctrl + alt + j prev

#global variables
CurrentlyAccessedFile = ''  # file opened by user

# functions

# ui functions

##################################
# def save_user_input_function():
#     global UserInputValue

#     UserInputValue = TextArea.get("1.0", END)[0:-1]

# # Function that is used to get user input
# # Accepts no arguments
# def open_user_input_window():
#     print('is this running?')
#     UserWindow = Toplevel(MainWindow)

#     UserInputTextArea = Text(UserWindow)
#     UserInputInputButton = Button(UserWindow, text="Enter", command=save_user_input_function)
##################################

# Function that is used to load a text file
# Accepts no arguments
# Sets the CurrentlyAccessedFile variable
def load_text():  # function used to load a text
    global CurrentlyAccessedFile  # access the global variable
    fileName = filedialog.askopenfilename(initialdir="C:/Users/Harlight/Documents", filetypes=[
                                          ("LOL files", "*.lol*"), ("asda", "*.txt")])  # open file dialog to select a file

    if fileName:  # if user selected a file
        try:
            # set the file directory shown in the ui
            FileDirectory.set(fileName)
            CurrentlyAccessedFile = fileName  # set the fileName to the global variable

            fileData = open(fileName, "r")  # open the file in read mode
            file_contents = fileData.read()  # read the file

            # delete the contents of the text area, if any
            TextArea.delete("1.0", "end")
            # insert the contents of the file to the text area
            TextArea.insert(END, file_contents)
            fileData.close()  # close the file
        except:
            # show an error if an error occurs
            messagebox.showerror(
                title="Error", message="Error in selecting a file")

# Function that is called when the Execute button is clicked
# Accepts no arguments
# Runs different functions
# Gets text from text area and writes to file
# Updates lexeme table based on text from text area
def execute_function():  # function used to set a text
    global CurrentlyAccessedFile  # access the file
    global ListOfLexemes
    global ListOfSymbols

    if CurrentlyAccessedFile:

        # get the current contents of the text area
        currentTextAreaContents = TextArea.get("1.0", END)[0:-1] #.get always adds a newline so it needs to be sliced
        # write to the selected text file

        fileData = open(CurrentlyAccessedFile, "w")
        fileData.write(currentTextAreaContents)

        # fileText = currentTextAreaContents.replace(
        #     "\n", "\n")  # set new lines as separate strings 
        fileText = currentTextAreaContents
        fileText = fileText.replace("\n", " \n")
        #ATTEMPT TO FIX BUG

        ListOfLexemes.clear()  # clear global variable before adding more lexemes
        ListOfSymbols.clear()  # clear global variable before adding more lexemes
        ResultText = "" # clear global result text

        return_list_of_lexemes(fileText)  # parse the file
        # print_lexeme_list(ListOfLexemes)
        fileData.close()  # close the file

        for item in LexemeTableFrame.get_children():  # delete contents in table if any
            LexemeTableFrame.delete(item)

        lexeme_table_row_counter = 0  # initialize identifier for table rows
        for i in range(len(ListOfLexemes)):  # iterate over each lexeme in ListOfLexemes
            # do not include new lines in table
            if(ListOfLexemes[i].classification == "New Line"):
                continue
            LexemeTableFrame.insert(parent='', index='end', iid=lexeme_table_row_counter, text='', values=(
                ListOfLexemes[i].string, ListOfLexemes[i].lineNumber, ListOfLexemes[i].classification))  # insert each lexeme to the table
            lexeme_table_row_counter += 1  # increment identifier for table rows

        ResultText = return_list_of_symbols() #parse the lexemes

        for item in SymbolTableFrame.get_children():  # delete contents in table if any
            SymbolTableFrame.delete(item)

        symbol_table_row_counter = 0  # initialize identifier for table rows
        for i in range(len(ListOfSymbols)):  # iterate over each lexeme in ListOfSymbols
            SymbolTableFrame.insert(parent='', index='end', iid=symbol_table_row_counter, text='', values=(
                ListOfSymbols[i].identifier, ListOfSymbols[i].value))  # insert each symbol to the table
            symbol_table_row_counter += 1  # increment identifier for table rows

        #result in console
        if(len(ResultText) != 0):
            ConsoleArea.delete("1.0", END) #delete contents in console
            ConsoleArea.insert(END, ResultText) #put new contents in console

    else:
        # show an error when trying to execute without a file
        messagebox.showerror(title="Error", message="No selected file")


# TopFrame
TopFrame = Frame(MainWindow)
TopFrame.pack(ipadx=10, ipady=10)

#text frame
TextFrame = Frame(TopFrame)
TextFrame.pack(ipadx=10, ipady=10, side=LEFT)
TextFrameUpper = Frame(TextFrame)
TextFrameLower = Frame(TextFrame)
TextFrameUpper.pack(ipadx=10, ipady=10, side=TOP)
TextFrameLower.pack(ipadx=10, ipady=10, side=BOTTOM)

#widgets for text frame
FileDirectory = StringVar() #variable for holding file name
FileDirectory.set('No file selected')
FileDirectoryLabel = Label(TextFrameUpper, textvariable=FileDirectory)
FileDirectoryLabel.pack(padx=5, pady=5, fill=X, expand=TRUE, side=LEFT)

SelectFileButton = Button(TextFrameUpper, text="Select file", command=load_text)
SelectFileButton.pack(padx=5, pady=5, fill=X, expand=TRUE,side=RIGHT)

TextArea = Text(TextFrameLower)
TextArea.pack(padx=5, pady=5, expand=TRUE, fill=BOTH, side=LEFT)

#lexeme frame
LexemeFrame = Frame(TopFrame)
LexemeFrame.pack(ipadx=10, ipady=10, expand=TRUE, fill=BOTH, side=LEFT)
LexemeFrameYScrollbar = Scrollbar(LexemeFrame)
LexemeFrameYScrollbar.pack(side=LEFT, fill=Y) #TODO GUI ISSUES WITH SCROLLBAR

#widgets for lexeme frame
LexemeTableFrame = ttk.Treeview(LexemeFrame, yscrollcommand=LexemeFrameYScrollbar.set)
LexemeFrameYScrollbar.config(command=LexemeTableFrame.yview)

LexemeTableFrame['columns'] = (
    'lexeme', 'line_number', 'classification')  # set columns
LexemeTableFrame.column('#0', width=0, stretch=NO)
LexemeTableFrame.column('lexeme', anchor=CENTER, width=80)
LexemeTableFrame.column('line_number', anchor=CENTER, width=80)
LexemeTableFrame.column('classification', anchor=CENTER, width=120)

# set headings of columns
LexemeTableFrame.heading('#0', text="Lexeme", anchor=CENTER)
LexemeTableFrame.heading('lexeme', text="Lexeme", anchor=CENTER)
LexemeTableFrame.heading('line_number', text="Line Number", anchor=CENTER)
LexemeTableFrame.heading(
    'classification', text="Classification", anchor=CENTER)
LexemeTableFrame.pack(padx=5, pady=5, expand=TRUE, fill=BOTH, side=LEFT)

#symbol frame
SymbolFrame = Frame(TopFrame)
SymbolFrame.pack(ipadx=10, ipady=10, expand=TRUE, fill=BOTH, side=LEFT)
SymbolFrameYScrollbar = Scrollbar(SymbolFrame)
SymbolFrameYScrollbar.pack(side=LEFT, fill=Y)

#widgets for symbol frame
SymbolTableFrame = ttk.Treeview(LexemeFrame, yscrollcommand=SymbolFrameYScrollbar.set)
SymbolFrameYScrollbar.config(command=SymbolTableFrame.yview)

SymbolTableFrame['columns'] = (
    'identifier', 'value')  # set columns
SymbolTableFrame.column('#0', width=0, stretch=NO)
SymbolTableFrame.column('identifier', anchor=CENTER, width=80)
SymbolTableFrame.column('value', anchor=CENTER, width=80)

# set headings of columns
SymbolTableFrame.heading('#0', text="Symbol", anchor=CENTER)
SymbolTableFrame.heading('identifier', text="Identifier", anchor=CENTER)
SymbolTableFrame.heading('value', text="Value", anchor=CENTER)
SymbolTableFrame.pack(padx=5, pady=5, expand=TRUE, fill=BOTH, side=LEFT)

#middle frame
MiddleFrame = Frame(MainWindow)
MiddleFrame.pack(ipadx=10, ipady=10, expand=TRUE, fill=BOTH)

#widgets for middle frame
ExecuteButton = Button(MiddleFrame, text="Execute", command=execute_function)
ExecuteButton.pack(padx=5, pady=5)

#bottom frame
BottomFrame = Frame(MainWindow)
BottomFrame.pack(ipadx=10, ipady=10, expand=TRUE, fill=BOTH)

ConsoleArea = Text(BottomFrame)
ConsoleArea.pack(padx=5, pady=5, expand=TRUE, fill=BOTH, side=LEFT)

MainWindow.mainloop()
