import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import ttk
import tkinter.filedialog
from tkinter.messagebox import showinfo
from pandastable import Table

class Budget:
    """Budgeting software that helps the user anaylze their budget without entering data manually."""

    def __init__(self, dataTable=[]):
        """Initializes software"""

        #assign class variables
        self.dataTable = dataTable[:]
        self.categoriesDict = self.loadCategories()
        self.recBudget = {50 : ['HOUSING', 'TRANSPORT', 'FOOD', 'UTILITIES', 'INSURANCE', 'MEDICAL-HEALTH'], 30 : ['OTHER', 'ENETERTAINMENT', 'SERVICES'], 20 : ['DEBT', 'SAVINGS']}
        self.budgetType = bool
        self.categoryList = []

        self.runtkinter()


    def runtkinter(self):
        root = tk.Tk()

        root.title("Python Budgeting Software - v3.0")

        window_width = 600
        window_height = 400

        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.mainmenu(root)

        root.mainloop()

    def mainmenu(self, root):
        mainmenuframe = tk.Frame(root)
        mainmenuframe.pack(side="top", expand=True, fill="both")
        introMessage = tk.Label(mainmenuframe, text="Welcome to 2023 Budgeting with Python")
        introMessage2 = tk.Label(mainmenuframe, text="Please choose from the options below")
        introMessage.pack()
        introMessage2.pack()

        prevData = ttk.Button(
            mainmenuframe, 
            text="Display Previous Data",
            command=self.runPreviousData
            )
        runbudget = ttk.Button(
            mainmenuframe,
            text="Run Budgeting Software",
            command=lambda: self.runcalc(mainmenuframe)
        )

        prevData.pack(
            ipadx = 5,
            ipady = 5,
            expand = True
        )
        runbudget.pack(
            ipadx = 5,
            ipady = 5,
            expand =  True
        )

    def runcalc(self, calcframe):
        """runs the program once variables are initialized"""

        for widget  in calcframe.winfo_children():
            widget.destroy()

        calcMessage = tk.Label(calcframe, text="Please choose an option to get started.")
        calcMessage.pack()

        recBudget = ttk.Button(
            calcframe,
            text="Use Recomended Budget",
            command=lambda: self.getUserTransactions(calcframe)
        )
        ownBudget = ttk.Button(
            calcframe,
            text="Enter Your Own Budgeting Categories",
            command=lambda: self.setbudgetCategories(calcframe)
        )
        recBudget.pack(
            ipadx = 5,
            ipady = 5,
            expand = True
        )
        ownBudget.pack(
            ipadx = 5,
            ipady = 5,
            expand = True
        )

        #need to select date range somehow.

        #id categories into preset based on description

        #sort categories based on category strings and account name
        #userTransactionsDF = self.sortTransactions(userTransactionsDF)

        #display the user Transactions
        #self.displayTransactions(userTransactionsDF)

        #allow the user to review the information for correctness
        #self.reviewInfo(userTransactionsDF)

        #once the user verifies the information is correct
        #add together categories with the same name

        #determine how on budget the user is with the rec budget
        #or there personal budget

    def setbudgetCategories(self, catframe):
        for widget  in catframe.winfo_children():
            widget.destroy()

        categoryLabel = tk.Label(catframe, text="Please enter a category:")
        categoryLabel.pack(fill="x", expand="True")

        addButton = ttk.Button(
            catframe, 
            text="Add Category", 
            command=lambda: self.addEntry(catframe)
        )
        addButton.pack()

        doneButton = ttk.Button(
            catframe, 
            text="Finish", 
            command=lambda: self.getUserTransactions(catframe)
        )
        doneButton.pack()

    def addEntry(self, catframe):
        #needs to be changed to a dict
        entryFrame = ttk.Frame(catframe)
        entryFrame.pack()

        entryBox = ttk.Entry(entryFrame)
        entryBox.pack()

        self.categoryList.append(entryBox)
        return self.categoryList

    def runPreviousData(self):
        pass

    def reviewInfo(self, userTransactionsDF):

        #have user review information
        print("Please review category information for accuracy.")
        
        answer = input("Is information correct? Enter y for YES and n for NO: ")
        if answer == 'y':
            return userTransactionsDF
        elif answer == 'n':
            userTransactionsDF = self.changeCategory(userTransactionsDF)

            self.displayTransactions(userTransactionsDF)

            userTransactionsDF = self.reviewInfo(userTransactionsDF)
            return userTransactionsDF
        else:
            print("Unrecoginzed input. Please try again.")
            userTransactionsDF = self.reviewInfo(userTransactionsDF)
            return userTransactionsDF
            

    def getUserTransactions(self, calcframe):
        """Prompts the user to enter their file name so it can be uploaded."""

        filepath = tkinter.filedialog.askopenfile(parent=calcframe, mode="rb", title="Choose a File")
        if filepath:
            data = pd.read_csv(filepath)
            userTransactionsDF = pd.DataFrame(data, columns=['Date', 'Original Description', 'Amount', 'Category', 'Account Name'])

        #clean data first -> try to change categories based off of preset dict?
            
        self.displayTransactions(userTransactionsDF, calcframe)

    def loadCategories(self):
        """Creates categories dictionary that assosciates certain description strings to that category for easy identification"""
        categoriesDict = {
            "HOUSING" : [],
            "TRANSPORT" : ['shell', 'chevron', 'maverik', 'les schwab', '7-eleven'],
            "FOOD" : ['qdoba', 'saladworks', "auntie anne's", "wetzel's", 'five guys', 'costa vida', 'uber eats', 'jack in the box', 'jamba juice', 'einstein bagels', 'doordash', 'grubhub', 'panda express', 'dunkin', 'keva juice', 'wendy', 'instacart', 'dairy queen', 'subway', 'in n out burger', 'taco bell', 'dutch bros', 'raising canes', 'mcdonalds', 'trader joes','kroger','wholefds', 'safeway', 'albertsons', 'smiths', 'winco', 'save mart', 'wal-mart', 'target', 'food maxx', 'costco', 'grocery outlet', 'raley', 'panera bread', 'pizza hut'],
            "UTILITIES" : ['vzwrlss', 'sprint', 'tmobile', 'nv energy'],
            "INSURANCE" : ['geico', 'hometown health', 'ambetter', 'farmers ins', 'gerber', 'anthem', 'vsp', 'metlife'],
            "MEDICAL-HEALTH" : ['walgreens', 'cvs'],
            "DEBT" : ['discover'],
            "SAVINGS" : ['americanexpress'],
            "OTHER" : ['petco', 'ulta', 'hot topic', 'forever 21', 'sally beauty supply', 'lush', 'chewy', 'bath and body works', 'barnesnoble', "victoria's secret", 'adobe', 'usps', 'amazon', 'amzn', 'dollar tree', 'lowe', 'ross', 'e bay', 'godaddy', 'bed bath &'],
            "INCOME" : [],
            "ENTERTAINMENT" : ['nintendo', 'hbo max', 'netflix', 'amc', 'hulu', 'spotify', 'paramount', 'disney plus', 'sling tv', 'apple', 'peacock', 'roku', 'amazon prime', 'galaxy', 'steam'],
            "SERVICES" : []
        }

        return categoriesDict

    def changeCategory(self, userTransactionsDF):
        """Lets the user change a transaction's category"""

        row = input("Please enter the row number of the item you want to change: ")

        change = input("Enter the name of the category you would like to change to: ")

        userTransactionsDF.iloc[int(row), 3]= change

        return userTransactionsDF

    def displayTransactions(self, userTransactionsDF, transactionFrame):
        """Displays the transaction list to the user so they can review it to see if the information looks correct"""

        for widget  in transactionFrame.winfo_children():
            widget.destroy()

        pt = Table(transactionFrame, dataframe=userTransactionsDF)
        pt.show()

    def sortTransactions(self, userTransactionsDF):
        """identifies transaction category based on description"""
        userTransactionsDF = userTransactionsDF.sort_values(by=["Account Name", "Category"])

        return userTransactionsDF

#main program
Budget()