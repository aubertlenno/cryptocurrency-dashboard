import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import yfinance as yf
from datetime import datetime


st.set_page_config(
    page_title="Home",
    page_icon="🏠",
    initial_sidebar_state="expanded"
)
st.sidebar.header("Options")