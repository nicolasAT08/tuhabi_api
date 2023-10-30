import pytest
import pandas as pd
from IPython. display import display
import json
from typing import Optional, List
from mysql.connector import connect, errorcode, Error
import os
from dotenv import load_dotenv
load_dotenv()

# Set environment variables
class Settings(object):
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    user = os.environ.get("USER")
    passwordd = os.environ.get("PASSWORD")
    database = os.environ.get("DATABASE")


    class Config:
        env_file = '.env'

settings = Settings()

# Database credentials
config = {
    'host': settings.host,
    'port': settings.port,
    'user': settings.user,
    'password': settings.passwordd,
    'database': settings.database
}

def connect_db():
  try:
      cnn = connect(**config)
      cur = cnn.cursor()
      print('Connection successful!')
      return cnn, cur
  except Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
      print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
      print("Database does not exist")
    else:
      print(err)
  else:
    cnn.close()

cnn, cur = connect_db()

# Database tables schemas
auth_table = 'habi_db.auth_user'
status_table = 'habi_db.status'
status_history_table = 'habi_db.status_history'
property_table = 'habi_db.property'

# User request
with open('api/user_request.json') as f:
   user_request = json.load(f)

def login(cur, user, pwd): 
    query = f"""
            SELECT * FROM {auth_table} au
            WHERE au.username = '{user}'
            AND au.password = '{pwd}'
            AND au.is_staff = 1
            AND au.is_active = 1
            OR au.is_superuser = 1;
            """

    cur.execute(query)
    user = cur.fetchone()

    if not user:
        raise Exception('Invalid credentials')

    access = True

    return access

def for_sale_properties(cur, user, pwd,
                        city_filter: Optional[List[str]] = f'SELECT DISTINCT(p.city) FROM {property_table} AS p',
                        year_filter: Optional[List[int]] = f'SELECT DISTINCT(p.year) FROM {property_table} as p'):
    
    try:
        if login(cur, user,pwd):
            # Columns allowed to see by users
            allowed_status = ('pre_venta', 'en_venta', 'vendido')
            
            # Query result columns
            response_cols = ['ID','Address', 'City', 'Status', 'Price', 'Description']

            # Format filters
            if isinstance(city_filter,list):
                city_filter = ','.join([i for i in city_filter])
            else:
                pass

            if isinstance(year_filter,list):
                year_filter = ','.join([str(i) for i in year_filter])
            else:
                pass

            print(city_filter)    

            query = f"""
                    SELECT p.id, p.address, p.city, s.name, p.price, p.description
                    FROM {property_table} AS p LEFT JOIN {status_history_table} sh ON p.id = sh.property_id
                                                LEFT JOIN {status_table} s ON s.id = sh.status_id
                    WHERE s.name IN {allowed_status}
                    AND p.city IN ('{city_filter}')
                    AND p.year IN ({year_filter})
                    AND sh.update_date IN (SELECT t.date_max FROM (SELECT p.id AS id_max, sh.status_id, MAX(sh.update_date) AS date_max
                                                        FROM {property_table} p INNER JOIN {status_history_table} sh
                                                        ON p.id = sh.property_id
                                                        GROUP BY 1) t);
                    """

            cur.execute(query)
            data = cur.fetchall()

            # Create and print final response to the user.
            df = pd.DataFrame(data, columns=response_cols)
            df['Address'].fillna('-', inplace=True)
            df['City'].fillna('-', inplace=True)
            df['Status'].fillna('-', inplace=True)
            df['Price'].fillna('0', inplace=True)
            df['Description'].fillna('-', inplace=True)

    except:
        raise Exception("Invalid credentials.")

    return df

##################################### TESTS ##################################### 
@pytest.mark.parametrize("cur, user, pwd, city, year", [(cur, 'naranguren', 'pwd1234', ['bogota','medellin'], [2018, 2022]),
                                             (cur, 'naranguren', 'pwd1234', ['bogota','medellin', 'barranquilla'], [2022]),
                                             (cur, 'naranguren', 'pwd1234', ['pereira'], [2011])])
def test_for_sale_properties_two_filters(cur, user, pwd, city, year):
   print("Testing add function with city and year filters...")
   assert isinstance(for_sale_properties(cur, user, pwd, city, year), pd.DataFrame)

@pytest.mark.parametrize("cur, user, pwd, city", [(cur, 'naranguren', 'pwd1234', ['bogota','medellin']),
                                             (cur, 'naranguren', 'pwd1234', ['medellin']),
                                             (cur, 'naranguren', 'pwd1234', ['barranquilla'])])
def test_for_sale_properties_city_filter(cur,user, pwd, city):
   print("Testing add function with city filter...")
   assert isinstance(for_sale_properties(cur, user, pwd, city), pd.DataFrame)

@pytest.mark.parametrize("cur, user, pwd, city, year", [(cur, 'naranguren', 'pwd1234', f'SELECT DISTINCT(p.city) FROM {property_table} AS p', [2002,2011]),
                                             (cur, 'naranguren', 'pwd1234', f'SELECT DISTINCT(p.city) FROM {property_table} AS p', [2016]),
                                             (cur, 'naranguren', 'pwd1234', f'SELECT DISTINCT(p.city) FROM {property_table} AS p', [2018,2015])])
def test_for_sale_properties_year_filter(cur, user, pwd, city, year):
   print("Testing add function with year filter...")
   assert isinstance(for_sale_properties(cur, user, pwd, city, year), pd.DataFrame)

@pytest.mark.parametrize("cur, user, pwd", [(cur, 'naranguren', 'pwd1234'),
                                            (cur, 'elon', 'testpass123'),
                                            (cur, 'naranguren', 'pwd1234')])
def test_for_sale_properties_year_filter(cur, user, pwd):
   print("Testing add function with no filter...")
   assert isinstance(for_sale_properties(cur, user, pwd), pd.DataFrame)