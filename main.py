# Step 1: Import the necessary libraries
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta
import pytz
import os
import sys

# Step 2: Define the ticker symbols and corresponding full names
ticker_symbols = {'XU100.IS': 'BIST 100', '^GSPC': 'S&P 500', '^STOXX': 'Euro Stoxx 600', 'USDTRY=X': 'USD/TRY', 'EURTRY=X': 'EUR/TRY', 'GC=F': 'Altın (ons)'}

# Step 3: Get the financial data
# Get the current time in GMT+3 timezone
local_timezone = pytz.timezone('Europe/Istanbul')
current_time = datetime.now(local_timezone).time()

# Calculate the current Eastern Time by subtracting 7 hours
et_timezone = pytz.timezone('US/Eastern')
et_current_time = (datetime.combine(datetime.today(), current_time) - timedelta(hours=7)).time()

# Determine the date range based on the current Eastern Time
if datetime.strptime('17:00:00', '%H:%M:%S').time() <= et_current_time <= datetime.strptime('23:59:59', '%H:%M:%S').time():
    # Fetch the closing price data for the current day in Eastern Time and the previous day in Eastern Time
    data = yf.download(list(ticker_symbols.keys()), period='2d')

else:
    print("Please run the program between 00:00 and 07:00 Istanbul time to get the latest data.")
    sys.exit(2)

# Filter the data to keep only the 'Close' column
data = data['Close']

# Set the Pandas display options to show all rows and columns without truncation
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

# Print the raw data table for debugging
print("Raw Data Table:")
print(data)

# Perform calculations on the raw data
if len(data) < 2:
    print("Insufficient data to calculate percent change.")
else:
    latest_closing_data = data.iloc[-1]
    previous_closing_data = data.iloc[-2]
    percent_change = ((latest_closing_data - previous_closing_data) / previous_closing_data) * 100
    closing_prices = [round(latest_closing_data[ticker], 2) for ticker in ticker_symbols.keys()]

    # Create a list of tickers in the order specified in the ticker_symbols dictionary
    tickers_ordered = list(ticker_symbols.keys())

    # Reindex the DataFrame to match the order of tickers in the ticker_symbols dictionary
    closing_data_df = pd.DataFrame({
        'Ticker': list(ticker_symbols.values()),
        'Last Close': closing_prices,
        'Trend': [
            f'<span class="positive-change">▲</span>' if x >= 0 else f'<span class="negative-change">▼</span>'
            for x in percent_change
        ],
        'Percent Symbol': [
            f'<span class="positive-change">%</span>' if x >= 0 else f'<span class="negative-change">%</span>'
            for x in percent_change
        ],
        'Percent Change': [
            f'<span class="positive-change">{format(abs(x), ".2f")}</span>' if x >= 0 else f'<span class="negative-change">{format(abs(x), ".2f")}</span>'
            for x in percent_change
        ]
    }).reindex(tickers_ordered)

    # Convert the DataFrame to an HTML table without index and header row
    table_html = closing_data_df.to_html(index=False, header=False, escape=False, classes=['styled-table'])

    # Generate the HTML file
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans&display=swap');

            .styled-table {{
                font-family: 'IBM Plex Sans', Arial, sans-serif;
                font-size: 17pt;
                background-color: #fafbfc;
                border-collapse: collapse;
                border-style: hidden;
            }}

            .styled-table td {{
                padding-top: 6px;
                padding-bottom: 6px;
                padding-left: 20px;
                padding-right: 20px;
                text-align: center;
                border-collapse: collapse;
            }}

            .styled-table td:first-child {{
                border-top: 0px solid #e5e5e5;
                border-bottom: 1px solid #e5e5e5;
                border-left: 0px solid #e5e5e5;
                border-right: 1px solid #e5e5e5;
                text-align: left;
            }}

            .styled-table td:nth-child(2) {{
                border-top: 0px solid #e5e5e5;
                border-bottom: 1px solid #e5e5e5;
                border-left: 0px solid #e5e5e5;
                border-right: 0px solid #e5e5e5;
                text-align: right;
            }}

            .styled-table td:nth-child(3) {{
                border-top: 0px solid #e5e5e5;
                border-bottom: 1px solid #e5e5e5;
                border-left: 0px solid #e5e5e5;
                border-right: 0px solid #e5e5e5;
                font-size: 19pt;
            }}
            
            .styled-table td:nth-child(4) {{
                border-top: 0px solid #e5e5e5;
                border-bottom: 1px solid #e5e5e5;
                border-left: 0px solid #e5e5e5;
                border-right: 0px solid #e5e5e5;
                text-align: left;
                padding-right: 4px;
            }}

            .styled-table td:nth-child(5) {{
                border-top: 0px solid #e5e5e5;
                border-bottom: 1px solid #e5e5e5;
                border-left: 0px solid #e5e5e5;
                border-right: 0px solid #e5e5e5;
                text-align: left;
                padding-left: 4px;
            }}

            .styled-table-container {{
                border-top: 1px solid #e5e5e5;
                border-bottom: 0.01px solid #e5e5e5;
                border-left: 1px solid #e5e5e5;
                border-right: 1px solid #e5e5e5;
                border-radius: 16px;
                border-collapse: collapse;
                box-shadow: 0 4px 4px 0 rgba(0, 0, 0, 0.08);
                overflow: hidden;
                display: inline-block;
            }}

            .positive-change {{
                color: #00ca1b;
            }}

            .negative-change {{
                color: #ff0000;
            }}
        </style>
    </head>
    <body>
    <div class="styled-table-container">
        <table class="styled-table">
            {table_html}
        </table>
    </div>
    <button class="download-button" onclick="downloadTableAsPNG()">Download as PNG</button>
    <script src="https://html2canvas.hertzen.com/dist/html2canvas.min.js"></script>
    <script>
        function downloadTableAsPNG() {{
            const table = document.querySelector('.styled-table');
            const tableContainer = document.querySelector('.styled-table-container');

            html2canvas(tableContainer, {{backgroundColor: null}}).then(function (canvas) {{
                const image = canvas.toDataURL('image/png');
                const link = document.createElement('a');
                link.href = image;
                link.download = 'closing_data_table.png';
                link.click();
            }});
        }}
    </script>
    </body>
    </html>
    """

    # Save the HTML content to a file
    file_name = 'closing_data_table.html'
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"HTML file '{file_name}' generated successfully in the current directory.")
