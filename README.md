# Market Data Utility

### What is Market Data Utility?

It's a simple Python script that:
1. Retrieves the latest two closing data points for six prespecified financial instruments from Yahoo Finance.
2. Calculates the percentage change between those points.
3. Creates a DataFrame, which is then converted to an HTML table.
4. Creates an HTML file which contains the table and a button to download the table as a PNG file.

### How to use it?

You can run the script directly in your favorite IDE (I happen to use PyCharm) to test it in your local environment (given the necessary dependencies are installed), or build it into a standalone executable using `pyinstaller`.

**For the first option**, here is a list of dependencies:
- pandas
- yfinance
- pytz

You can install them via your Terminal using:

`pip3 install {dependency}`

**For the second option**, you can run the command below on your Terminal to get the executable:

`pyinstaller --onefile main.py`

Either way, after you run the script, an HTML file titled `closing_data_table.html` will be created in your current working directory. Simply open it with any browser, and feel free to take a screenshot of the table or download the PNG file directly.

### Caveats

Currently the script will only fully run between 12am-7am Istanbul Time (GMT+3). It is hardcoded to correspond to 5pm-12am Eastern Time. This ensures the latest data is retrieved, after the markets close. If you run the script anytime except these hours, it will terminate before completion with exit code 2.

### Potential bugs and limitations

Apparently, free financial data APIs and/or libraries are not well maintained at all. The `yfinance` library will occasionally fetch & print `NaN` values for some instruments even though data is available on the Yahoo Finance website. I unfortunately don't know how to deal with it, so feel free to make suggestions or offer alternative APIs/libraries to fetch data.

_P.S. I've already tried using Pandas DataReader with both Yahoo and Google Finance as data sources. Both failed. The library is simply outdated, i.e. it does not handle latest changes made to Yahoo's and Google's APIs._

There is another known issue with the data table being converted to a PNG file. I used a JS library called `html2canvas`, which does not take a screenshot per se, but rather traverses the DOM to recreate the elements in it. While CSS styles applied to the table will render perfectly in any browser when you open the HTML file, for some reason `html2canvas` can't get it 100% right, therefore producing a slightly altered representation of the table. Let me know if there's an alternative way to get a pixel-perfect PNG file from an HTML file!
