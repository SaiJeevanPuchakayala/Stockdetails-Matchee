# Stockdetails-Matchee
**Stockdetails-Matchee Will help you automatically generate a consolidated list of Instruments**
1. By mapping their ISIN codes to
    1. BSE Stock codes and symbols
    2. NSE symbols
    3. Zerodha symbols
    4. Yahoo symbols (Both .NS and .BO)


# Instructions

## Inputs needed
### You need to download 3 files
1. BSE Bhavcopy: Download from `https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx`. 
2. NSE Bhavcopy: Download from `https://www1.nseindia.com/products/content/equities/equities/archieve_eq.htm`. \
Note: Downloading BHAV Copy using programmatic methods is illegal.
3. Zerodha Instruments: Download from `https://api.kite.trade/instruments`

### Then place these files in the following locations
1. BSE Bhavcopy: `data/marketData/bhavCopies`
2. NSE Bhavcopy: `data/marketData/bhavcopies`\
You need to update the file name in `lib/bin/bhavCopy.py`. \
In future version, this will be more streamlined
3. Zerodha Instruments: `data/marketData/zerodha`. The filename should be instruments.csv

## Running the app
#### On windows
```bash
python app.py
```

#### On linux/MacOS
```bash
python3 ./app.py
```

Or open it in your favourite code editor and run from there. 


