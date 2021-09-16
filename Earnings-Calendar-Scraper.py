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



pd.options.display.float_format = '{:.0f}'.format

class EarningsScraper:
    def __init__(self, month):
        self.month = datetime.datetime.strptime(month, '%B %Y')
        self.days = self.getMonth(self.month)
        self.offset = 0
        self.offset_step=100
        self.url = 'https://finance.yahoo.com/calendar/earnings'
        self.EarningsMonth = self.getEarningsMonth(self.days)
        



    def formatDate(self, date):
        
        return datetime.datetime.strptime(date, '%b %d %Y %I:%M%p')

    def formatUrl(self, date):

        self.date = date.strftime('%Y-%m-%d')
        date_url = '{0}?day={1}&offset={2}&size{3}'.format(self.url, self.date, self.offset, self.offset_step)
        print("dated_url", date_url)
        return date_url

    def getEarnings(self, date):

        self.thisDateUrl = self.formatUrl(date)

        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(self.thisDateUrl)
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
            EarningsList.append(Earnings(t,u,v,w,x,y))

        print(len(EarningsList))
        self.printEarnings(EarningsList)
        return [date, EarningsList]

    def printEarnings(self, earningsList):

        for x in earningsList:
            print(x.name)

    def getMonth(self, mon):
        year = mon.year

        month = mon.month

        num_days = calendar.monthrange(year, month)[1]

        days = [datetime.date(year, month, day).strftime('%b %d %Y %I:%M%p')for day in range(1, num_days+1)]

        return [datetime.datetime.strptime(x, '%b %d %Y %I:%M%p')for x in days]

    
    def getEarningsMonth(self, days):

        old_stdout = sys.stdout
        log_file = open("message.log", "w")
        sys.stdout = log_file
        print("this will start the log:")
        print(str(days))

        try:
            with concurrent.futures.ProcessPoolExecutor() as executor:

                results = [executor.submit(self.getEarnings, x)for x in days]


                concurrent.futures.wait(results, timeout = None, return_when=concurrent.futures.ALL_COMPLETED)

                return results

        except Exception as e:
            print(e)

        sys.stdout = old_stdout
        log_file.close()


        





class Earnings:

    def __init__(self, ticker, name, callTime, epsEst, repEps, surprisePct):
        self.ticker = ticker
        self.name = name
        self.callTime = callTime
        self.epsEst = epsEst
        self.repEps = repEps
        self.surprisePct = surprisePct

    # def ticker(self):
    #     return self.ticker

    # def name(self):

    #     return self.name

    # def callTime(self):
    #     return self.callTime

    # def epsEst(self):
    #     return self.epsEst

    # def repEps(self):
    #     return self.repEps

    # def surprisePct(self):
    #     return self.surprisePct

if __name__ == '__main__':    
    # extractor = parallelTestModule.ParallelExtractor()
    # extractor.runInParallel(numProcesses=2, numThreads=4)
    test = EarningsScraper('September 2021')

    for x in test.EarningsMonth:
        print(str(x))





    
            
        

   
        
