def read_urls(file_name):
    urls = []

    with open(file_name, 'r') as file:
        for url in file:
            urls.append(url.rstrip())
    return urls

urls = ['https://www.uniqlo.com/ca/en/men/bottoms/bottoms-collections',
        # 'https://www.uniqlo.com/ca/en/men/tops/tops-collections',
        # 'https://www.uniqlo.com/ca/en/men/accessories-and-home/accessories-collections',
        # 'https://www.uniqlo.com/ca/en/men/outerwear/outerwear-collections',
        ]