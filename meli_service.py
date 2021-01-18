import requests
import pandas as pd
import config

OFFSET_PARAM = '&offset='
LIMIT_PARAM = '&limit='
LIMIT_VALUE = '50'


def get_item_ids(search, offset):
    response = requests.get(config.api_search['url'] + search + LIMIT_PARAM + LIMIT_VALUE + OFFSET_PARAM + str(offset)).json()
    try:
        response_data = pd.json_normalize(response, record_path='results')
        item_ids = response_data['id']
    except KeyError:
        item_ids = pd.DataFrame()
    finally:
        return item_ids


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
        if requests.get(config.api_questions['url'] + item_id) is None:
            print('req is none')
        response = requests.get(config.api_questions['url'] + item_id).json()
        response_df = pd.json_normalize(response)
        questions_info = pd.DataFrame()
        questions_info['item_id'] = item_id
        questions_info.set_index('item_id', inplace=True)
        for variable in config.api_questions['variables']:
            variable_name = 'questions_' + variable
            try:
                questions_info.loc[item_id, variable_name] = response_df[variable][0]
            except KeyError:
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
            variable_name = 'user_' + variable
            try:
                user_df.loc[user, variable_name] = response_df[variable][0]
            except KeyError:
                user_df.loc[user, variable_name] = ''
        user_info = user_info.append(user_df)
    return user_info


def get_product_info(product_ids):
    print('Getting products info...')
    product_info = pd.DataFrame()
    for product in product_ids:
        response = requests.get(config.api_products['url'] + str(product)).json()
        response_df = pd.json_normalize(response)
        product_df = pd.DataFrame()
        product_df['product_id'] = product
        product_df.set_index('product_id', inplace=True)
        for variable in config.api_products['variables']:
            variable_name = 'product_' + variable
            try:
                product_df.loc[product, variable_name] = response_df[variable][0]
            except KeyError:
                product_df.loc[product, variable_name] = ''
        product_info = product_info.append(product_df)
    return product_info


def get_reviews_info(items):
    print('Getting reviews info...')
    item_reviews = pd.DataFrame()
    for item in items.iterrows():
        item_id = item[0]
        response = requests.get(config.api_reviews['url'] + item_id).json()
        response_df = pd.json_normalize(response)
        reviews_info = pd.DataFrame()
        reviews_info['item_id'] = item_id
        reviews_info.set_index('item_id', inplace=True)
        for variable in config.api_questions['variables']:
            variable_name = 'reviews_' + variable
            try:
                reviews_info.loc[item_id, variable_name] = response_df[variable][0]
            except KeyError:
                reviews_info.loc[item_id, variable_name] = ''
        item_reviews = item_questions.append(reviews_info)
    return item_reviews
