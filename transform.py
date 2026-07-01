import pandas as pd
from pymongo import MongoClient

def get_customers():
   return pd.read_csv('raw-data/raw_customers.csv')

def clean_customers():
   df = get_customers()
   df = df.drop(columns=['email', 'signup_date', 'loyalty_points', 'phone'])
   df['first_name'] = df['first_name'].str.capitalize()
   df['last_name'] = df['last_name'].str.capitalize()
   df['city'] = df['city'].str.title()
   return df

def get_restaurants():
   return pd.read_csv('raw-data/raw_restaurants.csv')

def clean_restaurants():
   df = get_restaurants()
   df = df.drop(columns=['cuisine', 'address', 'is_open'])
   df = df.dropna(subset=['rating'])
   df['city'] = df['city'].str.title()
   df['rating'] = df['rating'].str[:3].astype(float)
   df['avg_prep_time_mins'] = df['avg_prep_time_mins'].str[:2].astype(int)
   return df 

def get_orders():
   return pd.read_csv('raw-data/raw_orders.csv')

def clean_orders():
   df = get_orders()
   df = df[df['restaurant_id'].isin(clean_restaurants()['restaurant_id'])]   
   df = df.drop(columns=['delivery_fee', 'delivery_time_mins', 'driver_id'])
   df['tip_amount'] = df['tip_amount'].fillna(0.0)
   df['order_amount'] = df['order_amount'].replace(r'[\$]', '', regex=True).astype(float)
   df['order_amount'] = df['order_amount'].abs()
   df['status'] = df['status'].str.lower()
   df['order_date'] = pd.to_datetime(df['order_date'], format='mixed')
   return df

def get_order_items():
   return pd.read_csv('raw-data/raw_order_items.csv')

def clean_order_items():
   df = get_order_items()
   df = df[df['order_id'].isin(clean_orders()['order_id'])]
   df = df.drop(columns=['special_instructions'])
   df = df[df['quantity'] != 0]
   df = df.dropna(subset=['item_price'])
   df['item_name'] = df['item_name'].str.lower()
   df['item_name'] = df['item_name'].str.strip()
   df['quantity'] = df['quantity'].abs()
   df['item_price'] = df['item_price'].replace(r'[\$]', '', regex=True).astype(float)
   return df

def get_drivers():
   return pd.read_csv('raw-data/raw_drivers.csv')

def clean_drivers():
   df = get_drivers()
   df = df.drop(columns=['age', 'vehicle_type'])
   df = df.dropna(subset=['total_deliveries'])
   df['rating'] = df['rating'].fillna(df['rating'].mean().round(2))
   df['rating'] = df['rating'].abs()
   df['is_active'] = df['is_active'].fillna('1')
   df['is_active'] = df['is_active'].map({'1': True, '0': False, 'True': True, 'False': False, 'true': True, 'false': False})
   return df

if __name__ == '__main__':
   customers_df = clean_customers()
   restaurants_df = clean_restaurants()
   orders_df = clean_orders()
   order_items_df = clean_order_items()
   drivers_df = clean_drivers()
   pd.set_option('display.max_rows', None)
   pd.set_option('display.max_columns', None)
   print(customers_df.head())
   print(customers_df.info())
   print(restaurants_df.head())
   print(restaurants_df.info())
   print(orders_df.head())
   print(orders_df.info())
   print(order_items_df.head())
   print(order_items_df.info())
   print(drivers_df.head())
   print(drivers_df.info())
   