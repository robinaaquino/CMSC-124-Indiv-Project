from asyncio.windows_events import NULL
from gettext import NullTranslations
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox

from lex import *

#key binds
#alt + k + 0 collapse
#alt + k + j expand

#bookmarks
#cltr + alt + k bookmark
#ctrl + alt + l next
#ctrl + alt + j prev


#global variables
currently_accessed_file = NULL #file opened by user

#functions

#ui functions
def load_text(): #function used to load a text
    global currently_accessed_file 
    file_name = filedialog.askopenfilename(initialdir="C:/Users/Harlight/Documents",filetypes=[("LOL files", "*.lol*"), ("asda", "*.txt")])
    
    if file_name: #if user selected a file
        try:
            file_directory.set(file_name) #set the file directory shown in the ui
            currently_accessed_file = file_name #set the file_name to the global variable

            file_data = open(file_name, "r") #read the file
            file_contents = file_data.read()

            text_area.delete("1.0", "end") #delete the contents of the text area, if any
            text_area.insert(END, file_contents) #insert the contents of the file to the text area
            file_data.close() #close the file
        except:
            messagebox.showerror(title="Error", message="Error in selecting a file") #show an error

def execute_function(): #function used to set a text
    global currently_accessed_file #access the file
    if currently_accessed_file:
        print(currently_accessed_file)
        current_text_area_contents = text_area.get("1.0", END) #get the current contents of the text area
        file_data = open(currently_accessed_file, "w") #write to the selected text file
        file_data.write(current_text_area_contents)
        ReturnListOfLexemes(current_text_area_contents)
        file_data.close()
    else:
        messagebox.showerror(title="Error", message="No selected file") #show an error when trying to execute without a file

#create main window
main_window = Tk()

main_window.title("LOL Interpreter vers. CMSC124")#create a title for the window
main_window.geometry("800x400")

#frames
#text frames for file selection and text area
text_frame = Frame(main_window)
text_frame_upper = Frame(text_frame)
text_frame_lower = Frame(text_frame)
text_frame.pack()
text_frame_upper.pack(fill=BOTH, expand=True, side=TOP)
text_frame_lower.pack(fill=BOTH, expand=True, side=BOTTOM)

#execute_frame for the button
execute_frame = Frame(main_window)
execute_frame.pack()

#widgets for text frame
file_directory = StringVar()
file_directory.set('(/(=w=)?')
file_directory_label = Label(text_frame_upper, textvariable=file_directory)
file_directory_label.pack(side=LEFT, padx=5, pady=5)

select_file_button = Button(text_frame_upper, text="*(*w*)*", command=load_text)
select_file_button.pack(side=RIGHT, padx=5, pady=5)

text_area = Text(text_frame_lower, height=5, width=52)
text_area.pack(padx=5,pady=5)

#widgets for execute frame
execute_button = Button(execute_frame, text="\(owo)/", command=execute_function)
execute_button.pack(padx=5,pady=5)

main_window.mainloop()