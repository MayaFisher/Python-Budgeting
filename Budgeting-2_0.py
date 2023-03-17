import pandas as pd
import numpy as np

class Budget:
    """Budgeting software that helps the user anaylze their budget without entering data manually."""

    def __init__(self, dataTable=[]):
        """Initializes software"""

        #assign class variables
        self.dataTable = dataTable[:]
        self.categoriesDict = self.loadCategories()
        self.recBudget = {50 : ['HOUSING', 'TRANSPORT', 'FOOD', 'UTILITIES', 'INSURANCE', 'MEDICAL-HEALTH'], 30 : ['OTHER', 'ENETERTAINMENT', 'SERVICES'], 20 : ['DEBT', 'SAVINGS']}

        #let the user choose what they want to do
        #options are save their own categories
        #run calculation program
        #display previous data

        #run the calculation program
        self.runcalc()

    def runcalc(self):
        """runs the program once variables are initialized"""
        #get the user file
        userTransactionsDF = self.getUserTransactions()

        #id categories into preset based on description

        #sort categories based on category strings and account name
        userTransactionsDF = self.sortTransactions(userTransactionsDF)

        #display the user Transactions
        self.displayTransactions(userTransactionsDF)

        #allow the user to review the information for correctness
        self.reviewInfo(userTransactionsDF)

        #once the user verifies the information is correct
        #add together categories with the same name

        #determine how on budget the user is with the rec budget
        #or there personal budget

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
            

    def getUserTransactions(self):
        """Prompts the user to enter their file name so it can be uploaded."""

        filepath = input("Enter the path and name of the file (Ex: stored/filename.csv) ")

        try:
            data = pd.read_csv(filepath)
            userTransactionsDF = pd.DataFrame(data, columns=['Date', 'Original Description', 'Amount', 'Category', 'Account Name'])
        except FileNotFoundError:
            print("File not found!")

        return userTransactionsDF

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

    def displayTransactions(self, userTransactionsDF):
        """Displays the transaction list to the user so they can review it to see if the information looks correct"""

        with pd.option_context('display.max_rows', None,
                               'display.precision', 3,):
            print(userTransactionsDF)

    def sortTransactions(self, userTransactionsDF):
        """identifies transaction category based on description"""
        userTransactionsDF = userTransactionsDF.sort_values(by=["Account Name", "Category"])

        return userTransactionsDF

#main program
Budget()