from connect_mysql import connect_database
conn = connect_database()
cursor = conn.cursor()

class BorrowedBooks:
  def __init__ (self,user_id,book_id,borrow_date,id = None):
    # Borrowed Book class for handling all book that are to go out on loan
    self._id = id
    self._user_id = user_id
    self._book_id = book_id
    self._borrow_date = borrow_date
    self._return_date = None

  def update_borrowed_books_save(self):
    # updating MySQL borrowed_books when editing
    updating_genre = '''UPDATE borrowed_books SET user_id = %s, book_id = %s, borrow_date = %s, return_date = %s WHERE id = %s'''
    cursor.execute(updating_genre,(self.get_user_id(),self.get_book_id(),self.get_borrow_date(),self.get_return_date(),self.get_id()))
    conn.commit()
    print(f"Update Complete")

  def save_borrowed_books_sql(self):
    # saving info to MySQL borrowed_books
    search = " SELECT book_id FROM borrowed_books WHERE book_id = %s"
    cursor.execute(search,(self.get_book_id(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_book_id()}' is already checked out")
    else:
      adding_borrowed_books_sql = """INSERT INTO borrowed_books (user_id,book_id,borrow_date,return_date) VALUES (%s,%s,%s,%s)"""
      cursor.execute(adding_borrowed_books_sql,(self.get_user_id(),self.get_book_id(),self.get_borrow_date(),self.get_return_date()))
      conn.commit()

  @classmethod
  def create_borrowed_books(cls,user_id,book_id,borrow_date):
    # Creating borrowed_book class into MySQL database
    new_instance_borrowed_books = cls(user_id,book_id,borrow_date)
    new_instance_borrowed_books.save_borrowed_books_sql()
    return new_instance_borrowed_books

  @classmethod
  def create_from_database_borrowed_books(cls,borrowed_books_rows):
    # Pulling info from getting_rows and making them into borrowed_book class
    new_instance_borrowed_books_ = cls(borrowed_books_rows[1],borrowed_books_rows[2],borrowed_books_rows[3],borrowed_books_rows[4])
    new_instance_borrowed_books_._id = borrowed_books_rows[0]
    return new_instance_borrowed_books_
  
  @classmethod
  def get_borrowed_books_rows(cls):
    # Getting info from MySQL and passing it to my dicts
    fetching_borrowed_books = '''SELECT * FROM borrowed_books'''
    cursor.execute(fetching_borrowed_books)
    borrowed_books_table_rows = cursor.fetchall()
    if len(borrowed_books_table_rows) == 0:
      return None
    else:
      return [cls.create_from_database_borrowed_books(row) for row in borrowed_books_table_rows],[row[1] for row in borrowed_books_table_rows]

  @classmethod
  def getting_borrowed_book_id(cls,book_id,user_id):
    # Getting borrowed book id that matches both the user id and book id. Used to insure that the user returning the book matches that book on loan.
    search = """SELECT id FROM borrowed_books WHERE book_id = %s and user_id = %s"""
    cursor.execute(search,(book_id,user_id))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False

  @classmethod
  def getting_borrowed_book_id_delete_edit(cls,book_id):
      # This is for deleting borrowed books but also for getting the id of a borrowed book to edit.
      search = """SELECT id FROM borrowed_books WHERE book_id = %s"""
      cursor.execute(search,(book_id,))
      matching = cursor.fetchone()
      if matching:
        return matching[0]
      else:
        return False

  @classmethod
  def deleting_borrowed_book(cls,borrowed_book_id):
    delete = """DELETE FROM borrowed_books WHERE id = %s"""
    cursor.execute(delete,(borrowed_book_id,))
    conn.commit()

  @classmethod
  def getting_book_title(cls,borrowed_book_id):
    # Matching a loaned book when trying to view if it is out on loan
    search = """SELECT b.title
    FROM borrowed_books as bb
    JOIN books as b
    ON bb.book_id = b.id
    WHERE bb.id = %s"""
    cursor.execute(search,(borrowed_book_id,))
    matching = cursor.fetchone()
    return matching[0]
  
  @classmethod
  def getting_users_name(cls,borrowed_book_id):
  # Matching user with a book out on loan for viewing.
    search = """SELECT u.name
    FROM borrowed_books as bb
    JOIN users as u
    ON bb.user_id = u.id
    WHERE bb.id = %s"""
    cursor.execute(search,(borrowed_book_id,))
    matching = cursor.fetchone()
    return matching[0]

  def get_id(self):
    return self._id
  
  def get_user_id(self):
    return self._user_id
  
  def get_book_id(self):
    return self._book_id
  
  def get_borrow_date(self):
    return self._borrow_date
  
  def get_return_date(self):
    return self._return_date
  
  def set_user_id(self,new_user_id):
    self._user_id = new_user_id
  
  def set_book_id(self,new_book_id):
    self._book_id = new_book_id
  
  def set_borrow_date(self,new_borrow_date):
    self._borrow_date = new_borrow_date
  
  def set_return_date(self,new_return_date):
    self._return_date = new_return_date

  def view_borrowed_books(self):
    print("Books Checked Out:")
    print(f"\nBook Title: {self.getting_book_title(self.get_id())}\nBook I.D. Number: {self.get_book_id()}\nUsers Name: {self.getting_users_name(self.get_id())}\nUsers I.D. Number: {self.get_user_id()}\nDate Borrowed: {self.get_borrow_date()}\nReturn Date: {self.get_return_date()}\n")