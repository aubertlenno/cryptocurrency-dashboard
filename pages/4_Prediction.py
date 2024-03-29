# Importing modules
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd
import plotly.graph_objs as go
from prophet import Prophet
from prophet.plot import plot_plotly

# Setting the page configuration
st.set_page_config(
    page_title="Prediction",
    page_icon="🔮",
    initial_sidebar_state="expanded",   
)

# Making the sidebar
sources = st.sidebar.expander('Data source')
sources.write('''[Yahoo Finance](https://finance.yahoo.com)''')

# Defining class name
class Prediction:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol
    
    # Make function for getting the data of the crypto
    def getData(self):
        ticker = self.symbol + "-USD"
        initialize = yf.Ticker(ticker)
        data = initialize.history(period='3y', interval='1d')
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.date
        return data

    # Make function to get the data for the prediction
    def getDataForPrediction(self):
        ticker = self.symbol + "-USD"
        initialize = yf.Ticker(ticker)
        data = initialize.history(period='3y', interval='1d')
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])
        data['Date'] = data['Date'].dt.date
        data = data.rename(columns={"Date": "ds", "Close": "y"})
        return data

    
    def visualize(self,data):
        # Converting the datatype to float
        for i in ['Open', 'High', 'Close', 'Low']:
            data[i] = data[i].astype('float64')

        # Making the chart
        fig = go.Figure([go.Scatter(x=data['Date'], y=data['High'])])

        # Change the label for y-axis
        fig.update_layout(
            yaxis_title = 'Price (in US Dollars)'
        )

        # Make the slider and time period
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=1, label="1mo", step="month", stepmode="backward"),
                    dict(count=6, label="6mo", step="month", stepmode="backward"),
                    dict(count=1, label="YTD", step="year", stepmode="todate"),
                    dict(count=1, label="1y", step="year", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )
        
        return fig

    def predict(self,data):
        # Fitting the model
        model = Prophet()
        model.fit(data)

        # Predict
        future = model.make_future_dataframe(periods=180)
        prediction = model.predict(future)

        # Plot in a graph
        fig = plot_plotly(m=model, fcst=prediction, xlabel='Date', ylabel='Closing Price (in USD)', figsize=(700,500))
        return fig        

# Printing the page title
st.title('Prediction')

# Listing crypto names and symbols
crypto_name = ["Bitcoin (BTC)", "Ethereum (ETH)", "XRP (XRP)", "Tether (USDT)", "Dogecoin (DOGE)", "Cardano (ADA)", "Polygon (MATIC)", "Binance Coin (BNB)", "USD Coin (USDC)", "Binance USD (BUSD)"]

# make selectbox widget
selected = st.selectbox(label='Select your cryptocurrency', options=crypto_name)

# Solit the name and the symbol of the cryptocurrency
words = selected.split(" ")
crypto_name = " ".join(words[:-1])
crypto_symbol = words[-1].strip("()")

# Initializing class
crypto_predict = Prediction(crypto_name, crypto_symbol)

# Get data the data
crypto_data_3y = crypto_predict.getData()
crypto_data_for_prediction = crypto_predict.getDataForPrediction()

# Printing on Streamlit
st.subheader('Live 3 Years Chart')
st.plotly_chart(crypto_predict.visualize(crypto_data_3y))

st.subheader('6 Months Prediction')
disc = st.expander('Disclaimer. (Click to expand)')
disc.write("This is not a financial advise, buy at your own risk.")
st.plotly_chart(crypto_predict.predict(crypto_data_for_prediction))
