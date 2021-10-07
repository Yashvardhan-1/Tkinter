from tkinter import *
from tkinter import ttk, messagebox
from tkinter.constants import BOTH, RIGHT, TOP
from tkinter.ttk import Notebook, Progressbar
from tkcalendar import DateEntry
import datetime

import numpy as np
import pandas as pd
import sqlite3  as db
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


#backend functions

def init():
    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    create table if not exists expenses (
        date string,
        title string,
        expense number
        );
    '''
    curr.execute(query)
    connectionObjn.commit()

def submitexpense():
    values=[E_Date.get(),Title.get(),Expense.get()]
    print(values)
    F1_TV.insert('', 'end', values=values)

    connectionObjn = db.connect("expenseTracker.db")
    curr = connectionObjn.cursor()
    query = '''
    INSERT INTO expenses VALUES 
    (?, ?, ?)
    '''
    curr.execute(query,(E_Date.get(),Title.get(),Expense.get()))
    connectionObjn.commit()

    arr = pd.read_sql_query("Select * from expenses", connectionObjn)
    totalExpense = 0
    for item in arr['expense']:
        totalExpense += item
    progBar['value'] = (totalExpense/maxlimit)*100
    Prog_Label.config(text=str(progBar['value'])+'%')

def viewplot():
    connectionObjn = db.connect("expenseTracker.db")
    arr = pd.read_sql_query("Select * from expenses", connectionObjn)
    figure1 = plt.Figure(figsize=(6,4), dpi=100)
    ax1 = figure1.add_subplot(111)
    bar1 = FigureCanvasTkAgg(figure1, F2)
    bar1.get_tk_widget().grid(row=1, column=0)
    arr = arr[['date','title', 'expense']].groupby('date').sum()
    arr.plot(kind='line',color='r', legend=True, ax=ax1, marker='o')
    ax1.set_title('Date VS Expense')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Expenses')

def setmaxlimit(val):
    maxlimit = int(val)
    connectionObjn = db.connect("expenseTracker.db")
    arr = pd.read_sql_query("Select * from expenses", connectionObjn)
    totalExpense = 0
    for item in arr['expense']:
        totalExpense += item
    progBar['value'] = int((totalExpense/maxlimit)*100)
    Prog_Label.config(text=str(progBar['value'])+'%')

def btn_click(item):
    global expression
    expression = expression + str(item)
    input_text.set(expression)

def btn_clear(): 
    global expression 
    expression = "" 
    input_text.set("")
 
def btn_equal():
    global expression
    result = str(eval(expression)) #'eval' evaluates the string expression directly
    input_text.set(result)
    expression = result


#frontend / GUI

init()
GUI = Tk()
GUI.title('Expense Tracker')
GUI.resizable(0, 0)


Tab = Notebook(GUI)
F1 = Frame(Tab, width=450, height=500)
F2 = Frame(Tab, width=450, height=500)
F3 = Frame(Tab, width=450, height=500, highlightbackground="black", highlightcolor="black", highlightthickness=2)

Tab.add(F1, text = 'Add Expense')
Tab.add(F2, text = 'Graph')
Tab.add(F3, text = 'Calculator')

Tab.pack(fill=BOTH, expand=1)

#Tab1

#Row0------------------------------------------------
L_Date = ttk.Label(F1, text='Date', font=(None, 18))
L_Date.grid(row=0, column=0, padx=30, pady=5, sticky='w')

#Date Picker
E_Date = DateEntry(F1, width=19, background='purple', foreground='white', font=(None, 18))
E_Date.grid(row=0, column=1, padx=5, pady=5, sticky='w')

#Row1------------------------------------------------
L_Title = ttk.Label(F1, text='Title', font=(None, 18))
L_Title.grid(row=1, column=0, padx=30, pady=5, sticky='w')

Title = StringVar()

E_Title = ttk.Entry(F1, textvariable=Title, font=(None, 18))
E_Title.grid(row=1, column=1, padx=5, pady=5, sticky='w')

#Row2------------------------------------------------
L_Expense = ttk.Label(F1, text='Expense', font=(None, 18))
L_Expense.grid(row=2, column=0, padx=30, pady=5, sticky='w')

Expense = IntVar()

E_Expense = ttk.Entry(F1, textvariable=Expense, font=(None, 18))
E_Expense.grid(row=2, column=1, padx=5, pady=5, sticky='w')

#Row3------------------------------------------------
F1_Add = ttk.Button(F1, text='Add',command=submitexpense)
F1_Add.grid(row=3, column=1, padx=80, pady=5, sticky='w', ipadx=10, ipady=10)

#Row4------------------------------------------------
#Tree View-------------------------------------------
F1_List = ['Date', 'Title', 'Expense']
F1_TV = ttk.Treeview(F1, columns=F1_List, show='headings', height=5)
for i in F1_List:
    F1_TV.heading(i, text=i.title())
F1_TV.grid(row=4, column=0, padx=5, pady=5, sticky='w', columnspan=3)

#Row5------------------------------------------------
L_Limit = ttk.Label(F1, text='Max Funds', font=(None, 10))
L_Limit.grid(row=5, column=0, padx=50)

#Slider
slider = Scale(F1, from_=1000, to=200000, orient=HORIZONTAL, length=250, command=setmaxlimit)
slider.grid(row=5, column=1, pady=50)

#Row6------------------------------------------------
L_Used = ttk.Label(F1, text='Funds Used', font=(None, 10))
L_Used.grid(row=6, column=0, padx=50)

#Progress Bar
maxlimit = 1000

progBar = ttk.Progressbar(F1, orient=HORIZONTAL, mode='determinate', length=300)
progBar.grid(row=6, column=1, pady=10)
connectionObjn = db.connect("expenseTracker.db")
arr = pd.read_sql_query("Select * from expenses", connectionObjn)
totalExpense = 0
for item in arr['expense']:
    totalExpense += item
progBar['value'] = int((totalExpense/maxlimit)*100)
Prog_Label = Label(F1, text=str(progBar['value'])+'%')
Prog_Label.grid(row=6, column=2, padx=50)


#Tab2
viewplt=Button(F2,command=viewplot,text="View Graph")
viewplt.grid(row=0,column=0,padx=13,pady=13,sticky='w')


#Tab3
#Input Frame
input_frame = Frame(F3, width=450, height=80, bd=0, highlightbackground="black", highlightcolor="black", highlightthickness=2)
input_frame.pack(side=TOP)

expression = ""
input_text = StringVar()

#Input Row
E_Input = Label(input_frame, textvariable=input_text, width=39, bg="#eee", bd=0, font=(None, 18, 'bold'), cursor="none")
E_Input.grid(row=0, column=0, pady=1)
E_Input.pack(ipady=10) #internal padding

#Buttons frame
btn_frame = Frame(F3, width=450, height=420, bg="grey")
btn_frame.pack()

#Row0
clear = Button(btn_frame, text = "C", fg = "black", width = 62, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_clear())
clear.grid(row = 0, column = 0, columnspan = 3, padx = 1, pady = 1)
 
divide = Button(btn_frame, text = "/", fg = "black", width = 20, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("/"))
divide.grid(row = 0, column = 3, padx = 1, pady = 1)
 
#Row1
seven = Button(btn_frame, text = "7", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(7))
seven.grid(row = 1, column = 0, padx = 1, pady = 1)
 
eight = Button(btn_frame, text = "8", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(8))
eight.grid(row = 1, column = 1, padx = 1, pady = 1)
 
nine = Button(btn_frame, text = "9", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(9))
nine.grid(row = 1, column = 2, padx = 1, pady = 1)
 
multiply = Button(btn_frame, text = "*", fg = "black", width = 20, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("*"))
multiply.grid(row = 1, column = 3, padx = 1, pady = 1)
 
#Row2 
four = Button(btn_frame, text = "4", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(4))
four.grid(row = 2, column = 0, padx = 1, pady = 1)
 
five = Button(btn_frame, text = "5", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(5))
five.grid(row = 2, column = 1, padx = 1, pady = 1)
 
six = Button(btn_frame, text = "6", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(6))
six.grid(row = 2, column = 2, padx = 1, pady = 1)
 
minus = Button(btn_frame, text = "-", fg = "black", width = 20, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("-"))
minus.grid(row = 2, column = 3, padx = 1, pady = 1)
 
#Row3
one = Button(btn_frame, text = "1", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(1))
one.grid(row = 3, column = 0, padx = 1, pady = 1)
 
two = Button(btn_frame, text = "2", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(2))
two.grid(row = 3, column = 1, padx = 1, pady = 1)
 
three = Button(btn_frame, text = "3", fg = "black", width = 20, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(3))
three.grid(row = 3, column = 2, padx = 1, pady = 1)
 
plus = Button(btn_frame, text = "+", fg = "black", width = 20, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("+"))
plus.grid(row = 3, column = 3, padx = 1, pady = 1)
 
#Row4
zero = Button(btn_frame, text = "0", fg = "black", width = 41, height = 5, bd = 0, bg = "#fff", cursor = "hand2", command = lambda: btn_click(0))
zero.grid(row = 4, column = 0, columnspan = 2, padx = 1, pady = 1)
 
point = Button(btn_frame, text = ".", fg = "black", width = 20, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_click("."))
point.grid(row = 4, column = 2, padx = 1, pady = 1)

equals = Button(btn_frame, text = "=", fg = "black", width = 20, height = 5, bd = 0, bg = "#eee", cursor = "hand2", command = lambda: btn_equal())
equals.grid(row = 4, column = 3, padx = 1, pady = 1)


GUI.mainloop()
