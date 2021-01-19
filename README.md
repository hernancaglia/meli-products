# meli-products

Obtains data from the items that appear when searching mercadolibre.com.ar and stores it in meli_data.csv.

## Installation

Install Python 3.8.

Install dependencies: *pip install -r requirements.txt*, or *conda install --file requirements.txt* if using Conda. Otherwise, just install Pandas 1.2.0 and Requests 2.25.1.
Instalar las dependencias con *pip install -r requirements.txt*.

## How to use

Modify config.py as desired:
* products: Search terms to look for.
* api_search: Search limit is the amount of items per search. I recommend 50 for a quick processing and 200 for deeper analysis.
* api variables: Items' attributes to include. Add and remove as desired.


## How it works

The program connects to Mercadolibre's API (developers.mercadolibre.com.ar) and gets data from the following endpoints:
* Sites: Gets items from each specified search - api.mercadolibre.com/sites
* Items: Data from each item - api.mercadolibre.com/items
* Questions: Questions asked in each item - api.mercadolibre.com/questions
* Users: Data from the item's seller - api.mercadolibre.com/users
* Products: Data from the item's product - api.mercadolibre.com/products

