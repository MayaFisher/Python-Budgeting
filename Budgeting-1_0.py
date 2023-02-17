

class Budget:
    """
    Budgeting software that helps the user to decide
    where would be best to put any excess income.
    """

    def __init__(self, dataTable=[]):
        """Initializes software"""

        #assign class variables
        self.dataTable = dataTable[:]

        #get the user input
        self.getUserTransactions()

        #sort the input by category and return dict of totals
        categoryTotal = self.categorySort()

        #display totals for each category
        self.displayTotals()

    def getUserTransactions(self):
        """Prompts the user for thier transaction information"""

        isdone = 'n'

        while(isdone != 'y'):

            #get Description - what was the purchase for
            description = input("Enter category descripton: ")

            #get category - how would this be categorized
            #make sure to give the user preset options to start
            #have these be Housing, Insurance, Food, Gas, Service Bills, Debt, Savings, Health, Other, and Income
            possibleCategories = ["HOUSING", "INSURANCE", "FOOD", "GAS", "SERVICE BILLS", "DEBT", "SAVINGS", "HEALTH", "OTHER", "INCOME"]
            print("Enter transaction category - You may choose from HOUSING, INSURANCE, FOOD, GAS, SERVICE BILLS, DEBT, SAVINGS, HEALTH, OTHER, and INCOME")

            endloop = True

            while(endloop):
                category = input("Enter transaction category: ")
                
                if not any(category in x for x in possibleCategories):
                    #raise Exception("Category input is not part of possible catgories. Try again.")
                    pass
                else:
                    endloop = False

            #get the total of the transaction
            total = input("Enter transaction total: ")

            #get whether it was incoming or outgoing
            transactionType = input("Enter if tranaction was INCOMING or OUTGOING: ")

            #add input information to list transaction
            transaction = [description, category, total, transactionType]

            #store as list in dataTable -  as the program runs dataTable gets larger until the user is done entering transactions.
            #call method to store in dataTable. dataTable should only be accessed by this method
            self.addTo_dataTable(transaction)

            #ask if user is done inputing transactions
            print("Are you finished entering transaction information?")
            isdone = input("Enter 'y' for YES and 'n' for NO. ")

            self.categorySort()
            

    def addTo_dataTable(self, transaction):
        """
        Adds the transaction (which is a list) to the data table.
        This will then create a list of lists or an array or sorts 
        to represent the data table.
        """
        self.dataTable.append(transaction)

    def categorySort(self):
        """
        Sorts transactions by category.
        """
        transCopy = self.dataTable[:]

        sortedTrans = sorted(transCopy, key = lambda x : x[1])

        transHousing = []
        transInsurance = []
        transFood = []
        transGas = []
        transServices = []
        transDebt = []
        transSavings = []
        transHealth = []
        transOther = []
        transIncome = []

        for trans in sortedTrans:
            if trans[1].lower() == "housing":
                transHousing.append(trans)
            elif trans[1].lower() == "insurance":
                transInsurance.append(trans)
            elif trans[1].lower() == 'food':
                transFood.append(trans)
            elif trans[1].lower() == 'gas':
                transGas.append(trans)
            elif trans[1].lower() == 'service bills':
                transServices.append(trans)
            elif trans[1].lower() == 'debt':
                transDebt.append(trans)
            elif trans[1].lower() == 'savings':
                transSavings.append(trans)
            elif trans[1].lower() == 'health':
                transHealth.append(trans)
            elif trans[1].lower() == 'other':
                transOther.append(trans)
            elif trans[1].lower() == 'income':
                transIncome.append(trans)

        
            

    def categoryAdd(self):
        """
        Adds identical categories together to produce a total for that category.
        """

        pass

    def displayTotals(self):
        """
        Displays the totals of each category to the user.
        """

        #for trans in self.dataTable:
            #print(trans)

        

#main program
Budget()
