# import required lib
import pandas as pd 
import matplotlib.pyplot as plt
import seaborn as sns
import calendar 
import datetime
import holidays
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)
#!pip install holidays
#from datetime import date

import warnings
warnings.filterwarnings("ignore")
st.set_page_config(
        page_title="Event App",
)
#import data from CSV
orders = pd.read_csv("orders.csv")
holiday_data = pd.read_csv("holiday_data.csv")

#List of events 
events = holiday_data.holiday.unique()

#Streamlit app deatils
st.title('Sales/Orders graph from the selected event')

option = st.sidebar.selectbox(
    'Which event do you select?',
     events)
#pass one event to holiday data and fetch past 4 year dates.
event_data = holiday_data[holiday_data.holiday == option].sort_values(by=['year'],ascending = False).head(4)

#select days 
days = st.sidebar.selectbox(
    'Select days?',
     [10,20,30])

#select past or future
future_past = st.sidebar.selectbox(
    'Select Future/Past?', ['Future','Past'])

#select sales or orders
y = st.sidebar.selectbox(
    'Select Sales/Orders?',['quantity','total'])

#collect current year
current_year = datetime.date.today().year
    
#apply it to orders data and plot, before that add aloop which executes four times.
color = [['red'],['blue'],['orange'],['green']]

if option is not None and days is not None and future_past is not None and y is not None:
    j = 0
    if future_past == "Future":
        for i in event_data.Date:
            d = datetime.datetime.strptime(i,'%Y-%m-%d') + datetime.timedelta(days=(days))
            sns.lineplot(data = orders[(orders['Date'] > str(i)) & (orders['Date'] < str(d))], x ="Day", y =y , hue = 'Year',estimator = sum,palette=color[j])
            j = j+1
        plt.ylabel(y)
        plt.xlabel('Date')
        plt.legend()
        st.pyplot()
    elif future_past == 'Past':
        for i in event_data.Date:
            d = datetime.datetime.strptime(i,'%Y-%m-%d') + datetime.timedelta(days=(-1*days))
            sns.lineplot(data = orders[(orders['Date'] > str(d)) & (orders['Date'] < str(i))], x ="Day", y =y , hue = 'Year',estimator = sum,palette=color[j])
            j = j+1
        plt.ylabel(y)
        plt.xlabel('Date')
        plt.legend()
        st.pyplot()
    else:
        print("Date is not correct")
    #Streamlit app deatils
    st.title('Most products sold from the selected event')
    j = 0
    data = []
    data = pd.DataFrame(data)
    if future_past == "Future":
        for i in event_data.Date:
            d = datetime.datetime.strptime(i,'%Y-%m-%d') + datetime.timedelta(days=(days))
            data = data.append(orders[(orders['Date'] > str(i)) & (orders['Date'] < str(d))])
            j = j+1
        data.product_name.value_counts().head(10).plot.barh(rot=0)
        plt.xlabel('Count')
        st.pyplot()
    elif future_past == 'Past':
        for i in event_data.Date:
            d = datetime.datetime.strptime(i,'%Y-%m-%d') + datetime.timedelta(days=(-1*days))
            data = data.append(orders[(orders['Date'] > str(d)) & (orders['Date'] < str(i))])
            j = j+1
        data.product_name.value_counts().head(10).plot.barh(rot=0)
        plt.xlabel('Count')
        st.pyplot()
    else:
        print("Date is not correct")

else:
    st.write("Please select the the inputs")