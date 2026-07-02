import pandas as pd
import psycopg2
from transform import clean_customers, clean_drivers, clean_order_items, clean_orders, clean_restaurants

def load_data():
   customers = clean_customers()
   restaurants = clean_restaurants()
   orders = clean_orders()
   order_items = clean_order_items()
   drivers = clean_drivers()
   
   conn = psycopg2.connect(dbname='restaurants', user='naga', host='localhost')
   cur = conn.cursor()
   
   cur.execute('DROP TABLE IF EXISTS customers CASCADE;')
   cur.execute('DROP TABLE IF EXISTS restaurants CASCADE;')
   cur.execute('DROP TABLE IF EXISTS orders CASCADE;')
   cur.execute('DROP TABLE IF EXISTS order_items CASCADE;')
   cur.execute('DROP TABLE IF EXISTS drivers CASCADE;')
   
   cur.execute('''
               CREATE TABLE customers (
                  customer_id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  city TEXT
               )''')
   
   for _, row in customers.iterrows():
      cur.execute(
         'INSERT INTO customers VALUES (%s, %s, %s, %s)',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE restaurants (
                  restaurant_id INTEGER PRIMARY KEY,
                  restaurant_name TEXT,
                  cuisine TEXT,
                  city TEXT,
                  rating FLOAT,
                  avg_prep_time_mins INTEGER
               )''')
               
   for _, row in restaurants.iterrows():
      cur.execute(
         'INSERT INTO restaurants VALUES (%s, %s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE orders (
                  order_id INTEGER PRIMARY KEY,
                  customer_id INTEGER REFERENCES customers(customer_id),
                  restaurant_id INTEGER REFERENCES restaurants(restaurant_id),
                  order_date DATE,
                  status TEXT,
                  order_amount FLOAT,
                  tip_amount FLOAT
               )''')
   
   for _, row in orders.iterrows():
      cur.execute(
         'INSERT INTO orders VALUES (%s, %s, %s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE order_items (
                  item_id INTEGER PRIMARY KEY,
                  order_id INTEGER REFERENCES orders(order_id),
                  item_name TEXT,
                  quantity INTEGER,
                  item_price FLOAT
               )''')
   
   for _, row in order_items.iterrows():
      cur.execute(
         'INSERT INTO order_items VALUES (%s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   cur.execute('''
               CREATE TABLE drivers (
                  driver_id INTEGER PRIMARY KEY,
                  first_name TEXT,
                  last_name TEXT,
                  rating FLOAT,
                  total_deliveries INTEGER,
                  is_active BOOLEAN
               )''')
   
   for _, row in drivers.iterrows():
      cur.execute(
         'INSERT INTO drivers VALUES (%s, %s, %s, %s, %s, %s)',
         tuple(row)
      )
      
   conn.commit()
   cur.close()
   conn.close()
   
if __name__ == '__main__':
   load_data()
   print('Data loaded!')
   