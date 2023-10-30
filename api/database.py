from mysql.connector import connect, errorcode, Error
from config import settings

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
  
  