import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Comparison",
    page_icon="💡",
    initial_sidebar_state="expanded"
)

sources = st.sidebar.expander('Data source')
sources.write('''[Yahoo Finance](https://finance.yahoo.com)''')

st.title("Cryptocurrencies Comparison")

crypto_name = ["Bitcoin (BTC)", "Ethereum (ETH)", "XRP (XRP)", "Tether (USDT)", "Dogecoin (DOGE)", "Cardano (ADA)", "Polygon (MATIC)", "Binance Coin (BNB)", "USD Coin (USDC)", "Binance USD (BUSD)"]

names = []
symbols = []

for crypto in crypto_name:
    name, symbol = crypto.split("(")
    names.append(name.strip())
    symbols.append(symbol.strip().replace(")", ""))

selected = st.multiselect("Choose the cryptocurrencies you want to compare", symbols, [symbols[0], symbols[1]])

dataframe_list = []
marketcap_list = []

for crypto in selected:
    ticker = yf.Ticker(crypto + '-USD')
    hist = ticker.history(period='5y', interval='1d')
    info = ticker.info
    marketcap_list.append(info['marketCap'])
    hist['Name'] = crypto
    dataframe_list.append(hist)

combined = pd.concat(dataframe_list)
combined = combined.reset_index()

fig = px.line(
    data_frame=combined,
    x="Date",
    y="Close",
    color="Name",
    labels={
        "Close": "Closing Price (in USD)"
    }
    )

marketcap_df = pd.DataFrame({'Name':selected,'Marketcap':marketcap_list})
marketcap_fig = px.bar(marketcap_df, 'Name', 'Marketcap')

st.subheader("Price Comparison")
st.plotly_chart(fig)
st.subheader("Marketcap Comparison")
st.plotly_chart(marketcap_fig)