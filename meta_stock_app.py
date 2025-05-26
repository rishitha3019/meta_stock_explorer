import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Load Data (replace with actual path or Kaggle load)
@st.cache_data
def load_data():
    df = pd.read_csv("meta_stock_data.csv")  # Ensure this file is present in the same directory
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values("Date", inplace=True)
    return df

df = load_data()

# Sidebar - Date range selector
st.sidebar.header("Filter Options")
start_date = st.sidebar.date_input("Start Date", df["Date"].min())
end_date = st.sidebar.date_input("End Date", df["Date"].max())

# Validate date range
if start_date > end_date:
    st.sidebar.error("End date must fall after start date.")

filtered_df = df[(df["Date"] >= pd.to_datetime(start_date)) & (df["Date"] <= pd.to_datetime(end_date))]

# Sidebar - Moving average selection
st.sidebar.subheader("Moving Averages")
ma1 = st.sidebar.slider("MA 1 (days)", 5, 50, 10)
ma2 = st.sidebar.slider("MA 2 (days)", 5, 100, 20)

# Add moving averages to the dataframe
filtered_df[f"MA_{ma1}"] = filtered_df["Close"].rolling(window=ma1).mean()
filtered_df[f"MA_{ma2}"] = filtered_df["Close"].rolling(window=ma2).mean()

# Title
st.title("📈 Meta Stock Explorer")
st.markdown("Explore Meta's stock performance with interactive filters, moving averages, and candlestick charts.")

# Candlestick Chart
fig = go.Figure()
fig.add_trace(go.Candlestick(
    x=filtered_df['Date'],
    open=filtered_df['Open'],
    high=filtered_df['High'],
    low=filtered_df['Low'],
    close=filtered_df['Close'],
    name='Candlestick'
))

# Moving Averages on chart
fig.add_trace(go.Scatter(
    x=filtered_df['Date'], y=filtered_df[f"MA_{ma1}"],
    mode='lines', name=f"MA {ma1}"
))
fig.add_trace(go.Scatter(
    x=filtered_df['Date'], y=filtered_df[f"MA_{ma2}"],
    mode='lines', name=f"MA {ma2}"
))

fig.update_layout(
    title="Meta Stock Price Chart",
    xaxis_title="Date",
    yaxis_title="Price (USD)",
    xaxis_rangeslider_visible=False,
    template="plotly_white"
)

st.plotly_chart(fig, use_container_width=True)

# Display Data
if st.checkbox("Show Raw Data"):
    st.subheader("Raw Data")
    st.write(filtered_df)

# Footer
st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and Plotly")
