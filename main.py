import requests
import pandas as pd
import config

OFFSET_PARAM = '&offset='
LIMIT_PARAM = '&limit='
LIMIT_VALUE = '50'


def create_search_string(search):
    search_string = search.replace(' ', '%20')
    return search_string


def get_item_ids(search, offset):
    response = requests.get(config.API_SEARCH + search + LIMIT_PARAM + LIMIT_VALUE + OFFSET_PARAM + str(offset)).json()
    try:
        response_data = pd.json_normalize(response, record_path='results')
        item_ids = response_data['id']
    except KeyError:
        item_ids = pd.DataFrame()
    finally:
        return item_ids


def build_items():
    items_df = pd.DataFrame(columns=['product', 'item_id'])
    for product in config.PRODUCTS:
        product_string = create_search_string(product)
        offset = 0
        item_count = 0
        product_df = pd.DataFrame(columns=['product', 'item_id'])  # Create DF from this product's items
        while item_count < config.SEARCH_LIMIT:
            items_id = get_item_ids(search=product_string, offset=offset)
            product_df = product_df.append(pd.DataFrame({'product': product, 'item_id': items_id}), ignore_index=True)
            offset += 50
            item_count += len(items_id)
        items_df = items_df.append(product_df[0:config.SEARCH_LIMIT], ignore_index=True)  # Add items to DF
    items_df.set_index('item_id', inplace=True)
    return items_df


def get_item_info(items):
    items_info_df = pd.DataFrame()
    for item in items.iterrows():
        item_id = item[0]
        response = requests.get(config.API_ITEM + item_id).json()
        item_info = pd.json_normalize(response, meta=['seller_address', 'country', 'name'])
        item_info = item_info[['id',
                               'seller_id',
                               'category_id',
                               'official_store_id',
                               'price', 'base_price',
                               'original_price',
                               'initial_quantity',
                               'available_quantity',
                               'sold_quantity',
                               'buying_mode',
                               'listing_type_id',
                               'start_time',
                               'condition',
                               'accepts_mercadopago',
                               'seller_address.country.name',
                               'seller_address.state.name',
                               'status',
                               'tags',
                               'warranty',
                               'catalog_product_id',
                               'domain_id',
                               'health'
                               ]].set_index('id')
        item_info['item_id'] = item_id
        items_info_df = items_info_df.append(item_info)
    return items_info_df


def main():
    items = build_items()
    items_info = get_item_info(items)
    result = items.merge(items_info, how='left', left_on='item_id', right_on='id', suffixes=[None, '_i'])
    result.to_csv('result.csv', sep=',')



if __name__ == '__main__':
    main()
