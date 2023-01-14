# Importing library
import streamlit as st
import plotly.graph_objs as go
import yfinance as yf
import plotly.express as px

# Page configuration setting
st.set_page_config(
    page_title="Details",
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

# Make sidebar
sources = st.sidebar.expander('Data source')
sources.write('''[Yahoo Finance](https://finance.yahoo.com)''')

# Defining class name
class Crypto:
    def __init__(self, name, symbol):
        self.__name = name
        self.__symbol = symbol
        self.ticker = symbol + "-USD"
        self.initialize = yf.Ticker(self.ticker)
        self.data_1d = self.initialize.history(period="1d", interval="5m") # Get the historical data for 1 day with 5 minute interval
        self.data_3y = self.initialize.history(period="3y", interval="1d") # Get the historical data for 3 years with 1 day interval


    # Function for making the candlestick chart
    def make_candlestick(self):
        fig = go.Figure()

        # Making the candlestick chart using plotly.graph_objs
        fig.add_trace(go.Candlestick(x=self.data_1d.index,
            open=self.data_1d['Open'],
            high=self.data_1d['High'],
            low=self.data_1d['Low'],
            close=self.data_1d['Close'], name = 'market data'))

        # Change the title of the graph and the label for the y-axis
        fig.update_layout(
            title=self.__name + ' 24 Hours Candlestick Chart',
            yaxis_title=self.__name + ' Price (in US Dollars)'
        )

        # Enabling the slider below the graph and setting the range when button pressed (15 minutes, 45 minutes, hour to date, and 6 hours)
        fig.update_xaxes(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=list([
                    dict(count=15, label="15m", step="minute", stepmode="backward"),
                    dict(count=45, label="45m", step="minute", stepmode="backward"),
                    dict(count=1, label="HTD", step="hour", stepmode="todate"),
                    dict(count=6, label="6h", step="hour", stepmode="backward"),
                    dict(step="all")
                ])
            )
        )

        cs = fig.data[0]

        # Changing the color of candlestick when up and down
        cs.increasing.fillcolor = '#3D9970'
        cs.increasing.line.color = '#3D9970'
        cs.decreasing.fillcolor = '#FF4136'
        cs.decreasing.line.color = '#FF4136'

        return fig

    # Function for making the line chart
    def make_line_price(self):
        # Reseting the index
        df = self.data_3y.reset_index()
        for i in ['Open', 'High', 'Close', 'Low']:
            df[i] = df[i].astype('float64')

        # Making the line chart
        fig = go.Figure([go.Scatter(x=df['Date'], y=df['High'])])

        fig.update_layout(
            title=self.__name + ' 3 Years Chart',
            yaxis_title=self.__name + ' Price (in US Dollars)'
        )

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

    # Function for getting the brief description of the selected cryptocurrency
    def get_info(self):
        info = self.initialize.info
        description = info.get('description')
        return description



# Writing the title for the page
st.title("Details")

# Listing the top 10 market capitalization crypto
crypto_name = ["Bitcoin (BTC)", "Ethereum (ETH)", "XRP (XRP)", "Tether (USDT)", "Dogecoin (DOGE)", "Cardano (ADA)", "Polygon (MATIC)", "Binance Coin (BNB)", "USD Coin (USDC)", "Binance USD (BUSD)"]

# make the selectbox for selecting the crypto
selected = st.selectbox("Cryptocurrency", crypto_name)

# splitting the name and the symbol of the crypto for example: name is 'Bitcoin' and symbol is 'BTC'
words = selected.split(" ")
crypto_name = " ".join(words[:-1])
crypto_symbol = words[-1].strip("()")

# Executing the functions from the class
crypto_details = Crypto(crypto_name, crypto_symbol)
crypto_candlestick = crypto_details.make_candlestick()
crypto_info = crypto_details.get_info()
crypto_line = crypto_details.make_line_price()

# making the crypto info section
st.subheader(f"About {crypto_name} ({crypto_symbol})")
st.info(f"{crypto_info}")

# printing the line and candlestick chart to the streamlit
st.plotly_chart(crypto_line)
st.plotly_chart(crypto_candlestick)