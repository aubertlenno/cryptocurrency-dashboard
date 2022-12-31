import streamlit as st

st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    initial_sidebar_state="expanded",
    layout='wide'
)

sources = st.sidebar.expander('Data source')
sources.write('''[Yahoo Finance](https://finance.yahoo.com)''')

st.title('Cryptocurrency Dashboard')

st.image(image='./web-img/crypto.jpeg', width=800)

st.markdown(
    '''
    ## Overview
    The cryptocurrency market is currently having a nightmare. Many coins experiencing price downfall more than 50% from early 2022. The biggest marketcap crypto, Bitcoin, down 65% year to date. In this web app I provide visualize some data of the top 10 market capitalization cryptocurrencies (as of 31 December 2022). I also make a price prediction to see the estimate future of cryptocurrencies.
    '''
)

st.markdown(
    '''
    ## Definition
    Cryptocurrency is a digital or virtual currency that uses cryptography for security and is decentralized, meaning it is not controlled by a central authority such as a government or financial institution. Cryptocurrencies are designed to be used as a medium of exchange, and they use decentralized control as opposed to centralized digital currency and central banking systems.

    The most well-known cryptocurrency is Bitcoin, but there are many other types of cryptocurrencies, such as Ethereum, XRP, and Cardano. Cryptocurrencies are created through a process called mining, in which a network of computers around the world work together to solve complex mathematical problems. When a problem is solved, a new block is added to the blockchain, which is a public ledger that records all transactions made with the cryptocurrency.

    Cryptocurrencies have gained popularity in recent years due to their decentralized nature, security, and potential for increased privacy compared to traditional financial transactions. However, they are not without their drawbacks, as their value can be volatile and they have been associated with illegal activities.
    '''
)

st.markdown(
    '''
    ## Disclaimer
    The historical data is retrieved from [Yahoo Finance](https://finance.yahoo.com).
    
    **This site does not contain financial advice.** The financial information is provided for general informational and educational purposes only and is not a substitute for professional advice.

    Accordingly, before taking any actions based upon such information, I encourage you to consult with the appropriate professionals. I do not provide any kind of financial advice. The use or reliance of any information contained on this site is solely at your own risk.
    '''
)