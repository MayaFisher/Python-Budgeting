import pandas as pd
import numpy as np
import datetime
from datetime import date
import re 

def mainmenu():
    #let the user choose what they want to do
    print("Welcome to 2023 Budgeting with Python")
    print("****************************************")
    print("Please choose from the options below")
    print("1. Display Previous Data")
    print("2. Run Budgeting Software")

    programStart = input("What would you like to do? (Pick by number): ")

    if int(programStart) == 1:
        #still need to build out this function
        runPreviousData()
    elif int(programStart) == 2:
        runCalc()
    else:
        print("Error: unrecognized input")

def runCalc():
    filepath = getfile()

    userTransactionsDF = getUserTransactions(filepath)

    thirtyDaysTransactionsDF = pickdates(userTransactionsDF)

    categoriesDict = loadCategories()
    categoriesDict = addToCategoryDict(categoriesDict)

    categoryTotals = getBudgetTotals(categoriesDict)

    sorted30DayDF = idCategories(thirtyDaysTransactionsDF, categoriesDict)

    finalDF = displayTransactions(sorted30DayDF)

    chart_Data = addCategories(finalDF, usePredefinedCategories=True, userCategory, categoryTotals)

    #return thirtyDaysTransactionsDF

def getfile():
    filepath = input("Enter the path and name of the file (Ex: stored/filename.csv)")

    try:
        data = pd.read_csv(filepath)
    except FileNotFoundError:
        print("File not found!")

    return filepath

def getUserTransactions(filepath):
    data = pd.read_csv(filepath, low_memory=False)
    userTransactionsDF = pd.DataFrame(data, columns=['Date', 'Original Description', 'Amount', 'Category', 'Account Name'])

    return userTransactionsDF

def pickdates(userTransactionsDF):
    #Ensure the 'Date' column is in datetime format
    userTransactionsDF['Date'] = pd.to_datetime(userTransactionsDF['Date'])

    #Get today's date
    today = pd.to_datetime('today')

    #Get date of 30 days prior
    thirtyDays = today - pd.Timedelta(30, unit="D")

    #Only select dates between today and 30 days prior from the data frame
    mask = (userTransactionsDF['Date'] >= thirtyDays) & (userTransactionsDF['Date'] <= today)
    thirtyDaysTransactionsDF = userTransactionsDF.loc[mask]

    return thirtyDaysTransactionsDF

def loadCategories():
    """Creates categories dictionary that assosciates certain description strings to that category for easy identification"""
    categoriesDict = {
        "HOUSING" : [],
        "TRANSPORT" : ['shell', 'chevron', 'maverik', 'les schwab', '7-eleven', 'vioc'],
        "FOOD" : ['deli', 'trader', 'grocery', 'nekter', 'mcdonald', 'qdoba', 'saladworks', "auntie anne's", "wetzel's", 'five guys', 'costa vida', 'uber eats', 'jack in the box', 'jamba juice', 'einstein bagels', 'doordash', 'grubhub', 'panda express', 'dunkin', 'keva juice', 'wendy', 'instacart', 'dairy queen', 'subway', 'in n out burger', 'taco bell', 'dutch bros', 'raising canes', 'mcdonalds', 'trader joes','kroger','wholefds', 'safeway', 'albertsons', 'smiths', 'winco', 'save mart', 'wal-mart', 'target', 'food maxx', 'costco', 'grocery outlet', 'raley', 'panera bread', 'pizza hut'],
        "UTILITIES" : ['vzwrlss', 'sprint', 'tmobile', 'nv energy'],
        "INSURANCE" : ['geico', 'hometown health', 'ambetter', 'farmers ins', 'gerber', 'anthem', 'vsp', 'metlife'],
        "MEDICAL-HEALTH" : ['walgreens', 'cvs', 'tracy'],
        "DEBT" : ['discover'],
        "SAVINGS" : ['americanexpress', 'internet transfer'],
        "OTHER" : ['petco', 'ulta', 'hot topic', 'forever 21', 'sally beauty supply', 'lush', 'chewy', 'bath and body works', 'barnesnoble', "victoria's secret", 'adobe', 'usps', 'amazon', 'amzn', 'dollar tree', 'lowe', 'ross', 'e bay', 'godaddy', 'bed bath &'],
        "INCOME" : ['assist-2-sell'],
        "ENTERTAINMENT" : ['nintendo', 'hbo max', 'netflix', 'amc', 'hulu', 'spotify', 'paramount', 'disney plus', 'sling tv', 'apple', 'peacock', 'roku', 'amazon prime', 'galaxy', 'steam'],
        "SERVICES" : []
    }

    return categoriesDict

