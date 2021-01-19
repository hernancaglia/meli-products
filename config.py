products = {
    # 'Motorola G6',
    # 'Chromecast',
    # 'Google Home',
    # 'Apple TV'
    # 'Samsung Galaxy Tab',
    # 'Samsung S20',
    'Apple Macbook',
    # 'Microsoft Surface',
    # 'Dell XPS'
    # 'Apple Macbook Air',
    # 'HP Pavilion',
    'Lenovo Ideapad',
    'Dell Vostro'
}

api_search = dict(
    url='https://api.mercadolibre.com/sites/MLA/search?q=',
    search_limit=200
)

api_item = dict(
    url='https://api.mercadolibre.com/items/',
    variables={
        'id',
        'title',
        'seller_id',
        'category_id',
        'official_store_id',
        'price',
        'base_price',
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
        'warranty',
        'tags',
        'catalog_product_id',
        'domain_id',
        'health'
    }
)

api_questions = dict(
    url='https://api.mercadolibre.com/questions/search?item=',
    variables={
        'total'
    }
)

api_users = dict(
    url='https://api.mercadolibre.com/users/',
    variables={
        'nickname',
        'user_type',
        'seller_reputation.level_id',
        'seller_reputation.power_seller_status',
        'seller_reputation.transactions.canceled',
        'seller_reputation.transactions.completed',
        'seller_reputation.transactions.ratings.positive',
        'seller_reputation.transactions.ratings.neutral',
        'seller_reputation.transactions.ratings.negative'
        ''
    }
)

api_products = dict(
    url='https://api.mercadolibre.com/products/',
    variables={
        'domain_id',
        'name'
    }
)

api_reviews = dict(
    url='https://api.mercadolibre.com/reviews/item/',
    variables={
        'paging.total',
        'rating_average',
        'rating_levels.one_star',
        'rating_levels.two_star',
        'rating_levels.three_star',
        'rating_levels.four_star',
        'rating_levels.five_star',
    }
)
