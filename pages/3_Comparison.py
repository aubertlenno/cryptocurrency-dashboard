# Importing Modules
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.express as px

# Setting the page configuration
st.set_page_config(
    page_title="Comparison",
    page_icon="💡",
    initial_sidebar_state="expanded"
)

# Making the sidebar
sources = st.sidebar.expander('Data source')
sources.write('''[Yahoo Finance](https://finance.yahoo.com)''')

# Printing the title for the page
st.title("Cryptocurrencies Comparison")

# Listing the name of the top 10 market capitalization cryptocurrencies
crypto_name = ["Bitcoin (BTC)", "Ethereum (ETH)", "XRP (XRP)", "Tether (USDT)", "Dogecoin (DOGE)", "Cardano (ADA)", "Polygon (MATIC)", "Binance Coin (BNB)", "USD Coin (USDC)", "Binance USD (BUSD)"]

# Initializing empty lists for the crypto names and symbols
names = []
symbols = []

# splitting the crypto name and the symbol
for crypto in crypto_name:
    name, symbol = crypto.split("(")
    names.append(name.strip())
    symbols.append(symbol.strip().replace(")", ""))

# Making the multiselection widgets
selected = st.multiselect("Choose the cryptocurrencies you want to compare", symbols, [symbols[0], symbols[1]])

# Initializing empty list for the dataframe and marketcap
dataframe_list = []
marketcap_list = []

for crypto in selected:
    ticker = yf.Ticker(crypto + '-USD')
    hist = ticker.history(period='5y', interval='1d') # Getting the 5 years historical data
    info = ticker.info 
    marketcap_list.append(info['marketCap']) # Retrieving the marketcap of the crypto
    hist['Name'] = crypto # Add new column for the crypto name
    dataframe_list.append(hist) # Appending the hist dataframe into dataframe_list

# Combine the dataframe of selected crypto to be compared
combined = pd.concat(dataframe_list)
combined = combined.reset_index()

# Making the line chart for visualizing the price comparison
fig = px.line(
    data_frame=combined,
    x="Date",
    y="Close",
    color="Name",
    labels={
        "Close": "Closing Price (in USD)"
    }
    )

# Visualizing the bar chart for the market capitalization comparison
marketcap_df = pd.DataFrame({'Name':selected,'Marketcap':marketcap_list})
marketcap_fig = px.bar(marketcap_df, 'Name', 'Marketcap')

# Show in the Streamlit page
st.subheader("Price Comparison")
st.plotly_chart(fig)
st.subheader("Marketcap Comparison")
st.plotly_chart(marketcap_fig)