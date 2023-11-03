#importing necessary libraries
from calendar import month
from operator import contains
from tkinter import LAST

#needed for manipulating data
import pandas as pd
import numpy as np

#need to enable Google Drive API
import gspread

#needed to build dashboard
import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')
from datetime import date


#connect to google drive
gc = gspread.service_account(filename="service_account.json")
sh = gc.open("transactions")

ws = sh.worksheet('transactions')
df = pd.DataFrame(ws.get_all_records()) #import data from csv into dataframe

#clean dataframe
df = df[['Date', 'Description', 'Amount', 'Transaction Type', 'Account Name']]  #keeps only necessary columns
df['Description'] = df["Description"].map(str.lower)                            #change all descriptions to lowercase
df['Transaction Type'] = df['Transaction Type'].map(str.lower)                  #change all transaction types to lowercase
df['Account Name'] = df['Account Name'].map(str.lower)                          #change all account names to lowercase

df['Category'] = 'unassigned'                                                   #add category column and set all data to "unassigned"

#define catgories and change transactions to that category based on description

# Debt Interest
df['Category'] = np.where(df['Description'].str.contains
                          ('interest charges on purchases|interest charge on purchases'), 
                          'Debt Interest', df['Category'])

# Credit Card Payments
df['Category'] = np.where(df['Description'].str.contains
                          ('internet payment - thank you'),
                          'Credit Card Payments', df['Category'])

# Pet Food
df['Category'] = np.where(df['Description'].str.contains
                          ('cat person'),
                          'Pet Food', df['Category'])

# Insurance
df['Category'] = np.where(df['Description'].str.contains
                          ('best life|geico|metlife|anthem blue individual|vsp|farmers ins|hometown health|eqt*hometown health plan|eqt*hometown health'),
                          'Insurance', df['Category'])

# Rent
df['Category'] = np.where((df['Description'].str.contains
                         ('venmo|redfieldridge')) & (df['Amount'] > 300),
                         'Rent', df['Category'])

# Power & Gas
df['Category'] = np.where(df['Description'].str.contains
                          ('nv energy'),
                          'Power & Gas', df['Category'])

# Cellphone
df['Category'] = np.where(df['Description'].str.contains
                          ('vzwrlss'),
                          'Cellphone', df['Category'])

# Pet Items
df['Category'] = np.where(df['Description'].str.contains
                          ('cozy cattery|petco|chewy.com|petsmart|uval care|petco com'),
                          'Pet Items', df['Category'])

# Vet Visits
df['Category'] = np.where(df['Description'].str.contains
                         ('vca animal'),
                         'Vet Visits', df['Category'])

# Groceries
df['Category'] = np.where(df['Description'].str.contains
                          ('safeway|spice rack|costco whse|smiths|sq *prema farm|sq *oliver|winco foods|cvs/pharmacy|walmart sc|instacart|wm supercenter|wal-mart|trader joe|grocery outle|save mart|smiths food|sp sugar love candy|rin tin taps|prema garm|mwintsoph enterprisr|oliver|little fish'),
                          'Groceries', df['Category'])

# Eating Out
df['Category'] = np.where(df['Description'].str.contains
                          ('shell|saladworks|hinoki sushi|death valley coffeeb|beline carniceria|egg roll king|romanos|press start llc|sq *bibo coffee|michaels deli|pho restaurant|chevron|jack in the box|egg roll king|dunkin|baskin|subway|perenn bakery|ricks pizza|william|coca cola|bluefin poke|in n out burger|7-eleven|qdoba|jamba juice|raising canes|mcdonald|costa vida|dutch bros|doordash|nekter juice bar|uber|chevron/fastlane|the urban deli|nekterjuicebar'),
                          'Eating Out', df['Category'])

# Transportation
df['Category'] = np.where(df['Description'].str.contains
                          ('pos wd - costco gas|pos wd dmv-44|sw air dallas|pos wd costco gas|vioc|maverik|frys fuel|smiths-fuel|pos wd  costco gas'),
                          'Transportation', df['Category'])

