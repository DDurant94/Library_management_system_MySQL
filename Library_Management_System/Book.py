from DataError import BookError
from connect_mysql import connect_database
conn = connect_database()
cursor = conn.cursor()

class Book:

  def __init__ (self,title, author_id, genre_id, isbn, publication_date,availability_status = True, id = None):
    self.__id = id
    self.__title = title
    self.__author_id = author_id
    self.__isbn = isbn
    self.__genre_id = genre_id
    self.__publication_date = publication_date
    self.availability_status = availability_status

  def update_book_save(self):
    # updating books within MySQL after object is edited
    updating_book = '''UPDATE books SET title = %s,author_id = %s,genre_id = %s,isbn = %s,publication_date = %s,availability = %s WHERE id = %s'''
    cursor.execute(updating_book,(self.get_title(),self.get_author_id(),self.get_genre_id(),self.get_isbn(),self.get_publication_date(),self.availability_status,self.get_book_id()))
    conn.commit()
   
  def save_book_sql(self):
    # Saving to MySQL when adding info with a fail safe to check if the book is in database
    search = " SELECT title FROM books WHERE title = %s"
    cursor.execute(search,(self.get_title(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_title()}' is already in Database")
    else:
      adding_book_sql = """INSERT INTO Books (title,author_id,genre_id,isbn,publication_date,availability) VALUES (%s,%s,%s,%s,%s,%s)"""
      cursor.execute(adding_book_sql,(self.get_title(),self.get_author_id(),self.get_genre_id(),self.get_isbn(),self.get_publication_date(),self.availability_status))
      conn.commit()
      print(f"Book '{self.get_title()}' was added to Database ")

  @classmethod
  def create_book(cls,title,author_id,genre_id,isbn,publication_date):
      # Making info enter into a book object that can be moved around
    new_instance_book = cls(title,author_id,genre_id,isbn,publication_date)
    new_instance_book.save_book_sql()
    return new_instance_book
  
  @classmethod
  def create_from_database_book(cls,book_rows):
    # taking info from MySQL and checking if it doesn't contain any of the the genres. Used to populate anything that doesn't contain 
    # a subclass of books 
    if cls.getting_genre_name_sorting(book_rows[3]) != "Fiction" or "Non-Fiction" or "Biography":
      new_instance_book_ = cls(book_rows[1],book_rows[2],book_rows[3],book_rows[4],book_rows[5],book_rows[6])
      new_instance_book_.__id = book_rows[0]
      return new_instance_book_
  
  @classmethod
  def get_book_rows(cls):
    # grabbing all rows from books in Database
    fetching_books = '''SELECT * FROM books'''
    cursor.execute(fetching_books)
    book_table_rows = cursor.fetchall()
    return [cls.create_from_database_book(row) for row in book_table_rows],[row[1] for row in book_table_rows]
 
  @classmethod
  def get_book(cls,title):
    # getting all info from books in database that contains title that is stated
    fetching_book = '''SELECT b.id,b.title,b.author_id,b.genre_id,isbn,publication_date,availability
    FROM books as b
    WHERE b.title = %s'''
    cursor.execute(fetching_book,(title,))
    book_table_rows = cursor.fetchone()
    book = cls(book_table_rows[1],book_table_rows[2],book_table_rows[3],book_table_rows[4],book_table_rows[5],book_table_rows[6])
    book.__id = book_table_rows[0]
    return book

  @classmethod
  def search_book_name_for_id(cls,title):
    # getting book id by using the book title
    search = """SELECT id FROM books WHERE title = %s"""
    cursor.execute(search,(title,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      raise BookError(f"'{title}' is not in Library Inventory'")
    
  @classmethod
  def search_book_id_for_name(cls,id):
    # getting book title by using book id
    search = """SELECT title FROM books WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      raise BookError(f"'{cls.get_title()}' is not in Library Inventory'")

  @classmethod
  def searching_book_availability(cls,book_id):
    # checking if the book is available to be checked out or not
    search = """SELECT availability,title FROM books WHERE id = %s"""
    cursor.execute(search,(book_id,))
    matching = cursor.fetchone()
    if matching[0] == 1:
      return True
    else:
      raise BookError(f"'{matching[1]}' is not available for checkout")
    
  @classmethod
  def getting_author_name(cls,book_id):
    # getting author name that is linked to this book 
    search = """SELECT a.name
    FROM books as b
    JOIN authors as a
    ON b.author_id = a.id
    WHERE b.id = %s"""
    cursor.execute(search,(book_id,))
    matching = cursor.fetchone()
    return matching[0]
  
  @classmethod
  def getting_genre_name(cls,book_id):
    # getting genre that is linked to this book
    search = """SELECT g.name
    FROM books as b
    JOIN genres as g
    ON b.genre_id = g.id
    WHERE b.id = %s"""
    cursor.execute(search,(book_id,))
    matching = cursor.fetchone()
    return matching[0]
  
  @classmethod
  def deleting_book(cls,book_id):
    delete = """DELETE FROM books WHERE id = %s"""
    cursor.execute(delete,(book_id,))
    conn.commit()

  @classmethod
  def matching_isbn(cls,isbn):
    # checking the ISBN to see if it is attached to any book or not so that it can be unique 
    search = """SELECT title FROM books WHERE isbn = %s"""
    cursor.execute(search,(isbn,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False
    
  @classmethod
  def getting_genre_name_sorting(cls,genre_id):
    # This is to sort each book in database by its genres so that it can be added to the right class or subclass
    search = """SELECT name FROM genres WHERE id = %s"""
    cursor.execute(search,(genre_id,))
    results = cursor.fetchone()
    return results[0]
    
  def get_book_id(self):
    return self.__id

  def get_title(self):
    return self.__title
  
  def get_author_id(self):
    return self.__author_id
  
  def get_isbn(self):
    return self.__isbn
  
  def get_genre_id(self):
    return self.__genre_id
  
  def get_publication_date(self):
    return self.__publication_date
  
  def change_availability_status_view(self):
    if self.availability_status == True:
      return "Available"
    else:
      return "Borrowed"

  def borrow_book(self):
    if self.availability_status == True:
      self.availability_status = False
      return True
    return False

  def return_book(self):
    self.availability_status = True

  def set_title(self,new_title):
    self.__title = new_title

  def set_author_id(self,new_author_id):
    self.__author_id = new_author_id

  def set_isbn(self,new_isbn):
    self.__isbn = new_isbn

  def set_genre_id(self,new_genre_id):
    self.__genre_id = new_genre_id

  def set_publication_date(self,new_publication_date):
    self.__publication_date = new_publication_date

  def set_genre_(self):
    # Sorting by Genre for viewing
    return self.getting_genre_name(self.get_book_id()) + "- No additional info at this moment"
  
  def view_book(self): 
    print(f"\nTitle: {self.get_title()}\nBook Number: {self.get_book_id()}\nAuthor: {self.getting_author_name(self.get_book_id())}\nAuthor I.D. Number: {self.get_author_id()}\nI.S.B.N.: {self.get_isbn()}\nGenre: {self.set_genre_()}\nGenre I.D Number: {self.get_genre_id()}\nPublished: {self.get_publication_date()}\nAvailability: {self.change_availability_status_view()}")

class FictionBook(Book):

  @classmethod
  def getting_genre_name_sorting(cls,genre_id):
    # This is to sort each book in database by its genres so that it can be added to the right class or subclass
    search = """SELECT name FROM genres WHERE id = %s"""
    cursor.execute(search,(genre_id,))
    results = cursor.fetchone()
    return results[0]

  @classmethod
  def create_from_database_book(cls,book_rows):
    # taking info from MySQL and checking if it doesn't contain any of the the genres. Used to populate anything that doesn't contain 
    # a subclass of books 
    if cls.getting_genre_name_sorting(book_rows[3]) == "Fiction":
      new_instance_book_ = cls(book_rows[1],book_rows[2],book_rows[3],book_rows[4],book_rows[5],book_rows[6])
      new_instance_book_.__id = book_rows[0]
      return new_instance_book_
  
  @classmethod
  def get_book_rows(cls):
    # grabbing all rows from books in Database
    fetching_books = '''SELECT * FROM books'''
    cursor.execute(fetching_books)
    book_table_rows = cursor.fetchall()
    return [cls.create_from_database_book(row) for row in book_table_rows],[row[1] for row in book_table_rows]
  
  def get_book_id(self):
    return self.__id

  def set_genre_(self):
    # Sorting by Genre for viewing
    if self.getting_genre_name(self.get_book_id()) == "Fiction":
      return self.getting_genre_name(self.get_book_id()) + "- Is a fake story"
  
  def view_book(self):
   print(f"\nTitle: {self.get_title()}\nBook Number: {self.get_book_id()}\nAuthor: {self.getting_author_name(self.get_book_id())}\nAuthor I.D. Number: {self.get_author_id()}\nI.S.B.N.: {self.get_isbn()}\nGenre: {self.set_genre_()}\nGenre I.D Number: {self.get_genre_id()}\nPublished: {self.get_publication_date()}\nAvailability: {self.change_availability_status_view()}")

class NonFictionBook(FictionBook):

  @classmethod
  def getting_genre_name_sorting(cls,genre_id):
    # This is to sort each book in database by its genres so that it can be added to the right class or subclass
    search = """SELECT name FROM genres WHERE id = %s"""
    cursor.execute(search,(genre_id,))
    results = cursor.fetchone()
    return results[0]

  @classmethod
  def create_from_database_book(cls,book_rows):
    # taking info from MySQL and checking if it doesn't contain any of the the genres. Used to populate anything that doesn't contain 
    # a subclass of books 
    if cls.getting_genre_name_sorting(book_rows[3]) == "Non-Fiction":
      new_instance_book_ = cls(book_rows[1],book_rows[2],book_rows[3],book_rows[4],book_rows[5],book_rows[6])
      new_instance_book_.__id = book_rows[0]
      return new_instance_book_
  
  @classmethod
  def get_book_rows(cls):
    # grabbing all rows from books in Database
    fetching_books = '''SELECT * FROM books'''
    cursor.execute(fetching_books)
    book_table_rows = cursor.fetchall()
    return [cls.create_from_database_book(row) for row in book_table_rows],[row[1] for row in book_table_rows]
  
  def get_book_id(self):
    return self.__id

  def set_genre_(self):
    # Sorting by Genre for viewing
    if self.getting_genre_name(self.get_book_id()) == "Non-Fiction":
      return self.getting_genre_name(self.get_book_id()) + "- Is factual events or information"
  
  def view_book(self):
    print(f"\nTitle: {self.get_title()}\nBook Number: {self.get_book_id()}\nAuthor: {self.getting_author_name(self.get_book_id())}\nAuthor I.D. Number: {self.get_author_id()}\nI.S.B.N.: {self.get_isbn()}\nGenre: {self.set_genre_()}\nGenre I.D Number: {self.get_genre_id()}\nPublished: {self.get_publication_date()}\nAvailability: {self.change_availability_status_view()}")

class BiographyBook(NonFictionBook):

  @classmethod
  def getting_genre_name_sorting(cls,genre_id):
    # This is to sort each book in database by its genres so that it can be added to the right class or subclass
    search = """SELECT name FROM genres WHERE id = %s"""
    cursor.execute(search,(genre_id,))
    results = cursor.fetchone()
    return results[0]

  @classmethod
  def create_from_database_book(cls,book_rows):
    # taking info from MySQL and checking if it doesn't contain any of the the genres. Used to populate anything that doesn't contain 
    # a subclass of books
    if cls.getting_genre_name_sorting(book_rows[3]) == "Biography":
      new_instance_book_ = cls(book_rows[1],book_rows[2],book_rows[3],book_rows[4],book_rows[5],book_rows[6])
      new_instance_book_.__id = book_rows[0]
      return new_instance_book_
  
  @classmethod
  def get_book_rows(cls):
    # grabbing all rows from books in Database
    fetching_books = '''SELECT * FROM books'''
    cursor.execute(fetching_books)
    book_table_rows = cursor.fetchall()
    return [cls.create_from_database_book(row) for row in book_table_rows],[row[1] for row in book_table_rows] 

  def get_book_id(self):
    return self.__id   
  
  def set_genre_(self):
    # Sorting by Genre for viewing
    if self.getting_genre_name(self.get_book_id()) == "Biography":
      return self.getting_genre_name(self.get_book_id()) + "- Is about what a person has done in their life"
  
  def view_book(self):
    print(f"\nTitle: {self.get_title()}\nBook Number: {self.get_book_id()}\nAuthor: {self.getting_author_name(self.get_book_id())}\nAuthor I.D. Number: {self.get_author_id()}\nI.S.B.N.: {self.get_isbn()}\nGenre: {self.set_genre_()}\nGenre I.D Number: {self.get_genre_id()}\nPublished: {self.get_publication_date()}\nAvailability: {self.change_availability_status_view()}")