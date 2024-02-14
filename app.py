import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import cufflinks as cf
from datetime import datetime, timedelta
from sklearn.preprocessing import MinMaxScaler
# import tensorflow as tf
# from tensorflow.keras.models import Sequential
# from tensorflow.keras.layers import Dense
# from tensorflow.keras.layers import LSTM
import math
from sklearn.metrics import mean_squared_error

# Class LSTM
class LSTM:
    def __init__(self,df):
        self.df = df


# Layout Width
st. set_page_config(layout="wide")
# Sidebar
st.sidebar.subheader('Filter Parameters')

# Retrieving tickers data
ticker_list = pd.read_csv('symbols.txt')
tickerSymbol = st.sidebar.selectbox('Stock ticker', ticker_list) # Select ticker symbol
st.sidebar.markdown("""---""")
st.sidebar.subheader('Choose Dates -')

td = datetime.now()
ed = datetime.now() - timedelta(days=3*365)
start_date = st.sidebar.date_input("Start date", ed )
end_date = st.sidebar.date_input("End date", td)
st.sidebar.header('OR')
st.sidebar.subheader('Choose Period -')
period = st.sidebar.selectbox(
    'Intervals:',
    ('Please Choose','1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo', '6mo', '9mo', '1y', '3y', '6y'))

if tickerSymbol:
    tickerData = yf.Ticker(tickerSymbol) # Get ticker data

    # Ticker information
    if 'logo_url' in tickerData.info:
        string_logo = '<img src=%s>' % tickerData.info['logo_url']
        string_logo = ''
        st.markdown(string_logo, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["Company Overview", "Founders/Directors", "Statistics", "Contact"])

    with tab1:
        if 'longName' in tickerData.info:
            string_name = tickerData.info['longName']
            st.header('**%s**' % string_name, divider='rainbow')

        if 'longBusinessSummary' in tickerData.info:
            string_summary = tickerData.info['longBusinessSummary']
            st.info(string_summary)

    with tab2:
        st.header("Founders/Directors", divider='rainbow')
        if 'companyOfficers' in tickerData.info:
            i = 0
            col1, col2 = st.columns(2)   
            for officer in tickerData.info['companyOfficers']:
                if i%2 == 0:            
                    col1.subheader(officer["name"])
                    for key,val in officer.items():
                        ex = ["name","maxAge"]           
                        if key not in ex:
                            col1.text(key.title() + ": " + str(val))
                else:
                    col2.subheader(officer["name"])
                    for key,val in officer.items():
                        ex = ["name","maxAge"]           
                        if key not in ex:
                            col2.text(key.title() + ": " + str(val))   
                i+=1                     

            
    with tab3:
        st.header('Statistics', divider='rainbow')
        if tickerData.info:
            i = 0
            col1, col2 = st.columns(2) 
            for key,val in tickerData.info.items():
                ex = ["address1","address2","city","state","zip","country","phone","fax","website","city","address1","companyOfficers","longBusinessSummary","longName"]
                if key not in ex:
                    if i%2 == 0: 
                        col1.text(key.title() + ": " + str(val))
                    else:
                        col2.text(key.title() + ": " + str(val))
                    i+=1

    with tab4:
        st.header('Address', divider='rainbow')
        address = ""
        if 'address1' in tickerData.info:
            address = tickerData.info['address1'] + ',\n' 
        if 'address2' in tickerData.info:
            address = tickerData.info['address2'] + ',\n'         
        if 'city' in tickerData.info:        
            address += tickerData.info['city'] + ',\n' 
        if 'state' in tickerData.info:        
            address += tickerData.info['state'] + ',\n' 
        if 'zip' in tickerData.info:        
            address += tickerData.info['zip'] + ',\n' 
        if 'country' in tickerData.info:        
            address += tickerData.info['country'] + ',\n' 
        if 'phone' in tickerData.info:        
            address += "Phone: " + tickerData.info['phone'] + ',\n' 
        if 'fax' in tickerData.info:        
            address += "Fax:" + tickerData.info['fax'] + ',\n'         
        if 'website' in tickerData.info:        
            address += tickerData.info['website']
        st.text(address)   


    # Ticker data
    if period != 'Please Choose':
        if period in ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d']:
            tickerDf = tickerData.history(period=period, interval="1m") #get the historical prices for this ticker
        elif period in ['5d', '1wk']:
            tickerDf = tickerData.history(period=period, interval="1h") #get the historical prices for this ticker
        else:
            tickerDf = tickerData.history(period=period, interval="1d") #get the historical prices for this ticker
    else:
        tickerDf = tickerData.history(period='1d', start=start_date, end=end_date) #get the historical prices for this ticker

    if not tickerDf.empty:
        st.header('Ticker data', divider='rainbow')
        st.dataframe(tickerDf,use_container_width=True)

        # Bollinger bands
        st.header('Bollinger Bands', divider='rainbow')
        tab11, tab12, tab13, tab14 = st.tabs(["Bollinger 1", "Bollinger 2", "Bollinger 3", "Bollinger 4"])
        with tab11:
            qf = cf.QuantFig(tickerDf,title='STD-1',legend='top',name='GS',up_color='green', down_color='red')
            qf.add_bollinger_bands(periods=20, boll_std=1, colors=['cyan','grey'], fill=True,)
            qf.add_volume(name='Volume',up_color='green', down_color='red')
            fig = qf.iplot(asFigure=True)
            st.plotly_chart(fig, use_container_width=True)

        with tab12:
            qf = cf.QuantFig(tickerDf,title='STD-2',legend='top',name='GS',up_color='green', down_color='red')
            qf.add_bollinger_bands(periods=10, boll_std=2, colors=['cyan','grey'], fill=True,)
            qf.add_volume(name='Volume',up_color='green', down_color='red')
            fig = qf.iplot(asFigure=True)
            st.plotly_chart(fig, use_container_width=True)

        with tab13:
            pass

        with tab14:
            pass

        # Bollinger bands
        st.header('Models, Accuracy and Prediction', divider='rainbow')
        tab21, tab22, tab23, tab24 = st.tabs(["LSTM", "Chart 1", "Chart 2", "Chart 3"])
        with tab21:
            pass

    else:
        st.write('Unable to find!')
    ####
    # st.write('---')
    # st.write(tickerData.info)
else:
    st.write('Unable to find!')