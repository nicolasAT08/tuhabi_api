# tuhabi_api

This API contains the microservice 'user_look_up' logic to allow users to retrieve specific data (address, city, status, price, and description) and filter it by city(s) and year(s) of interest. 

## Technologies
*Note: A requeriments.txt is provided.*
- Python libraries: pandas, typing, mysql.connector, pytest
- MySQL Database

## Solution design
### Database connection
To achieve the connection to the DB, it was defined all the DB credentials using environmental variables to avoid the leak of sensitive information. If some other member of the team wants to connect to the DB, he/she has to set his/her own .env file.
### User authorization
The user ("username" and "password") must exist in the DB to look up the properties available.
### Unit Tests
Tests are executed for the API considring diferent scenarios (user requests). Pytest was the library used to implement tests.
### Fields response for the user
#### *Requirements*
Based on business requirements, the final variables are given (Address, City, Status, Price, Description). In the same way, it was required that the user can pass as parameters one or more cities and years to filter the data.
#### Assumptions
- Users with "is_superuser = 1" are allowed to look up the property table and don't need any other validation.
- Users with "is_staf = 0" and "is_active = 1" are allowed to look up the property table. This define an external user, which is not a employee but is active.
#### "Like propery" requirement
A new table called "user_like" will contain the "property_id" and the "user_id" (FKs) to store properties likes.