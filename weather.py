# Your name: Antony Wu
# Your student id:0439 9524 
# Your email: antonywu@umich.edu
# List who you have worked with on this project: Phillip Ripsam-Walsh 

import sqlite3
import json
import os
import requests
import re

def getJSON(url, api_key):
    '''
    Check whether the 'params' dictionary has been specified. Makes a request to
    access data with
    the 'url' and 'params' given, if any. If the request is successful, return a
    dictionary representation
    of the decoded JSON. If the search is unsuccessful, print out "Exception!" and
    return None.
    Parameters
    ----------
    url (str): a url that provides information about entities in the Star Wars
    universe.
    params (dict): optional dictionary of querystring arguments (default value is
    'None').
    Returns
    -------
    dict: dictionary representation of the decoded JSON.
    '''
    resp = requests.get(url, headers={'X-Api-Key':api_key})
    text = resp.text
    dataDict = json.loads(text)
    return dataDict

def main():
    # Step 1: Retrieve data from API
    
    #Covid DATA
    covidData = getJSON('https://api.api-ninjas.com/v1/covid19?country=US', '/40PGYdxP+G2VAXNvmCxAQ==iYGkUEfixenYSP8N')
    covid_dict = {}
    for date in covidData[0]['cases'].keys():
        #if re.search(str(date), '^2020') == None:
        #    continue
        match = re.search(r'^2020.*', date)
        if not match:
            break
        totalCases = covidData[0]['cases'][date]['total']
        newCases = covidData[0]['cases'][date]['new']
        
        month = re.search(r'-(\d{2})-', date).group(1)
        day = re.search(r'-(\d{2})$',date).group(1)
        date_id = month + day
        covid_dict[int(date_id)] = {'total':totalCases, 'new':newCases}
    #print(covid_dict)
            
    
    # Step 3: Connect to SQLite database
    conn = sqlite3.connect('covid.db')
    c = conn.cursor()
    
    # Step 4: Create table in database
    c.execute('''CREATE TABLE IF NOT EXISTS Covid_Data
                 (date INTEGER PRIMARY KEY, totalCases INTEGER, newCases INTEGER)''')  
    
    for date in covid_dict.keys():
        total = covid_dict[date]['total']
        new = covid_dict[date]['new']
        c.execute(
            "INSERT OR IGNORE INTO Covid_Data (date, totalCases, newCases) VALUES (?,?,?)", (date, total, new))
        conn.commit()

    # Commit changes and close database connection
    
    conn.close() 
    ######################################################################################################################
    #Stock Data
    stockData = getJSON("https://financialmodelingprep.com/api/v3/historical-price-full/AAPL?apikey=5dcc2d9a6fca434722717ec6dcba9e24", "")
    stock_dict = {}
    
    for listdateData in stockData['historical']:
        #if re.search(str(date), '^2020') == None:
        #    continue
        date = listdateData['date']
        match = re.search(r'^2020.*', date)
        if not match:
            continue
        month = re.search(r'-(\d{2})-', date).group(1)
        day = re.search(r'-(\d{2})$',date).group(1)

        date_id = month + day
        closePrice = listdateData['close']
        openPrice = listdateData['open']
        highPrice = listdateData['high']
        lowPrice = listdateData['low']
        changePrice = listdateData['change']
        changePercent = listdateData['changePercent']
        changeOverTime = listdateData['changeOverTime']

        stock_dict[int(date_id)] = {'close':closePrice, 'open':openPrice,'high':highPrice,'low':lowPrice,'change':changePrice,'changePercent':changePercent,'changeOverTime':changeOverTime}
    stock_dict = dict(sorted(stock_dict.items()))

    conn = sqlite3.connect('covid.db')
    c = conn.cursor()
    
    # Step 4: Create table in database
    c.execute('''CREATE TABLE IF NOT EXISTS Stock_Data
                 (date INTEGER PRIMARY KEY, closePrice INTEGER, openPrice INTEGER, highPrice INTEGER, lowPrice INTEGER, changePrice INTEGER, changePercent INTEGER, changeOverTime INTEGER)''')  
    
    for date in stock_dict.keys():
        closePrice = stock_dict[date]['close']
        openPrice = stock_dict[date]['open']
        highPrice = stock_dict[date]['high']
        lowPrice = stock_dict[date]['low']
        changePrice = stock_dict[date]['change']
        changePercent = stock_dict[date]['changePercent']
        changeOverTime = stock_dict[date]['changeOverTime']
        
        c.execute(
            "INSERT OR IGNORE INTO Stock_Data (date, closePrice, openPrice, highPrice, lowPrice, changePrice, changePercent, changeOverTime) VALUES (?,?,?,?,?,?,?,?)", (date, closePrice, openPrice, highPrice, lowPrice, changePrice, changePercent, changeOverTime))
        conn.commit()
    conn.close() 



if __name__ == "__main__":
    main()
