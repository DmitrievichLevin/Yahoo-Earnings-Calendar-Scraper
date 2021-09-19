import pandas as pd
from bs4 import BeautifulSoup
import re
from selenium import webdriver
import chromedriver_binary
import string
import numpy as np
from webdriver_manager.chrome import ChromeDriverManager
import datetime, calendar
import multiprocessing
import concurrent.futures
import sys
import requests
import json



pd.options.display.float_format = '{:.0f}'.format

class EarningsScraper(object):
    
    def __init__(self):
        
        self.offset = 0
        self.offset_step=100
        self.url = 'https://finance.yahoo.com/calendar/earnings'
      

    def checkDate(self, date):
        
        format = "%Y-%m-%d"

        try:
            datetime.datetime.strptime(date, format)
        except ValueError:
            print("Incorrect date string format. Should be YYYY-MM-DD.")
            raise

    def checkMonth(self, month):
        
        format = '%B %Y'

        try:
            datetime.datetime.strptime(month, format)
        except ValueError:
            print("Incorrect month string format. Should be Month-YYYY.")
            raise

        
    def formatUrl(self, date):

        date_url = '{0}?day={1}&offset={2}&size{3}'.format(self.url, date, self.offset, self.offset_step)
        print("dated_url", date_url)
        return date_url

    def getEarnings(self, date):
        
        self.checkDate(date)
        thisDateUrl = self.formatUrl(date)
        

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(thisDateUrl)
        html = driver.execute_script('return document.body.innerHTML;')
        soup = BeautifulSoup(html, 'lxml')
        driver.close()

        co_ticker = [entry.text for entry in soup.find_all('a', {
            'class': "Fw(600) C($linkColor)"
        })]
        co_name = [entry.text for entry in soup.find_all('td', {
            'aria-label': "Company"
        })]
        co_callTime = [entry.text for entry in soup.find_all('td', {
            'class': "Va(m) Ta(end) Pstart(15px) W(20%) Fz(s)"
        })]
        co_EpsEst = [entry.text for entry in soup.find_all('td', {
            'aria-label': "EPS Estimate"
        })]
        co_repEps = [entry.text for entry in soup.find_all('td', {
            'aria-label': "Reported EPS"
        })]
        co_surprisePct = [entry.text for entry in soup.find_all('td', {
            'aria-label': "Surprise(%)"
        })]

        EarningsList = []

        for t,u,v,w,x,y in zip(co_ticker, co_name, co_callTime, co_EpsEst, co_repEps, co_surprisePct):
            print("going through", t,u,v,w,x,y)
            EarningsList.append(Earnings(t,u,v,w,x,y,date))
        print(len(EarningsList))
        
        return [(x.js)for x in EarningsList] 

    def getMonth(self, mon):
        
        mon = datetime.datetime.strptime(mon, '%B %Y')
        
        year = mon.year

        month = mon.month

        num_days = calendar.monthrange(year, month)[1]

        
        return [datetime.datetime(year, month, x, 0, 0).strftime('%Y-%m-%d')for x in range(1, num_days+1)]

    
    def getEarningsMonth(self, monthYear):


        self.checkMonth(monthYear)

        days = self.getMonth(monthYear)
        

        try:
            with concurrent.futures.ProcessPoolExecutor() as executor:

                results = [executor.submit(self.getEarnings, x)for x in days]


                concurrent.futures.wait(results, timeout = None, return_when=concurrent.futures.ALL_COMPLETED)

                return [(x.result()) for x in results]

        except Exception as e:
            print(e)

        


        





class Earnings:

    def __init__(self, ticker, name, callTime, epsEst, repEps, surprisePct, date):
        self.date = date
        self.ticker = ticker
        self.name = name
        self.callTime = callTime
        self.epsEst = epsEst
        self.repEps = repEps
        self.surprisePct = surprisePct
        self.id=id
        self.js = {

            'date': self.date,
            'ticker': self.ticker,
            'corp': self.name,
            'callTime': self.callTime,
            'epsEst': self.epsEst,
            'repEps': self.repEps,
            'surPct': self.surprisePct

        }

    

if __name__ == '__main__':    
    
    test = EarningsScraper()
    print(test.getEarnings('2021-09-21'))
    print(test.getEarningsMonth('September 2021'))
    





    
            
        

   
        
