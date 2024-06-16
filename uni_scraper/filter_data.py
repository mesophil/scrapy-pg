import pandas as pd
import argparse


def filter(category, gender, incl_mat, excl_mat, price_min, price_max, rating_min, washable : int):

    filtered_items = pd.read_csv('uniqlo_all_items.csv')

    if category:
        filtered_items = filtered_items[filtered_items['category'].str.casefold() == category.casefold()]

    if gender:
        filtered_items = filtered_items[filtered_items['gender'].str.casefold().isin([gender.casefold(), 'unisex'.casefold()])]

    if incl_mat:
        filtered_items = filtered_items[filtered_items['composition'].str.contains(incl_mat, case=False)]

    if excl_mat:
        filtered_items = filtered_items[not filtered_items['composition'].str.contains(incl_mat, case=False)]

    if price_min:
        filtered_items = filtered_items[float(filtered_items['price']) >= float(price_min)]

    if price_max:
        filtered_items = filtered_items[float(filtered_items['price']) <= float(price_max)]

    if rating_min:
        filtered_items = filtered_items[float(filtered_items['rating']) >= float(rating_min)]

    if washable:
        filtered_items = filtered_items[filtered_items['washing_info'].str.contains('machine wash', case=False)]

    filtered_items.to_csv('filtered_items.csv')
    

if __name__ == '__main__':
    parse = argparse.ArgumentParser(description='Filter an existing CSV (must run the scrape first)')
    
    parse.add_argument('--category', '-c', choices=['tops', 'bottoms', 'accessories', 'loungewear', 'outerwear', 'innerwear', 'dresses'], help='Category of the desired item, e.g. bottoms')
    parse.add_argument('--gender', '-g', choices=['men', 'women'], help='Gender of the desired item (men or women)')
    parse.add_argument('--include-material', '-i', help='Include this material in all resulting items, e.g. cotton')
    parse.add_argument('--exclude-material', '-e', help='Exclude this material in all resulting items, e.g. polyester')
    parse.add_argument('--price-min', '-n', help='Minimum price for the resulting items (CAD)')
    parse.add_argument('--price-max', '-m', help='Maximum price for the resulting items (CAD)')
    parse.add_argument('--rating-min', '-r', help='Minimum average rating for each resulting item (0-5).')
    parse.add_argument('--machine-washable', '-w', choices=['0', '1'], help='Machine washable; set to 1 to have all items be machine washable.')
    
    args = parse.parse_args()

    filter(args.category, args.gender, args.include_material, args.exclude_material, args.price_min, args.price_max, args.rating_min, args.machine_washable)