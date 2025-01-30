# Trade Signal Bot

This project is a Python-based trading signal bot that uses the Fyers API to fetch historical data for symbols, calculate trade signals using the Supertrend indicator, and send notifications for these signals via WhatsApp using Twilio.

## File Structure

```
SCRIPT/
|-- fyers_appid.txt          # Contains the Fyers app ID.
|-- fyers_token.txt          # Contains the Fyers access token.
|-- fyersApi.log             # Log file for Fyers API interactions.
|-- fyersRequests.log        # Log file for Fyers request data.
|-- generateToken.py         # Script for generating a Fyers access token.
|-- last_scalp.json          # Tracks the last scalp signals.
|-- last_signals.json        # Tracks the last signal timestamps.
|-- NiftySymbols.xlsx        # Excel file containing the list of symbols.
|-- Scalp.py                 # Script for scalping strategy.
|-- TestBot.py               # Main script for the trade signal bot.
|-- tp.py                    # Additional script (purpose unspecified).
```

## Dependencies

The following Python libraries are required:

- `pandas`
- `numpy`
- `pandas_ta`
- `twilio`
- `fyers-apiv3`
- `pytz`
- `openpyxl` (for reading Excel files)

Install the dependencies using:

```bash
pip install pandas numpy pandas-ta twilio fyers-apiv3 pytz openpyxl
```

## Configuration

### 1. Fyers API Credentials

- Place your Fyers app ID in `fyers_appid.txt`.
- Place your Fyers access token in `fyers_token.txt`.

### 2. Twilio Credentials

Replace the following placeholders in the `TestBot.py` script with your Twilio account credentials:

```python
account_sid = 'Twilio account id'
auth_token = 'Twilio auth token'
```

Replace the recipient phone number:

```python
to='whatsapp:+91 Phone number'
```

### 3. Symbols List

- Add the symbols you want to monitor in the `NiftySymbols.xlsx` file under a column named `Symbols`.

## How It Works

1. The bot fetches historical data for each symbol from the Fyers API.
2. It calculates the Supertrend indicator and identifies trade signals ("Put Short" or "Call Short").
3. If a new signal is identified, it sends a WhatsApp notification with the signal details.
4. The bot tracks the last signal sent for each symbol to avoid duplicate notifications.

## Key Functions

- **custom_supertrend**: Calculates the Supertrend indicator and generates trade signals.
- **process_symbol**: Processes each symbol to fetch data, calculate signals, and send notifications for new signals.
- **send_whatsapp_message**: Sends WhatsApp messages using Twilio.
- **update_last_signal**: Updates the last signal timestamp for a symbol.

## Running the Bot

Run the bot using:

```bash
python TestBot.py
```

The bot will:
- Process each symbol listed in `NiftySymbols.xlsx`.
- Calculate Supertrend and identify trade signals.
- Send WhatsApp notifications for new signals.

## Logs

- **fyersApi.log**: Logs interactions with the Fyers API.
- **fyersRequests.log**: Logs details of API requests.

## Notes

- Ensure the `fyers_appid.txt`, `fyers_token.txt`, and `NiftySymbols.xlsx` files are correctly configured before running the bot.
- The bot uses a 15-minute interval and fetches data for the past 30 days.
- Modify the WhatsApp sender and recipient details as needed.

## Troubleshooting

- **Error fetching data for a symbol**: Ensure your Fyers credentials are valid and the symbol exists in the Fyers database.
- **No new trade signals triggered**: This means no signal changes have occurred for the symbol during the current session.

