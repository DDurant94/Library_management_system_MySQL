from DataError import UserError
from connect_mysql import connect_database
conn = connect_database()
cursor = conn.cursor()

class User:
  def __init__ (self,user_name,library_id,id = None):
    self._id = id
    self._user_name = user_name
    self._library_id = library_id

  def update_users_save(self):
    # updating MySQL when editing genres
    updating_genre = '''UPDATE users SET name = %s, library_id = %s WHERE id = %s'''
    cursor.execute(updating_genre,(self.get_user_name(),self.get_library_id(),self.get_user_id()))
    conn.commit()
    print(f"'{self.get_user_name()}' has been Updated")
 
  def save_users_sql(self):
    # Saving to MySQL when adding info with a fail safe to check if the user is in MySQL
    search = " SELECT name FROM users WHERE name = %s"
    cursor.execute(search,(self.get_user_name(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_user_name()}' is already in Database")
    else:
      adding_users_sql = """INSERT INTO users (name,library_id) VALUES (%s,%s)"""
      cursor.execute(adding_users_sql,(self.get_user_name(),self.get_library_id()))
      conn.commit()
      print(f"User '{self.get_user_name()}' was added to Database ")

  @classmethod 
  def create_users(cls,name,library_id):
    # adding info to MySQL via save_user_sql
    new_instance_users = cls(name,library_id)
    new_instance_users.save_users_sql()
    return new_instance_users
  
  @classmethod 
  def create_from_database_users(cls,users_rows):
    # making rows into class objects
    new_instance_users_ = cls(users_rows[1],users_rows[2])
    new_instance_users_._id = users_rows[0]
    return new_instance_users_

  @classmethod 
  def get_users_rows(cls):
    # taking each row from MySql and passing it to create_from_database_users and returning info to my dicts as objects
    fetching_users = '''SELECT * FROM users'''
    cursor.execute(fetching_users)
    users_table_rows = cursor.fetchall()
    return [cls.create_from_database_users(row) for row in users_table_rows],[row[1] for row in users_table_rows]
  
  @classmethod
  def search_user_name_for_id(cls,name):
     # using users name to get users id 
    search = """SELECT id FROM users WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      raise UserError(f"'{name}' is not a User in Database")
         
  @classmethod
  def search_user_id_for_name(cls,id):
     # using users id to get users name
    search = """SELECT name FROM users WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      raise UserError(f"'{cls.get_user_name()}' is not a User in Database")
  
  @classmethod 
  def search_library_ids(cls,library_id):
    # matching library ids. each id is to be unique
    search = """SELECT library_id FROM users WHERE library_id = %s """
    cursor.execute(search,(library_id,))
    matching = cursor.fetchone()
    if matching:
      return True
    else:
      return False
    
  @classmethod
  def deleting_user(cls,user_id):
    delete = """DELETE FROM users WHERE id = %s"""
    cursor.execute(delete,(user_id,))
    conn.commit()

  @classmethod 
  def getting_borrowed_books(cls,user_id):
    # getting all books that the user has on loan matching the book id and getting titles back
    search = """SELECT b.title, bb.borrow_date,bb.return_date
    FROM books as b
    INNER JOIN borrowed_books AS bb
    ON b.id = bb.book_id
    INNER JOIN users as u
    ON u.id = bb.user_id
    WHERE u.id = %s"""
    cursor.execute(search,(user_id,))
    matching = cursor.fetchall()
    if matching:
      return matching
    else:
      return False
    
  def get_user_id(self):
    return self._id

  def get_user_name(self):
    return self._user_name
  
  def get_library_id(self):
    return self._library_id
  
  def set_users_name(self,new_user_name):
    self._user_name = new_user_name
  
  def set_library_id(self,new_library_id):
    self._library_id = new_library_id

  def view_user_details(self):
    print(f"\nName: {self.get_user_name()}\nI.D. Number: {self.get_user_id()}\nUser Library I.D. Number: {self.get_library_id()}")
    books_checked_out = self.getting_borrowed_books(self.get_user_id())
    print("Borrowed Books:")
    if books_checked_out == False:
      print("No Books Checked out")
    else:
        for count, matches in enumerate(books_checked_out):
          print(f"{count + 1}. Title: {matches[0]} Borrow Date: {matches[1]} Return Date: {matches[2]}")
        print(f"Total Books Checked Out: {len(books_checked_out)}")