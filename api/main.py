from database import connect_db
import json
from models.users_look_up import for_sale_properties, property_table

# Connection to the database
cnn, cur = connect_db()

# User request
with open('api/user_request.json') as f:
   user_request = json.load(f)



# Call user query function
# for_sale_properties(cur, 'naranguren', 'pwd1234', year_filter=user_request['year'])

if "city" in list(user_request.keys()) and "year" in list(user_request.keys()) :
    for_sale_properties(cur, 'naranguren', 'pwd1234', city_filter=user_request['city'], year_filter=user_request['year'])

elif "city" not in list(user_request.keys()) and "year" in list(user_request.keys()):
    for_sale_properties(cur, 'naranguren', 'pwd1234', year_filter=user_request['year'])

elif "city" in list(user_request.keys()) and "year" not in list(user_request.keys()):
    for_sale_properties(cur, 'naranguren', 'pwd1234', city_filter=user_request['city'])

elif "city" not in list(user_request.keys()) and "year" not in list(user_request.keys()):
    for_sale_properties(cur, 'naranguren', 'pwd1234')