# Dates
df['Category'] = np.where(df['Description'].str.contains
                          ('pho 777 reno|wild island|century theatres|odysea aquarium|little caesars|west wind drive-ins|galaxy theatre legends'),
                          'Dates', df['Category'])

# Other
df['Category'] = np.where(df['Description'].str.contains
                          ('now withdrawal  zelle|sally beauty|stich fix|amazon|south 40 reno|death valley natural|ulta|sp laracago|seatgeek|costco com|barnesnoble|atm foreign trns fee|atm fee|atm withdrawl press start|chatgpt subscription|now withdrawal zelle|ross stores|ash ave comics|tjmaxx|target|akchin pavilion|talking stick resort|steamgames.com|max od access fee|amazon.com|l essence day spa|natural selection|bath and body works|paypal|withdrawal zelle|withdrawal - zelle|wd - venmo*|wd  venmo*|dndbeyond|slushees vapor|steam purchase|amzn mktp'),
                          'Other', df['Category'])

# Subscriptions
df['Category'] = np.where(df['Description'].str.contains
                          ('filestar|hostgator|apple.com|spotify|netflix|roku|youneedabudget.com|amazon prime'),
                          'Subscriptions', df['Category'])

# Health & Wellness
df['Category'] = np.where(df['Description'].str.contains
                          ('remi|tracy legee|ellen b. mcbride|one stop nutrition|renown health'),
                          'Health & Wellness', df['Category'])

# Savings In
df['Category'] = np.where(df['Description'].str.contains
                          ('internet transfer from greater nevada credit union|deposit - internet transfer from|deposit internet transfer from x|deposit rent|deposit dental insurance|deposit upcoming bills'),
                          'Savings In', df['Category'])

# Savings Out
df['Category'] = np.where(df['Description'].str.contains
                          ('withdrawl morgans bday|withdrawal addis part of fob tic|withdrawal costco|withdrawl internet transfer to|internet transfer to greater nevada credit union|overdraft protection withdraw') & (df['Account Name'].str.contains('high yield savings acct|regular share')),
                          'Savings Out', df['Category'])

#Income
df['Category'] = np.where(df['Description'].str.contains
                          ('now deposit  zelle|descriptive deposit cash back|credit interest|now deposit - zelle|descriptive deposit - cash back|now deposit zelle|cashout|interest payment|external dp assist-2-sell|automatic statement credit|external dp - assist-2-sell|external dp venmo cashout|now deposit zelle from ihc-met|descriptive deposit cashback|atm deposit|descriptive deposit - cashback'),
                          'Income', df['Category'])

#Excluded
df['Category'] = np.where(df['Description'].str.contains
                          ('deposit morgans bday|withdrawal repay savings costco|withdrawl upcoming bills|withdrawl dental insurance|withdrawl rent|withdrawal internet transfer to|deposit internet transfer from x|overdraft protection deposit|external dp - fisher,maya person|external wd - discover dc pymnts|external wd discover dc pymnts|external dp fisher,maya person|external wd americanexpress pe|tiktok shop seller|american express|withdrawal - internet transfer t') & (df['Account Name'].str.contains('cash back student checking')),
                          'Excluded', df['Category'])

#changes to date column
df['Date'] = pd.to_datetime(df['Date']) #conver to datetime format

df['Month'] = df['Date'].dt.month       #extract month and make new column
df['Year'] = df['Date'].dt.year         #extract year and make new column

# Create Summary - last months income, recurring expenses, non-recurring expenses, savings
latest_month = date.today().month       #get the latest month
latest_year = df['Year'].max()          #get the latest year

last_month_expenses = df[(df['Month'] == latest_month) & (df['Year'] == latest_year)]                                       #create new dataframe and add in data from previous dataframe that is from the latest month and year

last_month_expenses = last_month_expenses.groupby('Category')['Amount'].sum().reset_index()                                 #group by category, get total of each category, set back to original order

#note: important to sum all data before removing '-' so we have negatives and positives being calculated for the correct sum

