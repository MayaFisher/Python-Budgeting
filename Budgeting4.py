import pandas as pd
import numpy as np
import datetime
from datetime import date
import re 

def runcalc(filepath):
    """Runs the budgeting software"""

    #get the user file
    userTransactionsDF = getUserTransactions(filepath)

    #get specifict date range in data frame
    userTransactionsDF = pickdates(userTransactionsDF)

    return userTransactionsDF

def getUserTransactions(filepath):
    data = pd.read_csv(filepath, low_memory=False)
    userTransactionsDF = pd.DataFrame(data, columns=['Date', 'Original Description', 'Amount', 'Category', 'Account Name'])

    return userTransactionsDF

def addCategories(userTransactionsDF, usePredefinedCategories, userCategory, userValues):
    recBudget = {50 : ['HOUSING', 'TRANSPORT', 'FOOD', 'UTILITIES', 'INSURANCE', 'MEDICAL-HEALTH'], 30 : ['OTHER', 'ENETERTAINMENT', 'SERVICES'], 20 : ['DEBT', 'SAVINGS']}

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

    
def pickdates(userTransactionsDF):
    #Ensure the 'Date' column is in datetime format
    userTransactionsDF['Date'] = pd.to_datetime(userTransactionsDF['Date'])

    #Get today's date
    today = pd.to_datetime('today')

    #Get date of 30 days prior
    thirtyDays = today - pd.Timedelta(30, unit="D")

    #Only select dates between today and 30 days prior from the data frame
    mask = (userTransactionsDF['Date'] >= thirtyDays) & (userTransactionsDF['Date'] <= today)
    ThirtyDaysDF = userTransactionsDF.loc[mask]

    return ThirtyDaysDF

def idCategories(userTransactionsDF, userCategory, usePredefinedCategories):
    #consider renaming "budgetType" to "usePredefinedCategories"
    if usePredefinedCategories:
        categoriesDict = loadCategories()
    else:
        categoriesDict = userCategory

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

def loadCategories():
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