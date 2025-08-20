"""
This is a sample strategy that demonstrates how to implement a basic trading strategy
that passes all validation requirements. This strategy is for educational purposes only
and does not guarantee profitable trades. Users are encouraged to create their own
strategies based on their trading knowledge and risk management principles.
"""

import pandas as pd
import numpy as np




def get_coin_metadata() -> dict:
    return {
        "targets": [{"symbol": "SOL", "timeframe": "4H"}],
        "anchors": [
            {"symbol": "BTC", "timeframe": "1H"},
            {"symbol": "ETH", "timeframe": "2H"}
        ]
    }

def generate_signals(anchor_df: pd.DataFrame, target_df: pd.DataFrame) -> pd.DataFrame:
    """
    Strategy: Buy LDO if BTC or ETH pumped >2% in the last 4H candle.
    Enhanced with sell conditions and position sizing for complete trading pairs.

    Inputs:
    - anchor_df: DataFrame with timestamp, close_BTC_4H, close_ETH_4H columns
    - target_df: DataFrame with timestamp, close_LDO_1H columns

    Output:
    - DataFrame with ['timestamp', 'symbol', 'signal', 'position_size']
    """
    try:
            # Merge anchor and target data on timestamp
        df = pd.merge(
        target_df[['timestamp', 'close_SOL_4H']],
        anchor_df[['timestamp', 'close_BTC_1H', 'close_ETH_2H']],
        on='timestamp',
        how='inner'
        ).sort_values('timestamp').reset_index(drop=True)

        # Calculate anchor returns
        df['btc_return_1h'] = df['close_BTC_1H'].pct_change(fill_method=None)
        df['eth_return_2h'] = df['close_ETH_2H'].pct_change(fill_method=None)

        signals = []
        position_sizes = []
        in_position = False
        entry_price = 0

        for i in range(len(df)):
            btc_pump = df['btc_return_1h'].iloc[i] > 0.02 if pd.notna(df['btc_return_1h'].iloc[i]) else False
            eth_pump = df['eth_return_2h'].iloc[i] > 0.02 if pd.notna(df['eth_return_2h'].iloc[i]) else False
            sol_price = df['close_SOL_4H'].iloc[i]

            if not in_position:
                if (btc_pump or eth_pump) and pd.notna(sol_price):
                    signals.append('BUY')
                    position_sizes.append(0.5)
                    in_position = True
                    entry_price = sol_price
                else:
                    signals.append('HOLD')
                    position_sizes.append(0.0)
            else:
                if pd.notna(sol_price) and entry_price > 0:
                    profit_pct = (sol_price - entry_price) / entry_price
                    if profit_pct >= 0.05 or profit_pct <= -0.03:
                        signals.append('SELL')
                        position_sizes.append(0.0)
                        in_position = False
                        entry_price = 0
                    else:
                        signals.append('HOLD')
                        position_sizes.append(0.5)
                else:
                    signals.append('HOLD')
                    position_sizes.append(0.5 if in_position else 0.0)

        result_df = pd.DataFrame({
            'timestamp': df['timestamp'],
            'symbol': 'SOL',
            'signal': signals,
            'position_size': position_sizes
        })
        

        return result_df
    except Exception as e:
        raise RuntimeError(f"Error in generate_signals: {e}")
if __name__ == "__main__":
    df = pd.read_csv('market1_data.csv')
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
    signals.to_csv('signals.csv', index=False)
    print("Signals generated and saved to signals.csv")

