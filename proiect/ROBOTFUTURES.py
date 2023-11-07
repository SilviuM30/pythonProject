import tkinter as tk
from tkinter import Label, Entry, Button
import json
import numpy as np
from binance.client import Client
import time
import subprocess

# Function to save the API keys
def save_keys():
    api_key = api_key_entry.get()
    api_secret = api_secret_entry.get()
    keys = {"api_key": api_key, "api_secret": api_secret}

    with open('api_keys.json', 'w') as f:
        json.dump(keys, f)

    root.quit()  # Close the Tkinter window after saving the keys

# Function to synchronize the PC's clock
def synchronize_clock():
    try:
        subprocess.run(["w32tm", "/resync"])
        print("PC clock synchronized successfully.")
    except Exception as e:
        print("Error synchronizing PC clock:", e)

# Create the Tkinter window
root = tk.Tk()
root.title("Binance API Key Setup")
root.geometry("300x200")

# Create labels and entry fields for API Key and API Secret
api_key_label = Label(root, text="Binance API Key:")
api_key_label.pack()
api_key_entry = Entry(root)
api_key_entry.pack()

api_secret_label = Label(root, text="API Secret Key:")
api_secret_label.pack()
api_secret_entry = Entry(root, show="*")  # The show option hides the entered text
api_secret_entry.pack()

# Create a button to save the keys
save_button = Button(root, text="Save Keys", command=save_keys)
save_button.pack()

# Create a button to synchronize the PC's clock
sync_clock_button = Button(root, text="Sync PC Clock", command=synchronize_clock)
sync_clock_button.pack()

# Start the Tkinter main loop
root.mainloop()


# Load API keys from the JSON file
with open('api_keys.json') as f:
    api_keys = json.load(f)

api_key = api_keys["api_key"]
api_secret = api_keys["api_secret"]
client = Client(api_key, api_secret)

take_profit_target = 10

# CREATE A CLASS FROM STRATEGY


# Define your trading strategy
def trading_strategy():
    symbol = 'SOLUSDT'  # Change to the Solana trading pair
    timeframe = '1h'    # Set your desired timeframe (e.g., 1h for 1-hour candles)

    short_ma_period = 10
    long_ma_period = 50
    rsi_period = 14

    short_ma_values = []
    long_ma_values = []
    rsi_values = []

    current_position = None  # To keep track of the current position

    while True:
        try:
            # Gather historical price data
            klines = client.futures_klines(symbol=symbol, interval=timeframe, limit=100)
            closing_prices = np.array([float(kline[4]) for kline in klines])

            # Calculate Moving Averages
            if len(closing_prices) >= long_ma_period:
                short_ma = np.mean(closing_prices[-short_ma_period:])
                long_ma = np.mean(closing_prices[-long_ma_period:])
                short_ma_values.append(short_ma)
                long_ma_values.append(long_ma)

                if len(short_ma_values) > long_ma_period:
                    short_ma_values.pop(0)
                    long_ma_values.pop(0)

            # Calculate RSI
            if len(closing_prices) >= rsi_period:
                price_changes = np.diff(closing_prices)
                gains = price_changes[price_changes > 0]
                losses = -price_changes[price_changes < 0]

                avg_gain = np.mean(gains[-rsi_period:])
                avg_loss = np.mean(losses[-rsi_period:])
                rs = avg_gain / avg_loss if avg_loss != 0 else 0
                rsi = 100 - (100 / (1 + rs))
                rsi_values.append(rsi)

                if len(rsi_values) > rsi_period:
                    rsi_values.pop(0)

            # Get the most recent values
            current_price = float(klines[-1][4])
            current_short_ma = short_ma_values[-1] if short_ma_values else 0
            current_long_ma = long_ma_values[-1] if long_ma_values else 0
            current_rsi = rsi_values[-1] if rsi_values else 0

            # Check current position
            position_info = client.futures_position_information(symbol=symbol)
            position_side = position_info[0]['positionSide']

            # Define your trading logic based on indicators here
            if current_short_ma > current_long_ma and current_rsi > 30:
                if position_side == 'SHORT':
                    # Close the short position first
                    order = client.futures_create_order(
                        symbol=symbol,
                        side="BUY",
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=1  # Set your desired quantity
                    )
                    print('Closing short position:', order)
                elif position_side != 'LONG':
                    # Place a buy order
                    order = client.futures_create_order(
                        symbol=symbol,
                        side="BUY",
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=1,# Set your desired quantity

                    )
                    print('Buy order executed:', order)
                current_position = 'LONG'
            elif current_short_ma < current_long_ma and current_rsi < 70:
                if position_side == 'LONG':
                    # Close the long position first
                    order = client.futures_create_order(
                        symbol=symbol,
                        side="SELL",
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=1  # Set your desired quantity
                    )
                    print('Closing long position:', order)
                elif position_side != 'SHORT':
                    # Place a sell order
                    order = client.futures_create_order(
                        symbol=symbol,
                        side="SELL",
                        type=Client.ORDER_TYPE_MARKET,
                        quantity=1,  # Set your desired quantity

                    )
                    print('Sell order with take profit executed:', order)
                current_position = 'SHORT'

            # Adjust the sleep duration as needed
            time.sleep(60)  # Sleep for 60 seconds before checking again

        except Exception as e:
            print('An error occurred:', e)

# Run your trading strategy
if __name__ == "__main__":
 trading_strategy()