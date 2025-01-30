import pandas as pd
from numpy import nan as npNaN
from pandas_ta.overlap import hl2
from pandas_ta.volatility import atr
from pandas_ta.utils import verify_series
from datetime import datetime, timedelta
from twilio.rest import Client
from fyers_apiv3 import fyersModel
import pytz

import json
import os

# Load last sent signals timestamps
signals_file = "last_scalp.json"
if os.path.exists(signals_file):
    with open(signals_file, 'r') as f:
        last_signals = json.load(f)
else:
    last_signals = {}

# Function to update and save the last signal timestamp for a symbol
def update_last_signal(symbol, signal_date):
    last_signals[symbol] = signal_date
    with open(signals_file, 'w') as f:
        json.dump(last_signals, f)

# Read app_id and access_token from files
app_id = open("fyers_appid.txt", 'r').read().strip()
access_token = open("fyers_token.txt", 'r').read().strip()

# Initialize the fyersModel instance
fyers = fyersModel.FyersModel(client_id=app_id, token=access_token)

# Set interval and date range
interval = "15"  # 15 min interval
to_date = int(datetime.now().timestamp())
start_date = int((datetime.now() - timedelta(days=30)).timestamp())

# Load symbols from Excel file
excel_path = "NiftySymbols.xlsx"  # Replace with the path to your Excel file
df_symbols = pd.read_excel(excel_path)
symbols = df_symbols['Symbols'].tolist()  # Adjust the column name if different

# Twilio credentials
account_sid = 'Twilio account id'
auth_token = 'Twilio  auth token'
client = Client(account_sid, auth_token)

# Function to send a WhatsApp message
def send_whatsapp_message(message_body):
    try:
        message = client.messages.create(
            from_='whatsapp:+14155238886',  # Your Twilio WhatsApp sandbox number
            body=message_body,
            to='whatsapp:+91 Your phone number'  # Recipient's WhatsApp number
        )
        print(f"Message sent successfully: {message.sid}")
    except Exception as e:
        print(f"Failed to send message: {str(e)}")

# Supertrend function with trade signals
def custom_supertrend(high, low, close, length=10, multiplier=3.0):
    high, low, close = map(lambda x: verify_series(x, length), [high, low, close])
    if high is None or low is None or close is None:
        return None
    
    hl2_ = hl2(high, low)
    matr = multiplier * atr(high, low, close, length)
    upperband, lowerband = hl2_ + matr, hl2_ - matr

    m = len(close)
    direction, supertrend, signals = [1] * m, [0] * m, [npNaN] * m

    for i in range(1, m):
        if close.iloc[i] > upperband.iloc[i - 1]:
            direction[i] = 1
        elif close.iloc[i] < lowerband.iloc[i - 1]:
            direction[i] = -1
        else:
            direction[i] = direction[i - 1]
            if direction[i] == 1 and lowerband.iloc[i] < lowerband.iloc[i - 1]:
                lowerband.iloc[i] = lowerband.iloc[i - 1]
            if direction[i] == -1 and upperband.iloc[i] > upperband.iloc[i - 1]:
                upperband.iloc[i] = upperband.iloc[i - 1]

        supertrend[i] = lowerband.iloc[i] if direction[i] == 1 else upperband.iloc[i]

        if direction[i] == 1 and direction[i - 1] == -1:
            signals[i] = "Put Short"
        elif direction[i] == -1 and direction[i - 1] == 1:
            signals[i] = "Call Short"

    return pd.DataFrame({'Supertrend': supertrend, 'Direction': direction, 'Signal': signals}, index=close.index)

# Process each symbol and check for signals
def process_symbol(symbol):
    data = {
        "symbol": symbol,
        "resolution": interval,
        "date_format": "0",
        "range_from": start_date,
        "range_to": to_date,
        "cont_flag": "1"
    }
    
    response = fyers.history(data)
    if response["s"] == "ok":
        historical_data = response["candles"]
        df = pd.DataFrame(historical_data, columns=["timestamp", "open", "high", "low", "close", "volume"])

        # Convert timestamps to readable dates
        df["date"] = pd.to_datetime(df["timestamp"], unit='s', utc=True).dt.tz_convert('Asia/Kolkata')
        df["date"] = df["date"].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.drop("timestamp", axis=1, inplace=True)
        df = df.sort_values(by="date", ascending=True).reset_index(drop=True)
        
        # Calculate Supertrend and get signals
        supertrend_result = custom_supertrend(df["high"], df["low"], df["close"], length=7, multiplier=3.0)
        supertrend_result.index = df.index
        df = pd.concat([df, supertrend_result], axis=1)
        
        # Identify signal changes
        df['Signal_Change'] = df['Signal'] != df['Signal'].shift(1)
        signal_change_df = df[df['Signal_Change']].dropna(subset=['Signal'])
        
        # Filter signals for today
        today_date = datetime.now().date()
        today_signals = signal_change_df[pd.to_datetime(signal_change_df['date']).dt.date == today_date]
        
        # Check for new signals only
        new_signals = today_signals[
            today_signals['date'] > last_signals.get(symbol, "1970-01-01 00:00:00")
        ]
        
        # Send WhatsApp message for each new signal
        if not new_signals.empty:
            for index, row in new_signals.iterrows():
                message_body = (
                    f"Trade Signal: {row['Signal']} on *{symbol}* "
                    f"@{row['close']}\n{row['date']}"
                )
                send_whatsapp_message(message_body)
                
                # Update the last signal timestamp
                update_last_signal(symbol, row['date'])
        else:
            print(f"No new trade signals triggered for {symbol}.")
            
    else:
        print(f"Error fetching data for {symbol}: {response}")

# Loop over each symbol in the list and process it
for symbol in symbols:
    process_symbol(symbol)