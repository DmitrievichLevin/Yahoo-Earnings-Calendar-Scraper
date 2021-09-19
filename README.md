# Yahoo Earnings Calendar Scraper


[![Build Status](https://app.travis-ci.com/DmitrievichLevin/Yahoo-Earnings-Calendar-Scraper.svg?branch=main)](https://app.travis-ci.com/DmitrievichLevin/Yahoo-Earnings-Calendar-Scraper)





## Usage
```python
from earningsCalendarScraper import EarningsScraper

test = EarningsScraper()
print(test.getEarnings('2021-09-21'))
print(test.getEarningsMonth('September 2021'))
```




## Output:
```json
 {
            'date': Date,
            'ticker': Ticker,
            'corp': Name,
            'callTime': Call Time,
            'epsEst': EPS Estimate,
            'repEps': Reported EPS,
            'surPct': Surprise(%)
        }
```

