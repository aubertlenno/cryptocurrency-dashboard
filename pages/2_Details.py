import streamlit as st
import plotly.graph_objs as go
import yfinance as yf
import plotly.express as px

st.set_page_config(
    page_title="Details",
    page_icon="🔍",
    initial_sidebar_state="expanded"
)

sources = st.sidebar.expander('Data source')
sources.write('''[Yahoo Finance](https://finance.yahoo.com)''')

class Crypto:
    def __init__(self, name, symbol):
        self.__name = name
        self.__symbol = symbol
        self.ticker = symbol + "-USD"
        self.initialize = yf.Ticker(self.ticker)
        self.data_1d = self.initialize.history(period="1d", interval="5m")
        self.data_3y = self.initialize.history(period="3y", interval="1d")

    def make_candlestick(self):
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=self.data_1d.index,
            open=self.data_1d['Open'],
            high=self.data_1d['High'],
            low=self.data_1d['Low'],
            close=self.data_1d['Close'], name = 'market data'))

        fig.update_layout(
            title=self.__name + ' 24 Hours Candlestick Chart',
            yaxis_title=self.__name + ' Price (in US Dollars)'
        )

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

        cs.increasing.fillcolor = '#3D9970'
        cs.increasing.line.color = '#3D9970'
        cs.decreasing.fillcolor = '#FF4136'
        cs.decreasing.line.color = '#FF4136'

        return fig

    def make_line_price(self):
        # Reseting the index
        df = self.data_3y.reset_index()
        # Converting the datatype to float
        for i in ['Open', 'High', 'Close', 'Low']:
            df[i] = df[i].astype('float64')

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

    def get_info(self):
        info = self.initialize.info
        description = info.get('description')
        return description




st.title("Details")

crypto_name = ["Bitcoin (BTC)", "Ethereum (ETH)", "XRP (XRP)", "Tether (USDT)", "Dogecoin (DOGE)", "Cardano (ADA)", "Polygon (MATIC)", "Binance Coin (BNB)", "USD Coin (USDC)", "Binance USD (BUSD)"]

selected = st.selectbox("Cryptocurrency", crypto_name)
words = selected.split(" ")
crypto_name = " ".join(words[:-1])
crypto_symbol = words[-1].strip("()")

crypto_details = Crypto(crypto_name, crypto_symbol)
crypto_candlestick = crypto_details.make_candlestick()
crypto_info = crypto_details.get_info()
crypto_line = crypto_details.make_line_price()

st.subheader(f"About {crypto_name} ({crypto_symbol})")
st.info(f"{crypto_info}")

st.plotly_chart(crypto_line)
st.plotly_chart(crypto_candlestick)