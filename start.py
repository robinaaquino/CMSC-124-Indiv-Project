# Robina Rhamz M. Aquino
# CMSC 124 <section>
#
# This program is an individual implementation of the LOL interpreter

# Code Conventions
#Functions in snake_case
#Variables in camelCase
# Global variables in PascalCase
# Constant variables in ALLCAPS

from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox
from lex import *

N = 1

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

    if CurrentlyAccessedFile:

        # get the current contents of the text area
        currentTextAreaContents = TextArea.get("1.0", END)
        # write to the selected text file
        fileData = open(CurrentlyAccessedFile, "w")
        fileData.write(currentTextAreaContents)

        fileText = currentTextAreaContents.replace(
            "\n", " \n")  # set new lines as separate strings
        ListOfLexemes.clear()  # clear global variable before adding more lexemes
        return_list_of_lexemes(fileText)  # parse the file
        fileData.close()  # close the file

        for item in LexemeTableFrame.get_children():  # delete contents in table if any
            LexemeTableFrame.delete(item)

        table_row_counter = 0  # initialize identifier for table rows
        for i in range(len(ListOfLexemes)):  # iterate over each lexeme in ListOfLexemes
            # do not include new lines in table
            if(ListOfLexemes[i].classification == "New Line"):
                continue
            LexemeTableFrame.insert(parent='', index='end', iid=table_row_counter, text='', values=(
                ListOfLexemes[i].string, ListOfLexemes[i].lineNumber, ListOfLexemes[i].classification))  # insert each lexeme to the table
            table_row_counter += 1  # increment identifier for table rows

    else:
        # show an error when trying to execute without a file
        messagebox.showerror(title="Error", message="No selected file")


# create main window
MainWindow = Tk()

# create a title for the window
MainWindow.title("LOL Interpreter vers. CMSC124")
MainWindow.geometry("800x400")

# frames
# text frames for file selection and text area
TextFrame = Frame(MainWindow)
TextFrameUpper = Frame(TextFrame)
TextFrameLower = Frame(TextFrame)
TextFrame.pack()
TextFrameUpper.pack(fill=BOTH, expand=True, side=TOP)
TextFrameLower.pack(fill=BOTH, expand=True, side=BOTTOM)

# ExecuteFrame for the button
ExecuteFrame = Frame(MainWindow)
ExecuteFrame.pack()

# LexemeFrame for the lexemes and classificaiton
LexemeFrame = Frame(MainWindow)
LexemeFrame.pack()
LexemeFrameYScrollbar = Scrollbar(LexemeFrame)
LexemeFrameYScrollbar.pack(side=RIGHT, fill=Y)


# widgets for text frame
FileDirectory = StringVar()
FileDirectory.set('(/(=w=)?')
FileDirectoryLabel = Label(TextFrameUpper, textvariable=FileDirectory)
FileDirectoryLabel.pack(side=LEFT, padx=5, pady=5)

SelectFileButton = Button(TextFrameUpper, text="*(*w*)*", command=load_text)
SelectFileButton.pack(side=RIGHT, padx=5, pady=5)

TextArea = Text(TextFrameLower, height=5, width=52)
TextArea.pack(padx=5, pady=5)

# widgets for execute frame
ExecuteButton = Button(ExecuteFrame, text="\(owo)/", command=execute_function)
ExecuteButton.pack(padx=5, pady=5)

# widgets for lexeme table frame
LexemeTableFrame = ttk.Treeview(
    LexemeFrame, yscrollcommand=LexemeFrameYScrollbar.set)
LexemeTableFrame.pack()

# set scrollbar to access y view
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

LexemeTableFrame.pack()

MainWindow.mainloop()
