""" GUU interpreter
    powered by python
    made by Michael Makarov """

# importing the library for GUI console
import tkinter as TK
from tkinter import messagebox
from tkinter.filedialog import askopenfilename

# default font
myfont = "Times 10 bold italic"
# the default console parameters
console_name = "GUU CONSOLE"
typefile = (("Text files", "*.txt"),)
# list of variables
list_var = dict()
# list of functions
list_func = dict()
# flag of the entering into the main function
main_enter = False
# all usefull functions
# file opening function
def open_file():
    filename = askopenfilename(filetypes = typefile)
    opened_file = False
    try:
        fileread = open(filename, mode = "r")
        opened_file = True
    except FileNotFoundError:
        messagebox.showinfo("Warning", "Could not open file")
    if opened_file:
        console_entry.insert(TK.END, "PROGRAMM: " + filename + "\n" )
        text = ""
        line = fileread.readline()
        while line:
            text += line
            line = fileread.readline()
        commands = [q for w in text.split("\n") for t in w.split("\t") for q in t.split(" ") if q != ""]
        index = 0
        while index < len(commands):
            if commands[index] == new_func:
                i = index + 2
                array = list()
                while i < len(commands) and commands[i] != new_func:
                    array.append(commands[i])
                    i += 1
                list_func[commands[index + 1]] = array
                index = i
# functions of the implementation related to the language
# set variable
def set_function(pair):
    list_var[pair[0]] = pair[1]
    return 3
# print function
def print_function(variable):
    console_entry.insert(TK.END, "\n" + variable + " = " + list_var[variable])
    return 2
# processing the function when there was callback
def callback_function(function):
    func_commands = list_func[function]
    index = 0
    while index < len(func_commands):
        if func_commands[index] == list_com[0]:
            index += com_choice[func_commands[index]]((func_commands[index + 1], func_commands[index + 2]))
        else:
            index += com_choice[func_commands[index]](func_commands[index + 1])
    return 2
# functions of the implementation related to the debugger
# when input i 
def input_i_function(main_commands):
    index = 0
    while index < len(main_commands):
        if main_commands[index] == list_com[0]:
            index += com_choice[main_commands[index]]((main_commands[index + 1], main_commands[index + 2]))
        else:
            index += com_choice[main_commands[index]](main_commands[index + 1])
    return True
# when input o
def input_o_function(main_commands):
    index = 0
    while index < len(main_commands):
        if main_commands[index] == list_com[0]:
            index += com_choice[main_commands[index]]((main_commands[index + 1], main_commands[index + 2]))
        elif main_commands[index] == list_com[2]: index += 2
        else:
            index += com_choice[main_commands[index]](main_commands[index + 1])
    return True
# when input trace
def input_trace_function(main_commands):
    index = 0
    counter_com = 1
    console_entry.insert(TK.END, "\nImplementation of the main function:")
    while index < len(main_commands):
        splitter = "\n" + str(counter_com) + ")  "
        if main_commands[index] == list_com[0]:
            console_entry.insert(TK.END, splitter + main_commands[index] + " " +
                                     main_commands[index + 1] + " " + main_commands[index + 2])
            index += 3
        elif main_commands[index] == list_com[1] or main_commands[index] == list_com[2]:
            console_entry.insert(TK.END, splitter + main_commands[index] + " " +
                                     main_commands[index + 1])
            index += 2
        counter_com += 1
    return True
# when input var
def input_var_function(main_commands):
    console_entry.insert(TK.END, "\nVariables:")
    for variable in list_var:
        console_entry.insert(TK.END, "\n" + variable + " = " + list_var[variable])
    return True
# the choices of the functions and user's inputs
new_func = "sub"
main_func = "main"
list_com = ["set" , "print" , "call" ]
com_choice = {list_com[0] : set_function,
              list_com[1] : print_function,
              list_com[2] : callback_function}
list_input = ["i", "o", "trace", "var"]
input_choice = {list_input[0] : input_i_function,
                list_input[1] : input_o_function,
                list_input[2] : input_trace_function,
                list_input[3] : input_var_function}
# processing thecursor motion
def motion(event):
    current_pos = float(console_entry.index(TK.INSERT)) + 1.0
##    print(current_pos, last_pos[0])
    if current_pos < last_pos[0]: console_entry.config(state = TK.DISABLED)
    else: console_entry.config(state = TK.NORMAL)
    last_pos[0] = max(float(console_entry.index(TK.END)), last_pos[0])
# returning the contents
def return_line(event):
    last_pos = float(console_entry.index(TK.END))
    current_pos = float(console_entry.index(TK.INSERT)) + 1.0
    if last_pos > 2.0 and last_pos >= current_pos:
        console_entry.config(state = TK.NORMAL)
        console_entry.insert(last_pos, "\n")
# processing main function
def interpretate(event):
    if len(list_func) == 0:
        console_entry.insert(TK.END, "\nFile was not opened!\n")
        return
    position = float(console_entry.index(TK.END)) - 1.0
    input_value = console_entry.get(position, TK.END).split("\n")[0]
    index = 0
    main_commands = list_func[main_func]
    try: input_choice[input_value](main_commands)
    except KeyError: console_entry.insert(TK.END, "\nError: wrong input\n")

# implementation of the interpretetion
# creating GUI and initialization
#console and it's property
console = TK.Tk()
console.title(console_name)
# console text entry and scrollbars
console_entry = TK.Text(master = console, font = myfont, width = 80, height = 20,
                        bg = "black", fg = "white", wrap = TK.WORD, cursor = "pirate", insertbackground = "white")
console_scroll_horiz = TK.Scrollbar(command = console_entry.xview, orient = TK.HORIZONTAL)
console_scroll_vertic = TK.Scrollbar(command = console_entry.yview, orient = TK.VERTICAL)
console_scroll_horiz.pack(side = TK.BOTTOM, fill = TK.X)
console_entry.pack(side = TK.LEFT, fill = TK.Y)
console_scroll_vertic.pack(side = TK.RIGHT, fill = TK.Y)
console_entry.config(xscrollcommand = console_scroll_horiz.set)
console_entry.config(yscrollcommand = console_scroll_vertic.set)
last_pos = [float(console_entry.index(TK.END))]
console_entry.bind("<Return>", interpretate)
console_entry.bind_all("<Key>", motion)
console_entry.bind("<BackSpace>", return_line)
# menu and open file menu
main_menu = TK.Menu(console)
console.config(menu = main_menu)
file_menu = TK.Menu(main_menu, tearoff = 0)
main_menu.add_cascade(label = "File", command = open_file)
console.mainloop()
