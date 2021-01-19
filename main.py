import pandas as pd
import config
import meli_service as meli

"""
Could do:
Add desired variables to api's params so it only requests those. Then remove pandas filtering.
Change limit param to search only up to search_limit
Refactor get_items_info so it only takes item_ids list instead of df
Try catch in get_items_info?
Refactor nested fors in meli service?
"""


def create_search_string(search):
    search_string = search.replace(' ', '%20')
    return search_string


def build_items():

    items_df = pd.DataFrame(columns=['product', 'item_id'])

    for product in config.products:
        print('Getting items from ' + product + '...')
        product_string = create_search_string(product)
        offset = 0
        item_count = 0
        product_df = pd.DataFrame(columns=['product', 'item_id'])  # Create DF from this product's items

        while item_count < config.api_search['search_limit']:
            items_id = meli.get_item_ids(search=product_string, offset=offset)
            try:
                product_df = product_df.append(pd.DataFrame({'product': product, 'item_id': items_id}), ignore_index=True)
            except ValueError:
                break
            finally:
                item_count += len(items_id)
            offset += 50
            print(str(offset))

        print(str(item_count) + ' items found for ' + product)
        items_df = items_df.append(product_df[0:config.api_search['search_limit']], ignore_index=True)  # Add items to DF
    items_df.set_index('item_id', inplace=True)

    return items_df


def main():
    # Get items from each of the searches
    items = build_items()

    # Get items data
    items_info = meli.get_item_info(items)
    result = items.merge(items_info, how='left', left_on='item_id', right_on='id', suffixes=[None, '_i'])

    # Get data from the items' questions
    item_questions = meli.get_item_questions(items)
    result = result.merge(item_questions, how='left', left_on='item_id', right_on='item_id', suffixes=[None, '_q'])

    # Get data from the item's seller
    user_info = meli.get_user_info(pd.unique(items_info['seller_id']))
    result = result.reset_index().merge(user_info, how='left', left_on='seller_id', right_on='user_id', suffixes=[None, '_u'])

    # Get data from the item's product
    product_info = meli.get_product_info(pd.unique(items_info['catalog_product_id']))
    result = result.merge(product_info, how='left', left_on='catalog_product_id', right_on='product_id', suffixes=[None, '_p'])

    result.to_csv('rev.csv', sep=',')


if __name__ == '__main__':
    main()
