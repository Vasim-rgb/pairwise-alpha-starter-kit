import pandas as pd
from gote import get_coin_metadata, generate_signals

def load_data():
    # Load your market data CSV
    df = pd.read_csv('market_data.csv')
    # Example: create anchor and target DataFrames for BONK, BTC, ETH
    anchor_df = pd.DataFrame({
        'timestamp': df['timestamp'],
        'close_BTC_4H': df['close_BTC_1H'],  # Use 1H as dummy for 4H
        'close_ETH_2H': df['close_ETH_2H']   # Already present
    })
    target_df = pd.DataFrame({
        'timestamp': df['timestamp'],
        'close_BONK_1H': df['close_BTC_1H']  # Use BTC as dummy for BONK
    })
    return anchor_df, target_df

if __name__ == "__main__":
    anchor_df, target_df = load_data()
    signals = generate_signals(anchor_df, target_df)
    print(signals.head())