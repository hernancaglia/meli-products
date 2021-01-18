import requests
import pandas as pd
import config

"""
Mejoras:
Agregar las variables deseadas en los param del endpoint para traer solo esas. Luego se puede sacar el filtro de pd.
Multiget todos los items a la vez? Necesita token.
Hacer requirements.txt
Mover servicios a meli_service
Check blank lines add
try catch en item info?
"""

OFFSET_PARAM = '&offset='
LIMIT_PARAM = '&limit='
LIMIT_VALUE = '50'


def create_search_string(search):
    search_string = search.replace(' ', '%20')
    return search_string


def get_item_ids(search, offset):
    response = requests.get(config.api_search['url'] + search + LIMIT_PARAM + LIMIT_VALUE + OFFSET_PARAM + str(offset)).json()
    try:
        response_data = pd.json_normalize(response, record_path='results')
        item_ids = response_data['id']
    except KeyError:
        item_ids = pd.DataFrame()
    finally:
        return item_ids


def build_items():
    items_df = pd.DataFrame(columns=['product', 'item_id'])
    for product in config.products:
        print('Getting items from ' + product + '...')
        product_string = create_search_string(product)
        offset = 0
        item_count = 0
        product_df = pd.DataFrame(columns=['product', 'item_id'])  # Create DF from this product's items
        while item_count < config.api_search['search_limit']:
            items_id = get_item_ids(search=product_string, offset=offset)
            product_df = product_df.append(pd.DataFrame({'product': product, 'item_id': items_id}), ignore_index=True)
            offset += 50
            item_count += len(items_id)
        items_df = items_df.append(product_df[0:config.api_search['search_limit']], ignore_index=True)  # Add items to DF
    items_df.set_index('item_id', inplace=True)
    return items_df


def get_item_info(items):
    print('Getting items info...')
    items_info_df = pd.DataFrame()
    for item in items.iterrows():
        item_id = item[0]
        response = requests.get(config.api_item['url'] + item_id).json()
        item_info = pd.json_normalize(response)
        item_info = item_info[config.api_item['variables']].set_index('id')
        item_info['item_id'] = item_id
        items_info_df = items_info_df.append(item_info)
    return items_info_df


def get_item_questions(items):
    print('Getting questions info...')
    item_questions = pd.DataFrame()
    for item in items.iterrows():
        item_id = item[0]
        response = requests.get(config.api_questions['url'] + item_id).json()
        response_df = pd.json_normalize(response)
        questions_info = pd.DataFrame()
        questions_info['item_id'] = item_id
        questions_info.set_index('item_id', inplace=True)
        for variable in config.api_questions['variables']:
            variable_name = 'questions_' + variable
            try:
                questions_info.loc[item_id, variable_name] = response_df[variable][0]
            except:
                questions_info.loc[item_id, variable_name] = ''
        item_questions = item_questions.append(questions_info)
    return item_questions


def get_user_info(user_ids):
    print('Getting users info...')
    user_info = pd.DataFrame()
    for user in user_ids:
        response = requests.get(config.api_users['url'] + str(user)).json()
        response_df = pd.json_normalize(response)
        user_df = pd.DataFrame()
        user_df['user_id'] = user
        user_df.set_index('user_id', inplace=True)
        for variable in config.api_users['variables']:
            variable_name = 'users_' + variable
            try:
                user_df.loc[user, variable_name] = response_df[variable][0]
            except:
                user_df.loc[user, variable_name] = ''
        user_info = user_info.append(user_df)
    return user_info


def main():
    items = build_items()
    items.to_csv('1_items.csv', sep=',')

    items_info = get_item_info(items)
    items_info.to_csv('2_items_info.csv', sep=',')

    result = items.merge(items_info, how='left', left_on='item_id', right_on='id', suffixes=[None, '_i'])
    result.to_csv('3_result.csv', sep=',')

    item_questions = get_item_questions(items)
    item_questions.to_csv('4_item_questions.csv', sep=',')

    result = result.merge(item_questions, how='left', left_on='item_id', right_on='item_id', suffixes=[None, '_q'])
    result.to_csv('5_result.csv', sep=',')

    user_info = get_user_info(pd.unique(items_info['seller_id']))
    user_info.to_csv('6_user_info.csv', sep=',')

    result = result.reset_index().merge(user_info, how='left', left_on='seller_id', right_on='user_id', suffixes=[None, '_u'])
    result.to_csv('7_result.csv', sep=',')

if __name__ == '__main__':
    main()
