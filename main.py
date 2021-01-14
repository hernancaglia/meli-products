import requests
import pandas as pd

PRODUCTS = ['motorola g6', 'chromecast']


def get_item_ids(search):
    response = requests.get("https://api.mercadolibre.com/sites/MLA/search?q=Motorola%20G6").json()
    response_data = pd.json_normalize(response, record_path='results')
    # response_data.to_csv('response_data.csv', sep=';')
    item_ids = response_data['id']
    return item_ids


def main():
    item_ids = get_item_ids(search=PRODUCTS[0])
    print(type(item_ids))


if __name__ == '__main__':
    main()
