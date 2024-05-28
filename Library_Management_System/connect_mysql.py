import mysql.connector
from mysql.connector import Error
# Connecting to MySQL with mysql.connector
def connect_database():
# Database Connection Parameters
  db_name = "LibraryManagementSystem"
  user = "root"
  password = "password"
  host = "localhost"

  try:
    conn = mysql.connector.connect(
      database = db_name,
      user = user,
      password = password,
      host = host 
    )
    return conn
  except Error as e:
    print(f"Error: {e}")
    return None