# Ecommerce Scraper

## General Scrapy

1. Start the Python venv:

`pip3 install -r requirements.txt`
`source .venv/bin/activate`

2. Run a spider:

`scrapy crawl XXXXX`

## General Scraping

Production use of these scraping tools can be found on [my personal website](https://mesophil.github.io/scrapy-pg).

I generally update the CSVs once every couple of weeks.

## uni-scraper (manual)

A web scraper designed to shop at uniqlo.

After activating the virtual environment, navigate to `/uni_scraper/`, and run:

`bash scrape.sh`

to scrape all the data from UNIQLO's website. The result is stored in `uniqlo_all_items.csv`.

The data includes:
1.	Category
2.	Composition
3.	Description (cleaned)
4.	Gender
5.	Name
6.	Price (in CAD)
7.	Product ID
8.	Rating (average)
9.	Size chart (specific to the item)
10.	Washing info 

Filter these results through:

`python3 filter_data.py [options]`

type `python3 filter_data.py --help` for more information. The results are shown in an appropriately named `.csv` in the same directory.

To efficiently find the item of interest, search the product ID in Google.

14/06/2024
889 items scraped
327 duplicates across men/women


## uni-scraper (web)

Drop the result CSV from a scrape into `/data`, or use the one that's already there.

Run the web server:

`python3 -m http.server`

Navigate to `http://localhost:8000/`