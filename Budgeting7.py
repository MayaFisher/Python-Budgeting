from calendar import month
from operator import contains
from tkinter import LAST
import pandas as pd
import numpy as np

import gspread

import panel as pn
pn.extension('tabulator')
import hvplot.pandas
import holoviews as hv
hv.extension('bokeh')
from datetime import date

gc = gspread.service_account(filename="service_account.json")
sh = gc.open("transactions")

ws = sh.worksheet('transactions')
df = pd.DataFrame(ws.get_all_records())

df = df[['Date', 'Description', 'Amount', 'Transaction Type', 'Account Name']]
df['Description'] = df["Description"].map(str.lower)
df['Transaction Type'] = df['Transaction Type'].map(str.lower)
df['Account Name'] = df['Account Name'].map(str.lower)

df['Category'] = 'unassigned'

#df.loc['Amount'] = '-' + df['Amount'].map('{:,.0f}'.format)# - need to adjust to be just items where category isn't income.

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

#Add '-' to amounts where money was spent
#df['Amount'] = np.where(~df['Category'].str.contains
#                        ('Excluded|Savings In|Income'),
#                        '-' + df['Amount'].map('{:,.2f}'.format), df['Amount'])


df['Date'] = pd.to_datetime(df['Date'])

df['Month'] = df['Date'].dt.month
df['Year'] = df['Date'].dt.year

# Create Summary Banner - last months income, recurring expenses, non-recurring expenses, savings
latest_month = date.today().month - 1 #change back to be just latest month
latest_year = df['Year'].max()

last_month_expenses = df[(df['Month'] == latest_month) & (df['Year'] == latest_year)]

last_month_expenses = last_month_expenses.groupby('Category')['Amount'].sum().reset_index()

last_month_expenses['Amount'] = last_month_expenses['Amount'].astype('str')
last_month_expenses['Amount'] = last_month_expenses['Amount'].str.replace('-', '')
last_month_expenses['Amount'] = last_month_expenses['Amount'].astype('float')

last_month_expenses = last_month_expenses[last_month_expenses['Category'].str.contains('Excluded|unassigned') == False]
last_month_expenses = last_month_expenses.sort_values(by='Amount', ascending=False)
last_month_expenses['Amount'] = last_month_expenses['Amount'].round().astype(int)

#print(last_month_expenses)

income_row = last_month_expenses[last_month_expenses['Category'] == 'Income']
income = income_row['Amount'].iloc[0] if not income_row.empty else 0

savings_in_row = last_month_expenses[last_month_expenses['Category'] == 'Savings In']
savings_in = savings_in_row['Amount'].iloc[0] if not savings_in_row.empty else 0

#savings_out_row = last_month_expenses[last_month_expenses['Category'] == 'Savings Out']
#savings_out = savings_out_row['Amount'].iloc[0] if not savings_out_row.empty else 0

#total_saved = savings_in - savings_out


last_month_expenses_tot = last_month_expenses['Amount'].sum() - (income + savings_in)

income_widget = pn.widgets.TextInput(name="Income", value=str(income))
recurring_expenses_widget = pn.widgets.TextInput(name="Recurring Expenses", value="0")
monthly_expenses_widget = pn.widgets.TextInput(name="Monthly Expenses", value=str(last_month_expenses_tot))
difference_widget = pn.widgets.TextInput(name="Last Month's Savings", value="0")

def calculate_difference(event):
    income = float(income_widget.value)
    recurring_expenses = float(recurring_expenses_widget.value)
    monthly_expenses = float(monthly_expenses_widget.value)
    difference = income - recurring_expenses - monthly_expenses
    difference_widget.value = str(difference)

income_widget.param.watch(calculate_difference, "value")
recurring_expenses_widget.param.watch(calculate_difference, "value")
monthly_expenses_widget.param.watch(calculate_difference, "value")

pn.Row(income_widget, recurring_expenses_widget, monthly_expenses_widget, difference_widget).show()

last_month_expenses_chart = last_month_expenses.hvplot.bar(
    x='Category',
    y='Amount',
    height=250,
    width=850,
    title="Last Month Expenses",
    ylim=(0, 500))

df['Date'] = pd.to_datetime(df['Date'])
df['Month-Year'] = df['Date'].dt.to_period('M')
monthly_expenses_trend_by_cat = df.groupby(['Month-Year', 'Category'])['Amount'].sum().reset_index()

monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].astype('str')
monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].str.replace('-', '')
monthly_expenses_trend_by_cat['Amount']=monthly_expenses_trend_by_cat['Amount'].astype('float')
monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat[monthly_expenses_trend_by_cat['Category'].str.contains('Excluded') == False]

monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat.sort_values(by='Amount', ascending=False)
monthly_expenses_trend_by_cat['Amount'] = monthly_expenses_trend_by_cat['Amount'].round().astype(int)
monthly_expenses_trend_by_cat['Month-Year'] = monthly_expenses_trend_by_cat['Month-Year'].astype(str)
monthly_expenses_trend_by_cat = monthly_expenses_trend_by_cat.rename(columns={'Amount': 'Amount '})

select_category1 = pn.widgets.Select(name="Select Category", options=[
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

def plot_expenses(category):
    if category == 'All':
        plot_df = monthly_expenses_trend_by_cat.groupby('Month-Year').sum()
    else:
        plot_df = monthly_expenses_trend_by_cat[monthly_expenses_trend_by_cat['Category'] == category].groupby('Month-Year').sum()

    plot = plot_df.hvplot.bar(x='Month-Year', y='Amount')
    return plot

@pn.depends(select_category1.param.value)
def update_plot(category):
    plot = plot_expenses(category)
    return plot

monthly_expenses_trend_by_cat_chart = pn.Row(select_category1, update_plot)
monthly_expenses_trend_by_cat_chart[1].width =  600

df = df[['Date', 'Category', 'Description', 'Amount']]
df['Amount'] = df['Amount'].astype('str')
df['Amount'] = df['Amount'].str.replace('-', '')
df['Amount'] = df['Amount'].astype('float')

df = df[df['Category'].str.contains('Excluded') == False]
df['Amount'] = df['Amount'].round().astype(int)

def filter_df(category):
    if category == "All":
        return df
    return df[df['Category'] == category]

summary_table = pn.widgets.DataFrame(filter_df('All'), height = 1300, width = 400)

def update_summary_table(event):
    summary_table.value = filter_df(event.new)

select_category1.param.watch(update_summary_table, 'value')


template = pn.template.FastListTemplate(
    title="Personal Finances Summary",
    sidebar=[
        pn.pane.Markdownn("## *If you can't manage your money, making more won't help*"),
        pn.pane.PNG('vecteezy_pack-of-dollars-money-clipart-design-illustration_9303600_278.png', sizing_mode='scale_both'),
        pn.pane.Markdown(""),
        pn.pane.Markdown(""),
        select_category1
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

#pd.options.display.max_rows = 999
#pd.options.display.max_columns = 999
#print(df.head(200))