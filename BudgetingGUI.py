import Budgeting4
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import tkinter.simpledialog
from tkinter import *
from tkinter import ttk
import turtle
from pandastable import Table
import ast
import datetime
import os


class BudgetGUI:

    def __init__(self, root):
        self.root = root
        self.userCategory = {}
        self.userValues = {}

        self.windowCreate()

    def windowCreate(self):
        self.root.title("Python Budgeting Software - v4.0")

        window_width = 600
        window_height = 400

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        center_x = int(screen_width / 2 - window_width / 2)
        center_y = int(screen_height / 2 - window_height / 2)

        self.root.geometry(f'{window_width}x{window_height}+{center_x}+{center_y}')

        self.mainmenu()

        self.root.mainloop()

    def mainmenu(self):
        mainmenuframe = tkinter.Frame(self.root)
        mainmenuframe.pack(side="top", expand=True, fill="both")

        introMessage = tkinter.Label(mainmenuframe, text="Welcome to 2023 Budgeting with Python")
        introMessage2 = tkinter.Label(mainmenuframe, text="Please choose from the options below")
        introMessage.pack()
        introMessage2.pack()

        prevData = ttk.Button(
            mainmenuframe, 
            text="Display Previous Data",
            command=lambda: Budgeting4.runPreviousData()
            )
        runbudget = ttk.Button(
            mainmenuframe,
            text="Run Budgeting Software",
            command=lambda: self.setBudgetType(mainmenuframe)
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

    def setBudgetType(self, frame):
        for widget  in frame.winfo_children():
            widget.destroy()

        calcMessage = tkinter.Label(frame, text="Please choose an option to get started.")
        calcMessage.pack()

        recBudget = ttk.Button(
            frame,
            text="Use Recommended Budget",
            command=lambda: self.recBudgetRun(frame, usePredefinedCategories=True)
        )
        ownBudget = ttk.Button(
            frame,
            text="Enter Your Own Budgeting Categories",
            command=lambda: self.setBudgetCategories(frame)
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

    def recBudgetRun(self, frame, usePredefinedCategories):
        filepath = self.browseFiles(frame)
        if filepath is not None:
            userTransactionsDF = Budgeting4.runcalc(filepath.name)
            userTransactionsDF = Budgeting4.idCategories(userTransactionsDF,self.userCategory, usePredefinedCategories)
            self.displayAndReview(frame, userTransactionsDF, usePredefinedCategories)
        

    def userBudgetRun(self, frame, usePredefinedCategories):
        filepath = self.browseFiles(frame)
        if filepath is not None:
            userTransactionsDF = Budgeting4.runcalc(filepath.name)
            userTransactionsDF = Budgeting4.idCategories(userTransactionsDF, self.userCategory, usePredefinedCategories)
            self.displayAndReview(frame, userTransactionsDF, usePredefinedCategories)

    def browseFiles(self, frame):
        filepath = tkinter.filedialog.askopenfile(parent=frame, mode="rb", title="Choose a File")
        if filepath:
            return filepath

    def setUserValues(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        valueLabel = tkinter.Label(frame, text="Please enter the percentage of your budget:")
        valueLabel.pack(fill="x", expand="True")

        addButton = ttk.Button(
            frame,
            text="Add Value",
            command=lambda: self.addValue(frame)
        )
        addButton.pack()

        doneButton = ttk.Button(
            frame,
            text="Finish",
            command=lambda: self.userBudgetRun(frame, usePredefinedCategories=False)
        )
        doneButton.pack()

    def addValue(self, frame):
        value = ttk.Entry(frame)
        value.pack()

        categoryLabel = tkinter.Label(frame, text="Please enter the categories (as a list) that will total to this percentage of your budget:")
        categoryLabel.pack()

        category = ttk.Entry(frame)
        category.pack()

        value = value.get()
        category = category.get()

        addButton = ttk.Button(
            frame,
            text="Add Percentage",
            command=lambda: self.updateUserValues(value.get(), category.get())
        )
        addButton.pack()

    def updateUserValues(self, value, category):
        try:
            categoryList = ast.literal_eval(category) #convert string to list
            if isinstance(categoryList, list) and value not in self.userValues.keys():
                self.userValues[value] = categoryList
            else:
                tkinter.messagebox.showerror("Error", "Please provide a valid list of examples and a unique category.")
        except (ValueError, SyntaxError):
            tkinter.messagebox.showerror("Error", "Invalid format for examples. Please enter a list (e.g., ['example1', 'example2', 'example3']).")

    def setBudgetCategories(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

        categoryLabel = tkinter.Label(frame, text="Please enter a category:")
        categoryLabel.pack(fill="x", expand="True")

        addButton = ttk.Button(
            frame, 
            text="Add Category", 
            command=lambda: self.addCategory(frame)
        )
        addButton.pack()

        doneButton = ttk.Button(
            frame, 
            text="Finish", 
            command=lambda: self.setUserValues(frame)
        )
        doneButton.pack()

    def addCategory(self, frame):
        category = ttk.Entry(frame)
        category.pack()

        exampleLabel = tkinter.Label(frame, text="Please enter examples (as a list) for the category:")
        exampleLabel.pack()

        example = ttk.Entry(frame)
        example.pack()

        category = category.get()
        example = example.get()

        addButton = ttk.Button(
           frame,
           text="Add Category",
           command=lambda: self.updateUserCategory(category.get(), example.get())
        )
        addButton.pack()

    def updateUserCategory(self, category, example):
        try:
            exampleList = ast.literal_eval(example) #convert string to list
            if isinstance(exampleList, list) and category not in self.userCategory.keys():
                self.userCategory[category] = exampleList
            else:
                tkinter.messagebox.showerror("Error", "Please provide a valid list of examples and a unique category.")
        except (ValueError, SyntaxError):
            tkinter.messagebox.showerror("Error", "Invalid format for examples. Please enter a list (e.g., ['example1', 'example2', 'example3']).")

    def displayAndReview(self, frame, userTransactionsDF, usePredefinedCategories):
        for widget in frame.winfo_children():
            widget.destroy()

        pt = Table(frame, dataframe=userTransactionsDF, showtoolbar=True)
        pt.show()

        finishButton = ttk.Button(
            frame,
            text = "Finish",
            command=lambda: self.finishButtonClicked(frame, userTransactionsDF, usePredefinedCategories)
        )
        finishButton.pack()

    def finishButtonClicked(self, frame, userTransactionsDF, usePredefinedCategories):
        chart_data = Budgeting4.addCategories(userTransactionsDF, usePredefinedCategories, self.userCategory, self.userValues)

        self.finalInfo(frame, chart_data, userTransactionsDF)

    def finalInfo(self, frame, chart_data, userTransactionsDF):
        for widget in frame.winfo_children():
            widget.destroy()

        #Create a turtle screen
        screen = turtle.Screen()
        screen.setup(width=800, height = 600)
        screen.title("Budget Chart")

        #Set up turtle chart parameters
        chart_width = 400
        chart_height = 300
        chart_origin_x = -chart_width / 2
        chart_origin_y = -chart_height / 2

        #Calculate the bar width and spacing
        bar_width = chart_width / (len(chart_data) * 2)
        bar_spacing = bar_width

        #Find the maximum actual percentage for scaling
        max_actual_percentage = max(data[1] for data in chart_data)

        #Create a turtl for drawing the chart
        chart_turtle = turtle.Turtle()
        chart_turtle.penup()
        chart_turtle.goto(chart_origin_x, chart_origin_y)
        chart_turtle.pendown()

        #Draw the bars
        for target_percentage, actual_percentage in chart_data:
            #Calculate the bar height
            bar_height = (actual_percentage / max_actual_percentage) * chart_height

            #Draw the bar
            chart_turtle.left(90)
            chart_turtle.forward(bar_height)
            chart_turtle.right(90)
            chart_turtle.forward(bar_width)
            chart_turtle.right(90)
            chart_turtle.forward(bar_height)
            chart_turtle.left(90)

        #Hide the turtle and exit on click
        chart_turtle.hideturtle()
        screen.exitonclick()

        #Save the data and chart
        self.saveDataAndChart(userTransactionsDF, chart_data)

    def saveDataAndChart(self, userTransactionsDF, chart_data):
        #Get the current data and time
        current_datetime = datetime.datetime.now()

        #Create a folder for saving the data and charts if it doesn't exist
        folder_name = "BudgetingData"
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)

        #Save the data as a CSV file
        data_filename = f"{folder_name}/budget_data_{current_datetime.strftime('%Y%m%d_%H%M%S')}.csv"
        userTransactionsDF.to_csv(data_filename, index=False)

        # Save the chart as an image file
        chart_filename = f"{folder_name}/budget_chart_{current_datetime.strftime('%Y%m%d_%H%M%S')}.png"
        turtle.getscreen().getcanvas().postscript(file=chart_filename)
        
        # Show a message box to notify the user
        tkinter.messagebox.showinfo("Save Successful", f"Data and chart saved.\nData File: {data_filename}\nChart File: {chart_filename}")

root = tkinter.Tk()
BudgetGUI(root)
