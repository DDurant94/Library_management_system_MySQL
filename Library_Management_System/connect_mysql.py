import mysql.connector
from mysql.connector import Error

def connect_database():
# Database Connection Parameters
  db_name = "LibraryManagementSystem"
  user = "root"
  password = "$85PeopleDead94!"
  host = "localhost"

  try:
    conn = mysql.connector.connect(
      database = db_name,
      user = user,
      password = password,
      host = host 
    )
    print(f"Connected to MySQL Database Successfully!")
    return conn
  except Error as e:
    print(f"Error: {e}")
    return None
