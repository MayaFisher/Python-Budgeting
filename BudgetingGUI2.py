from urllib.robotparser import RobotFileParser
import Budgeting4
import pandas as pd
import numpy as np
import datetime
from datetime import date
import matplotlib.pyplot as plt
from matplotlib.figure import Figure 
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import tkinter.simpledialog
from tkinter import *
from tkinter.ttk import *
import tkinter.ttk as ttk
from pandastable import Table
import ast
import os

class BudgetGUI:
    
    def __init__(self, root):
        self.root = root 
        self.userCategory = {}
        self.userValues  ={}

        self.windowCreate()

    def windowCreate(self):
        self.root.title("Python Budgeting Software - v4.0")

        window_width = 600
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - screen_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')
        self.root.resizable(True, True)
        # self.root.iconbitmap('')

        self.mainmenu()

        self.root.mainloop()

    def mainmenu(self):
        btnStyle = Style()

        btnStyle.configure('MainMenuBtn', font=('Arial', 10, 'bold', 'underline'), foreground="blue")

        mainmenuframe = tkinter.Frame(self.root)
        mainmenuframe.pack(side="top", expand=True, fill="both")
        
        introMessage = tkinter.Label(mainmenuframe, text="Welcome to 2023 Budgeting with Python")
        introMessage2 = tkinter.Label(mainmenuframe, text="Please choose from the options below")
        introMessage.pack()
        introMessage2.pack()

        prevData = ttk.Button(
            mainmenuframe,
            text="Display Previous Data",
            style='MainMenuBtn',
            command=lambda: self.runPreviousData(mainmenuframe)
            )
        runbudget = ttk.Button(
            mainmenuframe,
            text="Run Budgeting Software",
            style="MainMenuBtn",
            command=lambda: self.setBudgettype(mainmenuframe)
            )

        prevData.grid(row=0, column=3, padx=20)
        prevData.grid(row=0, column=3, padx=20)

        prevData.pack(
            ipadx=5,
            ipady=5,
            expand=True
            )
        runbudget.pack(
            ipadx=5,
            ipady=5,
            expand=True
            )

    def setBudgetType(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        btnStyle = Style()

        btnStyle.configure('BudgetType', font=('Arial', 10, 'bold', 'underline'), foreground="red")

        calcMessage = tkinter.Label(frame, text="Please choose and option to get started.")
        calcMessage.pack()

        recBudget = ttk.Button(
            frame,
            text="Use Recommended Budget",
            style="BudgetType",
            command=lambda: self.recBudgetRun(frame, usePredefinedCategories=True)
            )
        ownBudget = ttk.Button(
            frame,
            text="Enter Your Own Budget",
            style="BudgetType",
            command=lambda: self.setBudgetCategories(frame)
            )

        recBudget.grid(row=1, column=3, padx=20)
        ownBudget.grid(row=1, column=3, padx=20)

        recBudget.pack(
            ipadx=5,
            ipady=5,
            expand=True
            )
        ownBudget.pack(
            ipadx=5,
            ipady=5,
            expand=True
            )

    def recBudgetRun(self, frame, usePredefinedCategories):
        filepath = self.browseFiles(frame)
        if filepath is not None:
            userTransactionsDF = Budgeting5.runcalc(filepath.name)
            userTransactionsDF = Budgeting5.idCategories(userTransactionsDF, self.userCategory, usePredefinedCategories)
            self.displayAndReview(frame, userTransactionsDF, usePredefinedCategories)

    def userBudgetRun(self, frame, usePredefinedCategories):
        filepath = self.browseFiles(frame)
        if filepath is not None:
            userTransactionsDF = Budgeting5.runcalc(filepath.name)
            userTransactionsDF = Budgeting5.idCategories(userTransactionsDF, self.userCategory, usePredefinedCategories)
            self.displayAndReview(frame, userTransactionsDF, usePredefinedCategories)

    def browseFiles(self, frame):
        filepath = tkinter.filedialog.askopenfile(parent=frame, mode="rb", title="Choose a File")
        if filepath:
            return filepath

    def setUserValues(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        valueLabel = tkinter.Label(frame, text="Please enter the percentage of your budget: ")
        valueLabel.pack(fill="x", expand="True")

        #addButton = ttk.Button()

        #doneButton = ttk.Button()

    def addValue(self, frame):
        value = ttk.Entry(frame)
        value.pack()

        categoryLabel = tkinter.Label(frame, text="Please enter the categories (as a list) that will total to this percentage of your budget: ")
        categoryLabel.pack()

        category = ttk.Entry(frame)
        category.pack()

        #addButton = ttk.Button()

    def updateUserValues(self, value, category):
        try:
            categoryList = ast.literal_eva(category) #convert string to list
            if isinstance(categoryList, list) and value not in self.userValues.keys():
                self.userValues[value] = categoryList
            else:
                tkinter.messagebox.showerror("Error")
        except (ValueError, SyntaxError):
            tkinter.messagebox.showerror("Error")

    def setBudgetCategories(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        categoryLabel = tkinter.Label(frame, text="Please enter a category: ")
        categoryLabel.pack(fill="x", expand="True")

        #addButton = ttk.Button()

        #doneButton = ttk.Button()

    def addCategory(self, frame):
        category = ttk.Entry(frame)
        category.pack()

        exampleLabel = tkinter.Label(frame, text="Please enter examples (as a list) for the category: ")
        exampleLabel.pack()

        example = ttk.Entry(frame)
        example.pack()

        category = category.get()
        example = example.get()

        #addButton = ttk.Button()

