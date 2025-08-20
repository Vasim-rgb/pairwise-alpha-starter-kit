import streamlit as st
import pandas as pd
from gote import get_coin_metadata, generate_signals

st.title("Pairwise Alpha Strategy Signals")

df = pd.read_csv('market1_data.csv')

# Only keep rows where SOL 4H price is available
df = df[df['close_SOL_4H'].notna()]

anchor_df = pd.DataFrame({
    'timestamp': df['timestamp'],
    'close_BTC_1H': df['close_BTC_1H'],
    'close_ETH_2H': df['close_ETH_2H']
})
target_df = pd.DataFrame({
    'timestamp': df['timestamp'],
    'close_SOL_4H': df['close_SOL_4H']
})

signals = generate_signals(anchor_df, target_df)

st.write("Signal Table")
st.dataframe(signals)

st.line_chart(signals['position_size'])