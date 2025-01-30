import pandas as pd

# Load the Excel file
file_path = 'NiftySymbols.xlsx'  # Replace with the path to your Excel file
df = pd.read_excel(file_path)

# List of Nifty 50 symbols (replace this list with actual symbols)
nifty_50_symbols = [
    'RELIANCE', 'TCS', 'HDFCBANK', 'INFY', 'ICICIBANK', 'HINDUNILVR', 'ITC',
    'SBIN', 'KOTAKBANK', 'LT', 'BHARTIARTL', 'HCLTECH', 'ASIANPAINT', 'AXISBANK',
    'MARUTI', 'BAJFINANCE', 'HDFCLIFE', 'SUNPHARMA', 'TITAN', 'WIPRO', 'ADANIENT',
    'ONGC', 'POWERGRID', 'ULTRACEMCO', 'NTPC', 'DIVISLAB', 'JSWSTEEL', 'BPCL',
    'INDUSINDBK', 'TATAMOTORS', 'COALINDIA', 'TATASTEEL', 'GRASIM', 'HEROMOTOCO',
    'BRITANNIA', 'ADANIGREEN', 'TECHM', 'NESTLEIND', 'APOLLOHOSP', 'BAJAJFINSV',
    'CIPLA', 'SBILIFE', 'EICHERMOT', 'TATACONSUM', 'DABUR', 'M&M', 'ICICIPRULI',
    'SHREECEM', 'ADANIPORTS', 'HINDALCO', 'BAJAJ-AUTO'
]

# Create a new column with the formatted symbol
df['Symbols'] = [f'NSE:{symbol}-EQ' for symbol in nifty_50_symbols]

# Save the updated DataFrame to Excel
df.to_excel(file_path, index=False)
print("Column added successfully.")
