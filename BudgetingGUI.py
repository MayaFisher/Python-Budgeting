
import Budgeting4
import pandas as pd
import numpy as np
import datetime
from datetime import date
import re
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter.filedialog
import tkinter.messagebox
import tkinter.font
import tkinter.simpledialog
from tkinter import *
from tkinter import ttk
from pandastable import Table
import ast
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
            command=lambda: self.runPreviousData(mainmenuframe)
            )
        runbudget = ttk.Button(
            mainmenuframe,
            text="Run Budgeting Software",
            command=lambda: self.setBudgetType(mainmenuframe)
        )
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

        #Filter out non-numeric columns
        numeric_columns = userTransactionsDF.select_dtypes(include=[np.number]).columns.tolist()
        numeric_df = userTransactionsDF[numeric_columns]

        if len(numeric_df.columns) == 0:
            tkinter.messagebox.showinfo("No Numeric Data", "No numeric data available for display.")
            return

        pt = Table(frame, dataframe=userTransactionsDF, showtoolbar=True)
        pt.show()

        finishButton = ttk.Button(
            frame,
            text = "Finish",
            command=lambda: self.finishButtonClicked(frame, userTransactionsDF, usePredefinedCategories)
        )
        finishButton.grid()

    def finishButtonClicked(self, frame, userTransactionsDF, usePredefinedCategories):
        chart_data = Budgeting4.addCategories(userTransactionsDF, usePredefinedCategories, self.userCategory, self.userValues)

        self.finalInfo(frame, chart_data, userTransactionsDF)

    def finalInfo(self, frame, chart_data, userTransactionsDF):
        for widget in frame.winfo_children():
            widget.destroy()

        #Create a figure and axis for the bar graph
        fig, ax = plt.subplots(figsize=(8, 6))
        width = 0.35 # Width of the bars

        target_percentages = [data[0] for data in chart_data]
        actual_percentages = [data[1] for data in chart_data]

        # Create bar plots for target and actual percentages
        ax.bar(np.arange(len(target_percentages)), target_percentages, width, label='Target Percentage')
        ax.bar(np.arange(len(actual_percentages)) + width, actual_percentages, width, label='Actual Percentage')

        # Set labels, title, and ticks
        ax.set_ylabel('Percentage')
        ax.set_title('Budgeting Results')
        ax.set_xticks(np.arange(len(target_percentages)) + width / 2)
        ax.set_xticklabels([str(data[0]) for data in chart_data])
        ax.legend()

        # Attach the plot to the Tkinter frame
        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack()

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
        plt.savefig(chart_filename)
        
        # Show a message box to notify the user
        tkinter.messagebox.showinfo("Save Successful", f"Data and chart saved.\nData File: {data_filename}\nChart File: {chart_filename}")

    def runPreviousData(self, frame):

        folder_name = "BudgetingData"
        files = []

        #Check if the folder exists
        if os.path.exists(folder_name):
            #Get all files in the folder
            files = os.listdir(folder_name)

        if not files:
            tkinter.messagebox.showinfo("No Previous Data", "No previous data found.")
            return
        else:
            for widget  in frame.winfo_children():
                widget.destroy()

        #Create a new window to display the previous data
        previousDataWindow = tkinter.Toplevel(self.root)
        previousDataWindow.title("Previous Data")

        #Create a scrollable frame to hold the data
        canvas = tkinter.Canvas(previousDataWindow)
        scrollbar = tkinter.Scrollbar(previousDataWindow, orient="vertical", command=canvas.yview)
        scrollableFrame = tkinter.Frame(canvas)

        scrollableFrame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scrollableFrame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        #Iterate over the files and create labels to display the file names
        for i, filename in enumerate(files):
            fileLabel = tkinter.Label(scrollableFrame, text=f"File {i+1}: {filename}")
            fileLabel.pack()

        #Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        #Add a button to close the window
        closeButton = ttk.Button(previousDataWindow, text="Close", command=previousDataWindow.destroy)
        closeButton.pack()

root = tkinter.Tk()
BudgetGUI(root)
