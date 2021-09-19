import setuptools
 
with open("README.md", "r") as fh:
    long_description = fh.read()
 
setuptools.setup(
    name="yahoo_earnings_calendar_scraper",
    packages=['yahoo_earnings_calendar_scraper'],
    install_requires=[
        'requests',
        'selenium',
        'numpy',
        'pandas',
        'webdriver_manager',
        'chromedriver_binary',
        'beautifulsoup4'
    ],
    version="0.0.1",
    author="DmitrievichLevin",
    author_email="jhowar39@emich.edu",
    description="Scrapes day or whole month from Yahoo Finance earnings calendar.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/DmitrievichLevin/Yahoo-Earnings-Calendar-Scraper',
    keywords=['finance', 'yahoo', 'earnings', 'scrape', 'calendar'],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)