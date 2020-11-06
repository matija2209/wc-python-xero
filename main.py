import requests, re
from woocommerce import API

# Initiate API
wcapi = API(
    url="https://b2b.meetharmony.com/",
    consumer_key="#",
    consumer_secret="#",
    wp_api=True,
    version="wc/v3"
)

def get_order_data(order_id):
    order_data = wcapi.get(f"orders/{order_id}").json()
    customer_id = order_data.get('customer_id')
    items = order_data['line_items']
    
    all_items = list()
    for itm in items:
        dic = {
            'name':itm.get('name'),
            'variation_id':itm.get('variation_id'),
            'subtotal':itm.get('subtotal'),
            'sku':itm.get('sku'),
            'price':itm.get('price')
        }
        all_items.append(dic)
    
    return {
        'customer_id' : customer_id,
        'items' : all_items
    }
    
    
def get_customer_role(customer_id):
    customer_data = wcapi.get(f"customers/{customer_id}").json()
    customer_group = customer_data.get('role')
    return {'customer_group':customer_group}
    
    
    
def tax_adjusted(item_line,customer_group):
    tax_multiplier = 1.21 if re.search(r"rate_21$", customer_group['customer_group']) else 1
    item_line['subtotal'] = float(item_line['subtotal']) * tax_multiplier
    return item_line
    
order_data = get_order_data(781364)
customer_id = order_data.get('customer_id')
customer_group = get_customer_role(customer_id)

apply_tax_calculation = list(map(lambda x: tax_adjusted(x,customer_group), order_data['items']))


"""
subtotal gets multiplied by 1.21 if the customer group ends with "_rate_21" bypassing any tax calculations done by WC
[{'name': 'E-Liquids - OG Kush - Pack of 6 - 600mg',
  'variation_id': 382,
  'subtotal': 135.036,
  'sku': 'HY-OGK-06-60-00',
  'price': 55.8}]"""
