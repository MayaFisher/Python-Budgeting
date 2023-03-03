import pandas as pd

class Budget:
    """Budgeting software that helps the user anaylze their budget without entering data manually."""

    def __init__(self, dataTable=[]):
        """Initializes software"""

        #assign class variables
        self.dataTable = dataTable[:]
        self.categoriesDict = self.loadCategories()

        #run the program
        self.run()

    def run(self):
        """runs the program once variables are initialized"""
        #get the user file
        self.getUserTransactions()

    def getUserTransactions(self):
        """Prompts the user to enter their file name so it can be uploaded."""

        filepath = input("Enter the path and name of the file (Ex: stored/filename.csv) ")

        try:
            data = pd.read_csv(filepath)
            userTransactionsDF = pd.DataFrame(data, columns=['Date', 'Original Description', 'Amount', 'Category', 'Account Name'])
        except FileNotFoundError:
            print("File not found!")

        print(userTransactionsDF)

    def loadCategories(self):

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

#class Budget:
    #"""
    #Budgeting software that helps the user to decide
    #where would be best to put any excess income.
    #"""

    #def __init__(self, dataTable=[]):
        #"""Initializes software"""

        #assign class variables
        #self.dataTable = dataTable[:]

        #get the user input
        #self.getUserTransactions()

        #sort the input by category
        #categoryTotal = self.categorySort()

    #def getUserTransactions(self):
        #"""Prompts the user for thier transaction information"""

        #isdone = 'n'

        #while(isdone != 'y'):

            #get Description - what was the purchase for
            #description = input("Enter category descripton: ")

            #get category - how would this be categorized
            #make sure to give the user preset options to start
            #have these be Housing, Insurance, Food, Gas, Service Bills, Debt, Savings, Health, Other, and Income
            #possibleCategories = ["HOUSING", "INSURANCE", "FOOD", "GAS", "SERVICE BILLS", "DEBT", "SAVINGS", "HEALTH", "OTHER", "INCOME"]
            #print("Enter transaction category - You may choose from HOUSING, INSURANCE, FOOD, GAS, SERVICE BILLS, DEBT, SAVINGS, HEALTH, OTHER, and INCOME")

            #endloop = True

            #while(endloop):
                #category = input("Enter transaction category: ")
                
                #if not any(category in x for x in possibleCategories):
                    #raise Exception("Category input is not part of possible catgories. Try again.")
                    #pass
                #else:
                    #endloop = False

            #get the total of the transaction
            #total = input("Enter transaction total: ")

            #get whether it was incoming or outgoing
            #transactionType = input("Enter if tranaction was INCOMING or OUTGOING: ")

            #add input information to list transaction
            #transaction = [description, category, total, transactionType]

            #store as list in dataTable -  as the program runs dataTable gets larger until the user is done entering transactions.
            #call method to store in dataTable. dataTable should only be accessed by this method
            #self.addTo_dataTable(transaction)

            #ask if user is done inputing transactions
            #print("Are you finished entering transaction information?")
            #isdone = input("Enter 'y' for YES and 'n' for NO. ")

        #sortedTrans = []
        #sortedTrans = self.categorySort()

        #self.categoryAdd(sortedTrans)
            

    #def addTo_dataTable(self, transaction):
        #"""
        #Adds the transaction (which is a list) to the data table.
        #This will then create a list of lists or an array or sorts 
        #to represent the data table.
        #"""
        #self.dataTable.append(transaction)

    #def categorySort(self):
        #"""
        #Sorts transactions by category.
        #"""
        #transCopy = self.dataTable[:]

        #sortedTrans = sorted(transCopy, key = lambda x : x[1])

        #return sortedTrans

    #def categoryAdd(self, sortedTrans):
        #"""
        #Adds identical categories together to produce a total for that category.
        #"""
        #housingTotal = 0
        #insuranceTotal = 0
        #foodTotal = 0
        #gasTotal = 0
        #servicesTotal = 0
        #debtTotal = 0
        #savingsTotal = 0
        #healthTotal = 0
        #otherTotal = 0
        #incomeTotal = 0

        #for trans in sortedTrans:
            #if trans[1].lower() == "housing":
                #add together transaction totals
                #housingTotal += float(trans[2])
            #elif trans[1].lower() == "insurance":
                #add together transaction totals
                #insuranceTotal += float(trans[2])
            #elif trans[1].lower() == 'food':
                #add together transaction totals
                #foodTotal += float(trans[2])
            #elif trans[1].lower() == 'gas':
                #add together transaction totals
                #gasTotal += float(trans[2])
            #elif trans[1].lower() == 'service bills':
                #add together transaction totals
                #servicesTotal += float(trans[2])
            #elif trans[1].lower() == 'debt':
                #add together transaction totals
                #debtTotal += float(trans[2])
            #elif trans[1].lower() == 'savings':
                #add together transaction totals
                #savingsTotal += float(trans[2])
            #elif trans[1].lower() == 'health':
                #add together transaction totals
                #healthTotal += float(trans[2])
            #elif trans[1].lower() == 'other':
                #add together transaction totals
                #otherTotal += float(trans[2])
            #elif trans[1].lower() == 'income':
                #add together transaction totals
                #incomeTotal += float(trans[2])

        #totalDict = {
            #"HOUSING" : housingTotal,
            #"INSURANCE" : insuranceTotal,
            #"FOOD" : foodTotal,
            #"GAS" : gasTotal,
            #"SERVICE BILLS" : servicesTotal,
            #"DEBT" : debtTotal,
            #"SAVINGS" : savingsTotal,
            #"HEALTH" : healthTotal,
            #"OTHER" : otherTotal,
            #"INCOME" : incomeTotal
        #}

        #self.displayTotals(totalDict)

    #def displayTotals(self, totalDict):
        #"""
        #Displays the totals of each category to the user.
        #"""

        #for key, val in totalDict.items():
            #print(key, "-", val)

#main program
Budget()