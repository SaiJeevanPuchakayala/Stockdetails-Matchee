import sys
from termcolor import colored
from lib.screen.screenManager import ScreenManager
from lib.bin.bhavCopy import bhavUpdate
from lib.bin.yahoo import yahooDataManager
from selenium import webdriver
import time
import os
import zipfile
from datetime import date
import datetime


# Getting todays date
today = date.today()

# All Week dates of present Week
week_day=datetime.datetime.now().isocalendar()[2]
start_date=datetime.datetime.now() - datetime.timedelta(days=week_day)
week_dates=[str((start_date + datetime.timedelta(days=i)).date().strftime("%d"+"-"+"%m"+"-"+"%Y")) for i in range(7)]


# Selenium Driver Configurations
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
current_directory = os.getcwd()
prefs = {"download.default_directory" : current_directory}
chrome_options.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(executable_path=r"chromedriver.exe", options=chrome_options)


# Downloading BSE Bhavcopy
driver.get("https://www.bseindia.com/markets/MarketInfo/BhavCopy.aspx")
html = driver.page_source
link = driver.find_element_by_partial_link_text("Equity with ISIN")
link.click()


# Downlaoding NSE Bhavcopy
for date in week_dates[::-1]:
    NSE_BHAV_URL = f"https://www1.nseindia.com/ArchieveSearch?h_filetype=eqbhav&date={date}&section=EQ"
    driver.get(NSE_BHAV_URL)
    html = driver.page_source
    zip_file_tag = driver.find_element_by_tag_name("tr")
    if zip_file_tag.text != "No file found for specified date. Try another date.":
        link = driver.find_element_by_tag_name("a")
        link.click()
        break


# Dowloading Zerodha Bhavcopy
driver.get("https://api.kite.trade/instruments")


time.sleep(10)


# Making list of Zip files to extract
my_list = os.listdir(current_directory)
zip_files = []
for f in my_list:
    if ".zip" in f:
        zip_files.append(f)


# Extracting Zip files
for file in zip_files:
    with zipfile.ZipFile(file,"r") as zip_ref:
        zip_ref.extractall(current_directory)


# Deleting Zip files after extraction
for file in zip_files:
    os.remove(file)


time.sleep(10)


# Adding BSE and NSE tags to corresponding Bhavcopies
csv_list = os.listdir(current_directory)
for f in csv_list:
    if ".csv" in f.lower():
        if "eq" in f.lower():
            base = os.path.splitext(f)[0]
            os.rename(f,"BSE-"+ base + '.csv')

        if "cm" in f:
            base = os.path.splitext(f)[0]
            os.rename(f,"NSE-"+ base + '.csv')


# Converting zerodha Instruments file to instruments.csv
zerodha_file = 'instruments'
base = os.path.splitext(zerodha_file)[0]
os.rename(zerodha_file, base + '.csv')


# Accessing Data folders to place Bhavcopies
data_folder_path = ".\data\marketData"
bhavCopies_folder_path = data_folder_path+ "/bhavCopies/"
zerodha_folder_path = data_folder_path+"\zerodha/"
old_files_bhavfolder = os.listdir(bhavCopies_folder_path)
old_files_zerodhafolder = os.listdir(zerodha_folder_path)


# Removing Old files in bhavCopies folder
for f in old_files_bhavfolder:
    if ".csv" in f.lower():
        os.remove(bhavCopies_folder_path+f)

# Removing Old files in Zerodha folder
for f in old_files_zerodhafolder:
    if "instruments.csv" in f:
        os.remove(zerodha_folder_path+f)

# Moving bhavcopies and instruments file to bhavCopies folder
current_directory_files = os.listdir(current_directory)
nse_bse_files = []
for f in current_directory_files:
    if "NSE" in f:
        os.rename(f, bhavCopies_folder_path+f)
    
    if "BSE" in f:
        os.rename(f, bhavCopies_folder_path+f)

    if "instruments" in f:
        os.rename(f,zerodha_folder_path+f)


time.sleep(10)

# Runnig the NSE , BSE, and instruments matching function
bhavUpdate()