def addToCategoryDict(categoriesDict):
    print("The current dictionary is: ")
    print(categoriesDict)

    while True:
        key = input("Enter the category you would like to add to (press q to quit): ")
        if key == 'q':
            break
        elif key in categoriesDict.keys():
            value = input("Enter the transaction description you would like to add to the category: ")
            for k, v in categoriesDict.items():
                if k == key:
                    if value in v:
                        print("this transaction description already exists")
                        break
                    else:
                        v.append(value)

    print("The updated Dictionary is: ")
    print(categoriesDict)

    return categoriesDict

def getBudgetTotals(categoriesDict):
    keys = categoriesDict.keys()
    categoryTotals = dict

    for i in keys:
        val = input("Please enter the total you would like to set for spending for category " + i + ": ")
        val = int(val)
        categoryTotals[i] = val

    return categoryTotals

def idCategories(userTransactionsDF, categoriesDict):
    #consider renaming "budgetType" to "usePredefinedCategories"
    #if usePredefinedCategories:
       #categoriesDict = loadCategories()
    #else:
        #ategoriesDict = userCategory

    # Convert "Original Description" column to strings
    userTransactionsDF["Original Description"] = userTransactionsDF["Original Description"].astype(str)

    #Ensure lower case for reliable matching
    userTransactionsDF["Original Description"] = userTransactionsDF["Original Description"].str.lower()
    categoriesDict = {k.lower(): [item.lower() for item in v] for k, v in categoriesDict.items()}

    def find_category(description):
        for category, keywords in categoriesDict.items():
            for keyword in keywords:
                if keyword in description:
                    return category
        return None #Return None or a default category if no match is found

    userTransactionsDF["Matched Category"] = userTransactionsDF["Original Description"].apply(find_category)

    return userTransactionsDF

def displayTransactions(transactionsDF):
    with pd.option_context('display.max_rows', None, 'display.precision', 3):
        print(transactionsDF)

    update = input("Does any category in the dataframe need to be updated (y = yes, n = no): ")
    if update == 'y':
        transactionsDF = changeCategory(transactionsDF)
        return transactionsDF
    elif update == 'n':
        return transactionsDF

def changeCategory(transactionsDF):
    row = input("Enter the row number of the item you want to change: ")
    change = input ("Enter the category you would like to change to: ")

    transactionsDF.iloc[int(row), 3] = change

    update = input("Does any category in the dataframe need to be updated (y = yes, n = no): ")
    if update == 'y':
        transactionsDF = changeCategory(transactionsDF)
        return transactionsDF
    elif update == 'n':
        return transactionsDF

def addCategories(userTransactionsDF, usePredefinedCategories, userCategory, userValues):
   #recBudget = {50 : ['HOUSING', 'TRANSPORT', 'FOOD', 'UTILITIES', 'INSURANCE', 'MEDICAL-HEALTH'], 30 : ['OTHER', 'ENETERTAINMENT', 'SERVICES'], 20 : ['DEBT', 'SAVINGS']}

    if usePredefinedCategories:
        #Process predefined categories
        categoriesDict = loadCategories()
        budgetDict = recBudget
    else:
        #Process user-defined categories
        categoriesDict = userCategory
        budgetDict = userValues

    category_totals = {}
    budget_totals = {}

    for _, row in userTransactionsDF.iterrows():
        category = row["Matched Category"]
        amount = row["Amount"]

        if category not in category_totals:
            category_totals[category] =  0

        category_totals[category] += amount

    #Calculate the actual amount spent as a percentage of the budget
    for percentage, categories in budgetDict.items():
        budget_totals[percentage] = sum(category_totals.get(category, 0) for category in categories)

    chart_data = []

    #Save the actual amount spent and target percentage
    for percentage, total_spent in budget_totals.items():
        target_percentage = percentage
        actual_percentage = (total_spent / target_percentage) * 100

        chart_data.append((target_percentage, actual_percentage))

    return chart_data





    