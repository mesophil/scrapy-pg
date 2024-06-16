import pandas as pd
import argparse


def filter(*args):
    pass



if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Filter an existing CSV (must run the scrape first)')
    
    parse.add_argument('--category', '-c', help='Category of the desired item, e.g. bottoms')
    parse.add_argument('--gender', '-g', choices=['male', 'female'], help='Gender of the desired item (male or female)')
    parse.add_argument('--include_material', '-i', help='Include this material in all resulting items, e.g. cotton')
    parse.add_argument('--exclude_material', '-e', help='Exclude this material in all resulting items, e.g. polyester')
    parse.add_argument('--price_low', '-l', help='Minimum price for the resulting items (CAD)')
    parse.add_argument('--price_high', '-h', help='Maximum price for the resulting items (CAD)')
    parse.add_argument('--rating_minimum', '-r', help='Minimum average rating for each resulting item.')
    parse.add_argument('--machine_washable', '-w', help='Machine washable; set to 1 to have all items be machine washable.')
    
    args = parse.parse_args()

    filter(args)