import pandas as pd
from .auth_user import login
from typing import Optional, List
from IPython. display import display

# Database tables schemas
auth_table = 'habi_db.auth_user'
status_table = 'habi_db.status'
status_history_table = 'habi_db.status_history'
property_table = 'habi_db.property'

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
                city_filter = ','.join(["'" + i +"'" for i in city_filter])
            else:
                pass

            if isinstance(year_filter,list):
                year_filter = ','.join([str(i) for i in year_filter])
            else:
                pass  

            query = f"""
                    SELECT p.id, p.address, p.city, s.name, p.price, p.description
                    FROM {property_table} AS p LEFT JOIN {status_history_table} sh ON p.id = sh.property_id
                                                LEFT JOIN {status_table} s ON s.id = sh.status_id
                    WHERE s.name IN {allowed_status}
                    AND p.city IN ({city_filter})
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

            display(df)
    except:
        raise Exception("Invalid credentials.")

    return df