import argparse

def read_urls(file_name='uni_scraper/urls.txt'):
    urls = []

    # base_url = 'https://www.uniqlo.com/ca/api/commerce/v3/en/products?path=%2C%2C'
    base_url = 'https://www.uniqlo.com/ca/api/commerce/v3/en/products?path='
    num_items = '&limit=350'

    with open(file_name, 'r') as file:
        for url in file:
            urls.append("".join([base_url, url.rstrip(), num_items]))
            # add break if testing
            
    return urls


if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Read the 5 digit identifiers from a file to make uniqlo API endpoints')
    parse.add_argument('filename')

    args = parse.parse_args()

    print(read_urls(args.filename))