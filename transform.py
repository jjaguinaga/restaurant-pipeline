import pandas as pd
from pymongo import MongoClient

def get_customers():
   return pd.read_csv('raw-data/raw_customers.csv')

def clean_customers():
   df = get_customers()
   df = df.drop(columns=['email', 'signup_date', 'loyalty_points'])
   df['phone'] = df['phone'].fillna('none')
   df['first_name'] = df['first_name'].str.capitalize()
   df['last_name'] = df['last_name'].str.capitalize()
   df['city'] = df['city'].str.title()
   clean = df['phone'].str.replace(r'\D', '', regex=True)
   df['phone'] = clean.str.replace(r'(\d{3})(\d{3})(\d{4})', r'\1-\2-\3', regex=True)   
   return df

def get_drivers():
   return pd.read_csv('raw-data/raw_drivers.csv')

def clean_drivers():
   df = get_drivers()
   df = df.drop(columns=['age'])
   df = df.dropna(subset=['total_deliveries'])
   df['rating'] = df['rating'].fillna(df['rating'].mean().round(2))
   df['rating'] = df['rating'].abs()
   df['is_active'] = df['is_active'].fillna('1')
   df['is_active'] = df['is_active'].map({'1': True, '0': False, 'True': True, 'False': False, 'true': True, 'false': False})
   df['vehicle_type'] = df['vehicle_type'].str.lower()
   return df

def get_order_items():
   return pd.read_csv('raw-data/raw_order_items.csv')

def clean_order_items():
   df = get_order_items()
   df = df.drop(columns=['special_instructions'])
   df = df[df['quantity'] != 0]
   df = df.dropna(subset=['item_price'])
   df['item_name'] = df['item_name'].str.lower()
   df['item_name'] = df['item_name'].str.strip()
   df['quantity'] = df['quantity'].abs()
   df['item_price'] = df['item_price'].replace(r'[\$]', '', regex=True).astype(float)
   return df

def get_orders():
   return pd.read_csv('raw-data/raw_orders.csv')

def clean_orders():
   df = get_orders()
   return df

def get_restaurants():
   return pd.read_csv('raw-data/raw_restaurants.csv')

def clean_restaurants():
   df = get_restaurants()
   return df 

if __name__ == '__main__':
   # customers_df = clean_customers()
   # drivers_df = clean_drivers()
   order_items_df = clean_order_items()
   # orders_df = clean_orders()
   # restaurants_df = clean_restaurants()
   pd.set_option('display.max_rows', None)
   pd.set_option('display.max_columns', None)
   # print(customers_df.head())
   # print(customers_df.info())
   # print(drivers_df.head())
   # print(drivers_df.info())
   print(order_items_df.head())
   print(order_items_df.info())
   # print(orders_df.head())
   # print(orders_df.info())
   # print(restaurants_df.head())
   # print(restaurants_df.info())
   