# scrapy-pg

1. Start the Python venv:

`pip3 install -r requirements.txt`
`source .venv/bin/activate`

2. Run a spider:

`scrapy crawl XXXXX`

## uni-scraper

A web scraper designed to shop at uniqlo.

After activating the virtual enrionment, navigate to `/uni_scraper/`, and run:

`bash scrape.sh`

to scrape all the data from UNIQLO's website. The result is stored in `uniqlo_all_items.csv`.

14/06/2024
889 items scraped
327 duplicates across men/women