last_month_expenses['Amount'] = last_month_expenses['Amount'].astype('str')                                                 #convert data in amount column to a string
last_month_expenses['Amount'] = last_month_expenses['Amount'].str.replace('-', '')                                          #remove all '-' drom data in amount column
last_month_expenses['Amount'] = last_month_expenses['Amount'].astype('float')                                               #convert data in amount column back to a float

last_month_expenses = last_month_expenses[last_month_expenses['Category'].str.contains('Excluded|unassigned') == False]     #filter categories and exxclude any labeled "excluded' or 'unassigned'
last_month_expenses = last_month_expenses.sort_values(by='Amount', ascending=False)                                         #Sort data in dataframe by the ascending values in the amount column
last_month_expenses['Amount'] = last_month_expenses['Amount'].round().astype(int)                                           #round the values in amount category to nearest whole number and then convert to type integer


#get amounts for income, savings in, and avings out
income_row = last_month_expenses[last_month_expenses['Category'] == 'Income']           #get the row in the data frame that the category 'income' is located
income = income_row['Amount'].iloc[0] if not income_row.empty else 0                    #get the value in the amount column for the category labeled income

savings_in_row = last_month_expenses[last_month_expenses['Category'] == 'Savings In']   #get the row in the data frame that the category 'savings in' is located
savings_in = savings_in_row['Amount'].iloc[0] if not savings_in_row.empty else 0        #get the value in the amount column for the category labeled savings in

savings_out_row = last_month_expenses[last_month_expenses['Category'] == 'Savings Out'] #get the row in the data frame that the category 'savings out' is located
savings_out = savings_out_row['Amount'].iloc[0] if not savings_out_row.empty else 0     #get the value in the amount column for the category labeled savings out

total_saved = savings_in - savings_out                                                  #calculate total saved


last_month_expenses_tot = last_month_expenses['Amount'].sum() - (income + total_saved)   #calculate the total monthly expenses minus income and total saved

#Create widfets for the dashboard using the panel library
income_widget = pn.widgets.TextInput(name="Income", value=str(income))
recurring_expenses_widget = pn.widgets.TextInput(name="Recurring Expenses", value="0")
monthly_expenses_widget = pn.widgets.TextInput(name="Monthly Expenses", value=str(last_month_expenses_tot))
difference_widget = pn.widgets.TextInput(name="Last Month's Savings", value="0")

#define calculate_difference
#retrieves wideget values and converts them to type float the calculates the differnce between income and recurring and monthly expenses, then updates value of difference widget
def calculate_difference(event):
    income = float(income_widget.value)
    recurring_expenses = float(recurring_expenses_widget.value)
    monthly_expenses = float(monthly_expenses_widget.value)
    difference = income - recurring_expenses - monthly_expenses
    difference_widget.value = str(difference)

#Watch for changes in value for the below widgets
income_widget.param.watch(calculate_difference, "value")
recurring_expenses_widget.param.watch(calculate_difference, "value")
monthly_expenses_widget.param.watch(calculate_difference, "value")


#create a bar chart using hvplot libary
#allows user to visualize expenses for each category from the last month
last_month_expenses_chart = last_month_expenses.hvplot.bar(
    x='Category',
    y='Amount',
    height=250,
    width=850,
    title="Last Month Expenses",
    ylim=(0, 500))


df['Date'] = pd.to_datetime(df['Date'])                                                                 #convert date column to datetime format
df['Month-Year'] = df['Date'].dt.to_period('M')                                                         #Create new column called month-year
monthly_expenses_trend_by_cat = df.groupby(['Month-Year', 'Category'])['Amount'].sum().reset_index()    #group and sum expenses by month-year column

monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].astype('str')                                               #convert amount column to type string
monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].str.replace('-', '')                                        #remove all '-' from data in amount column
monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].astype('float')                                             #convert amount column back to type float
monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat[monthly_expenses_trend_by_cat['Category'].str.contains('Excluded') == False]  #remove any data that is labeled as 'excluded'

monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat.sort_values(by='Amount', ascending=False) #sort the dataframe based on the amount column
monthly_expenses_trend_by_cat['Amount'] = monthly_expenses_trend_by_cat['Amount'].round().astype(int)   #round values in amount column to whole numbers and convert to tpye int
monthly_expenses_trend_by_cat['Month-Year'] = monthly_expenses_trend_by_cat['Month-Year'].astype(str)   #convert data in month-year column to type string
monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat.rename(columns={'Amount': 'Amount '})     #rename the amount column

#create dropdown widget for dashboard using the panel library
#lets user choose a specific category to visualize data from only the selected category
select_category = pn.widgets.Select(name="Select Category", options=[
    'All',
    'Debt Interest',
    'Credit Card Payments',
    'Pet Food',
    'Insurance',
    'Rent',
    'Power & Gas',
    'Cellphone',
    'Pet Items',
    'Vet Visits',
    'Groceries',
    'Eating Out',
    'Transportation',
    'Dates',
    'Other',
    'Subscriptions',
    'Health & Wellness',
    'Savings In',
    'Savings Out',
    'Income',
    #'Excluded'
 ])

#define plot_expenses
#produces bar chart of monthly expenses using hvplot libary
#bar chart data is baed on category selected in above select category widget
def plot_expenses(category):
    if category == 'All':
        plot_df = monthly_expenses_trend_by_cat.groupby('Month-Year').sum()
    else:
        plot_df = monthly_expenses_trend_by_cat[monthly_expenses_trend_by_cat['Category'] == category].groupby('Month-Year').sum()

    plot = plot_df.hvplot.bar(x='Month-Year', y='Amount')
    return plot

#defines update_plot
#returns a plot from plot_expenses, runs whenever the decorator detectss a change in the select category widget
@pn.depends(select_category.param.value)
def update_plot(category):
    plot = plot_expenses(category)
    return plot

#creates a row layout for dashboard using panel libary 
monthly_expenses_trend_by_cat_chart = pn.Row(select_category, update_plot)
#adjusts the width of the plot displayed on dashboard
monthly_expenses_trend_by_cat_chart[1].width =  600


df = df[['Date', 'Category', 'Description', 'Amount']]  #selects date, category, description, and amount from the dataframe df
df['Amount'] = df['Amount'].astype('str')               #changes amount column to type string
df['Amount'] = df['Amount'].str.replace('-', '')        #remove all '-' from amount column
df['Amount'] = df['Amount'].astype('float')             #convert amount column back to type float

df = df[df['Category'].str.contains('Excluded') == False]   #filter dataframe based on the category column
df['Amount'] = df['Amount'].round().astype(int)             #round values in amount column and change to type int

#defines filter_df
#filters dataframe df based on selected category
def filter_df(category):
    if category == "All":
        return df
    return df[df['Category'] == category]

#sets dimensions for summary table in dashboard
summary_table = pn.widgets.DataFrame(filter_df('All'), height = 1300, width = 400)

#defines update_summary_table
#if an event occurs that changes the selected catgory the summary table is updated
def update_summary_table(event):
    summary_table.value = filter_df(event.new)

select_category.param.watch(update_summary_table, 'value')

#using a FastListTemplate from the panel libary, layout widgets to be shown to the user for dashboard
template = pn.template.FastListTemplate(
    title="Personal Finances Summary",
    sidebar=[
        pn.pane.Markdownn("## *If you can't manage your money, making more won't help*"),
        pn.pane.PNG('vecteezy_pack-of-dollars-money-clipart-design-illustration_9303600_278.png', sizing_mode='scale_both'),
        pn.pane.Markdown(""),
        pn.pane.Markdown(""),
        select_category
        ],
    main=[
        pn.Row(income_widget, recurring_expenses_widget, monthly_expenses_widget, difference_widget, width=950),
        pn.Row(last_month_expenses_chart, height=240),
        pn.GridBox(
            monthly_expenses_trend_by_cat_chart[1],
            summary_table,
            ncols=2,
            width=500,
            align='start',
            sizing_mode='stretch_width'
            )
        ]
    )

template.show()
