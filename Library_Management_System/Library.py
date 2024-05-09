import re
from connect_mysql import connect_database
conn = connect_database()
cursor = conn.cursor()

class Book:
  def __init__ (self,title, author_id, isbn, genre_id, publication_date, id = None):
    self.__id = id
    self.__title = title
    self.__author_id = author_id
    self.__isbn = isbn
    self.__genre_id = genre_id
    self.__publication_date = publication_date
    self.availability_status = "Available"

  def save_book_sql(self):
    search = " SELECT title FROM books WHERE title = %s"
    cursor.execute(search,(self.get_title(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_title()}' is already in Database")
    else:
      adding_book_sql = """INSERT INTO Books (title,author_id,genre_id,isbn,publication_date,availability) VALUES (%s,%s,%s,%s,%s,%s)"""
      cursor.execute(adding_book_sql,(self.get_title(),self.get_author_id(),self.get_genre_id(),self.get_isbn(),self.get_publication_date(),self.change_availability_status_export()))
      conn.commit()
      print(f"Book '{self.get_title()}' was added to Database ")

  @classmethod
  def create_book(cls,title,author_id,genre_id,isbn,publication_date):
    new_instance_book = cls(title,author_id,genre_id,isbn,publication_date)
    new_instance_book.save_book_sql()
    return new_instance_book
  
  @classmethod
  def create_from_database_book(cls,book_rows):
    new_instance_book_ = cls(book_rows[1],book_rows[2],book_rows[3],book_rows[4],book_rows[5],book_rows[6])
    new_instance_book_.__id = book_rows[0]
    return new_instance_book_

  @classmethod
  def get_book_rows(cls):
    fetching_books = '''SELECT * FROM books'''
    cursor.execute(fetching_books)
    book_table_rows = cursor.fetchall()
    return [cls.create_from_database_book(row) for row in book_table_rows]
  
  @classmethod
  def get_book(cls,title):
    fetching_book = '''SELECT b.id,b.title,a.name,g.name,publication_date,availability
    FROM books as b
    JOIN authors as a and genres as g
    ON b.author_id = a.id and b.genre_id = g.id
    WHERE b.title = %s'''
    cursor.execute(fetching_book,(title,))
    book_table_rows = cursor.fetchone()
    return book_table_rows

  @classmethod
  def search_book_name_for_id(cls,title):
    search = """SELECT id FROM books WHERE title = %s"""
    cursor.execute(search,(title,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False
    
  @classmethod
  def search_book_id_for_name(cls,id):
    search = """SELECT title FROM books WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False

  @classmethod
  def searching_books(cls,title):
    search = """SELECT availability FROM books WHERE title = %s"""
    cursor.execute(search,(title,))
    matching = cursor.fetchone()
    if matching == "True":
      return True
    else:
      return False
    
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

  def change_availability_status_export(self):
    if self.availability_status == "Available":
      return True
    return False
  
  def change_availability_status_import(self): #needs fixed
    pass

  def borrow_book(self):
    if self.availability_status == "Available":
      self.availability_status = "Borrowed"
      return True
    return False

  def return_book(self):
    self.availability_status = "Available" 

  def set_author(self,new_author): # needs fixed
    self.__author = new_author

  def set_isbn(self,new_isbn):
    self.__isbn = new_isbn

  def set_genre(self,new_genre): # needs fixed
    self.__genre = new_genre

  def set_publication_date(self,new_publication_date):
    self.__publication_date = new_publication_date

  def set_genre_(self): # needs fixed
    return self.get_genre() + ": No additional info at this moment"
  
  def view_book(self): # needs fixed
    print(f"\nTitle: {self.get_title()}\nAuthor Number: {self.get_author_id()}\nBook Number: {self.get_isbn()}\nGenre: {self.get_genre_id()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class FictionBook(Book):

  def set_genre_(self):
    if self.get_genre() == "Fiction":
      return self.get_genre() + "- Is a fake story"
  
  def view_book(self): # needs fixed
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class NonFictionBook(FictionBook):

  def set_genre_(self):
    if self.get_genre() == "Non-Fiction":
      return self.get_genre() + "- Is factual events or information"
  
  def view_book(self): # needs fixed 
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class BiographyBook(NonFictionBook):
  
  def set_genre_(self):
    if self.get_genre() == "Biography":
      return self.get_genre() + "- Is about what a person has done in their life"
  
  def view_book(self): # needs fixed 
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class User:
  def __init__ (self,user_name,library_id,id = None):
    self._id = id
    self._user_name = user_name
    self._library_id =library_id
    self.borrowed_books = []

  def save_users_sql(self):
    search = " SELECT name FROM users WHERE name = %s"
    cursor.execute(search,(self.get_user_name(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_user_name()}' is already in Database")
    else:
      adding_users_sql = """INSERT INTO users (name,library_id) VALUES (%s,%s,%s)"""
      cursor.execute(adding_users_sql,(self.get_user_name(),self.get_library_id(),self.get_borrowed_books()))
      conn.commit()
      print(f"User '{self.get_user_name()}' was added to Database ")

  @classmethod
  def create_users(cls,name,library_id,borrowed_books):
    new_instance_users = cls(name,library_id,borrowed_books)
    new_instance_users.save_users_sql()
    return new_instance_users
  
  @classmethod
  def create_from_database_users(cls,users_rows):
    new_instance_users_ = cls(users_rows[1],users_rows[2])
    new_instance_users_._id = users_rows[0]
    return new_instance_users_

  @classmethod
  def get_users_rows(cls):
    fetching_users = '''SELECT * FROM users'''
    cursor.execute(fetching_users)
    users_table_rows = cursor.fetchall()
    return [cls.create_from_database_users(row) for row in users_table_rows]
  
  @classmethod
  def search_user_name_for_id(cls,name):
    search = """SELECT id FROM users WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False
    
  @classmethod
  def search_user_id_for_name(cls,id):
    search = """SELECT name FROM users WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False
  
  @classmethod
  def search_library_ids(cls,library_id):
    search = """SELECT library_id FROM users WHERE library_id = %s """
    cursor.execute(search,(library_id,))
    matching = cursor.fetchone()
    if matching:
      return True
    else:
      return False

  def get_user_id(self):
    return self._id

  def get_user_name(self):
    return self._user_name
  
  def get_library_id(self):
    return self._library_id
  
  def get_borrowed_books(self):
    return self.borrowed_books
  
  def set_library_id(self,new_library_id):
    self._library_id = new_library_id
  
  def adding_borrowed_books(self,book):
    if book in self.get_borrowed_books():
      print(f"{book} is already loaned to {self.get_user_name()}")
    else:
      self.get_borrowed_books().append(book)
      print(f"'{self.get_user_name()}' has checked out '{book}'")

  def returning_borrowed_book(self,book):
    if book in self.get_borrowed_books():
      self.get_borrowed_books().remove(book)
      print(f"'{book}' has been checked back in")
    else:
      print(f"'{book}' is not checked out to '{self.get_user_name()}'")

  def view_user_details(self):
    print(f"{self.get_user_name()}s User Library I.D. Number: {self.get_library_id()}")
    print(f"Borrowed Books: {', '.join(self.get_borrowed_books())}\n")

class Author:
  def __init__ (self, author_name, biography,id = None):
    self.__id = id
    self._author_name = author_name
    self._biography = biography

  def save_authors_sql(self):
    search = " SELECT name FROM authors WHERE name = %s"
    cursor.execute(search,(self.get_author_name(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_author_name()}' is already in Database")
    else:
      adding_authors_sql = """INSERT INTO authors (name,biography) VALUES (%s,%s)"""
      cursor.execute(adding_authors_sql,(self.get_author_name(),self.get_biography()))
      conn.commit()
      print(f"Author '{self.get_author_name()}' was add to Database")

  @classmethod
  def create_authors(cls,name,biography):
    new_instance_authors = cls(name,biography)
    new_instance_authors.save_authors_sql()
    return new_instance_authors
  
  @classmethod
  def create_from_database_authors(cls,authors_rows):
    new_instance_authors_ = cls(authors_rows[1],authors_rows[2])
    new_instance_authors_.__id = authors_rows[0]
    return new_instance_authors_

  @classmethod
  def get_authors_rows(cls):
    fetching_authors = '''SELECT * FROM authors'''
    cursor.execute(fetching_authors)
    authors_table_rows = cursor.fetchall()
    return [cls.create_from_database_authors(row) for row in authors_table_rows]
  
  @classmethod
  def search_author_name_for_id(cls,name):
    search = """SELECT id FROM authors WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching: 
      return matching[0]
    else:
      return False
    
  @classmethod
  def search_author_id_for_name(cls,id):
    search = """SELECT name FROM authors WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return True, matching[0]
    else:
      return False

  def get_author_id(self):
    return self.__id

  def get_author_name(self):
    return self._author_name
  
  def get_biography(self):
    return self._biography
  
  def set_biography(self,new_biography):
    self._biography = new_biography
  
  def view_author_details(self):
    print(f"Name: {self.get_author_name()}\nAuthor I.D.: {self.get_author_id()}\nBiography:\n{self.get_biography()}")

class Genre:
  def __init__(self,genre_name,description,category,id = None):
    self._id = id
    self._genre_name = genre_name
    self._description = description
    self._category = category

  def save_genres_sql(self):
    search = " SELECT name FROM genres WHERE name = %s"
    cursor.execute(search,(self.get_genre_name(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_genre_name()}' is already in Database")
    else:
      adding_genres_sql = """INSERT INTO genres (name,description,category) VALUES (%s,%s,%s)"""
      cursor.execute(adding_genres_sql,(self.get_genre_name(),self.get_description(),self.get_category()))
      conn.commit()
      print(f"Genre '{self.get_genre_name()}' was added to Database")

  @classmethod
  def create_genres(cls,name,description,category):
    new_instance_genres = cls(name,description,category)
    new_instance_genres.save_genres_sql()
    return new_instance_genres
  
  @classmethod
  def create_from_database_genres(cls,genres_rows):
    new_instance_genres_ = cls(genres_rows[1],genres_rows[2],genres_rows[3])
    new_instance_genres_._id = genres_rows[0]
    return new_instance_genres_

  @classmethod
  def get_genres_rows(cls):
    fetching_genres = '''SELECT * FROM genres'''
    cursor.execute(fetching_genres)
    genres_table_rows = cursor.fetchall()
    return [cls.create_from_database_genres(row) for row in genres_table_rows]
  
  @classmethod
  def search_genre_name_for_id(cls,name):
    search = """SELECT id FROM genres WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False
    
  @classmethod
  def search_genre_id_for_name(cls,id):
    search = """SELECT name FROM genres WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      return False

  def get_genre_id(self):
    return self._id

  def get_genre_name(self):
        return self._genre_name

  def get_description(self):
      return self._description

  def get_category(self):
      return self._category

  def set_description(self, new_description):
      self._description = new_description

  def set_category(self, new_category):
      self._category = new_category

  def view_genre_details(self):
    print(f"{self.get_genre_name()}:\nGenre I.D. Number{self.get_genre_id()}\nDescription- {self.get_description()}\nCategory: {self.get_category()}")

class BorrowedBooks:
  def __init__ (self,user_id,book_id,borrow_date,id = None):
    self._id = id
    self.user_id = user_id
    self.book_id = book_id
    self.borrow_date = borrow_date
    self.return_date = None

  def save_borrowed_books_sql(self):
    search = " SELECT book_id FROM borrowed_books WHERE book_id = %s"
    cursor.execute(search,(self.book_id,))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.user_id}' is already checked out")
    else:
      adding_borrowed_books_sql = """INSERT INTO borrowed_books (user_id,book_id,borrow_date,return_date) VALUES (%s,%s,%s,%s)"""
      cursor.execute(adding_borrowed_books_sql,(self.user_id,self.book_id,self.borrow_date,self.return_date))
      conn.commit()
      print(f"Book Checked out")

  @classmethod
  def create_borrowed_books(cls,user_id,book_id,borrow_date,return_date):
    new_instance_borrowed_books = cls(user_id,book_id,borrow_date,return_date)
    new_instance_borrowed_books.save_borrowed_books_sql()
    return new_instance_borrowed_books
  
  @classmethod
  def create_from_database_borrowed_books(cls,borrowed_books_rows):
    new_instance_borrowed_books_ = cls(borrowed_books_rows[1],borrowed_books_rows[2],borrowed_books_rows[3],borrowed_books_rows[4])
    new_instance_borrowed_books_._id = borrowed_books_rows[0]
    return new_instance_borrowed_books_

  @classmethod
  def get_borrowed_books_rows(cls):
    fetching_borrowed_books = '''SELECT * FROM borrowed_books'''
    cursor.execute(fetching_borrowed_books)
    borrowed_books_table_rows = cursor.fetchall()
    return [cls.create_from_database_borrowed_books(row) for row in borrowed_books_table_rows]
  
  def get_id(self):
    return self._id

class UserInterface:
  def __init__ (self):
    self.book_inventory = {}
    self.user_information = {}
    self.author_information = {}
    self.genre_information = {}
    self.current_loans = {}
    self.conn = connect_database()
    self.cursor = conn.cursor()

  def book_operations(self):
    if self.conn is not None:
      self.conn = connect_database()
    try:
      while True:
        self.cursor = conn.cursor()
        print("\nBook Operations Menu:\n1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books\n6. Edit Book\n7. Exit")
        book_operation_choice = input("Please choose a menu option: ")
        if book_operation_choice == "1":
          Adding_information.add_book()
        elif book_operation_choice == "2":
          BookProcessing.checking_book_out()
        elif book_operation_choice == "3":
          BookProcessing.returning_book()
        elif book_operation_choice == "4":
          book_search = input("Enter book name to search: ").title()     
          BiographyBook.view_book()
        elif book_operation_choice == "5":
          books = Book.get_book_rows()
          for book in books:
            Book.view_book(book)
        elif book_operation_choice == "6":
          EditInfo.edit_book()
        elif book_operation_choice == "7":
          self.conn.commit()
          print("Returning to Main Menu...")
          break
        else:
          print("Invalid Choice")
    except Exception as e:
      print(f"Error: {e}")
    finally:
      self.cursor.close()
      self.conn.close()
  
  def user_operations(self):
    if self.conn is not None:
      self.conn = connect_database()
    try:
      while True:
        self.cursor = conn.cursor()
        print("\nUser Operations Menu:\n1. Add a new user\n2. View user details\n3. Display all users\n4. Edit User\n5. Exit")
        user_operation_choice = input("Please choose a menu option: ")
        if user_operation_choice == "1":
          Adding_information.add_user()
        elif user_operation_choice == "2":
          users_name = input("Enter users First and Last Name: ").title()
          User.view_user_details()
        elif user_operation_choice == "3":
          users = User.get_users_rows()
          for user in users:
            User.view_user_details(user)
        elif user_operation_choice == "4":
          EditInfo.edit_user()
        elif user_operation_choice == "5":
          print("Returning to Main Menu...")
          self.conn.commit()
          break
        else:
          print("Invalid Choice")
    except Exception as e:
      print(f"Error: {e}")
    finally:
      self.cursor.close()
      self.conn.close()
      
  def author_operations(self):
    if self.conn is not None:
      self.conn = connect_database()
    try:
      while True:
        self.cursor = conn.cursor()
        print("\nAuthor Operations:\n1. Add a new author\n2. View author details\n3. Display all authors\n4. Edit Author\n5. Exit")
        author_operation_choice = input("Please choose a menu option: ")
        if author_operation_choice == "1":
          Adding_information.add_author()
        elif author_operation_choice == "2":
          author_name = input("Enter Authors name: ").title()
          Author.view_author_details()
        elif author_operation_choice == "3":
          all_authors = Author.get_authors_rows()
          for author in all_authors:
            Author.view_author_details(author)
        elif author_operation_choice == "4":
          EditInfo.edit_author()
        elif author_operation_choice == "5":
          print("Returning to Main Menu...")
          self.conn.commit()
          break
        else:
          print("Invalid Choice")
    except Exception as e:
      print(f"Error: {e}")
    finally:
      self.cursor.close()
      self.conn.close()

  def genre_operations(self):
    if self.conn is not None:
      self.conn = connect_database()
    try:
      while True:
        self.cursor = conn.cursor()
        print("\nGenre Operations:\n1. Add a new genre\n2. View genre details\n3. Display all genres\n4. Edit Genre\n5. Exit")
        genre_operation_choice = input("Please choose a menu option: ")
        if genre_operation_choice == "1":
          Adding_information.add_genre()
        elif genre_operation_choice == "2":
          genre_name = input("Enter Genre: ").title()
          Genre.view_genre_details()
        elif genre_operation_choice == "3":
          genres = Genre.get_genres_rows()
          for genre in genres:
            Genre.view_genre_details(genre)
        elif genre_operation_choice == "4":
          EditInfo.edit_genre()
        elif genre_operation_choice == "5":
          print("Returning to Main Menu...")
          self.conn.commit()
          break
        else:
          print("Invalid Choice")
    except Exception as e:
      print(f"Error: {e}")
    finally:
      self.cursor.close()
      self.conn.close()
    
class Database:


  # def adding_borrowed_book_database(current_loans,cursor): # needs rework
  #   search = """SELECT user_id FROM borrowed_books WHERE user_id = %s and book_id = %s"""
  #   cursor.execute(search,(user_id,book_id))
  #   matching = cursor.fetchone()
  #   if matching:
  #     print(f"User with I.D. Number {user_id} or Book with I.D. Number {book_id}is not Checked out")
  #   else:
  #     query = """INSERT INTO borrowed_books (user_id,book_id,borrow_date,return_date) VALUES (%s,%s,%s,%s)"""
  #     cursor.execute(query,(user_id,book_id,borrow_date,return_date))

  def search_borrowed_book_id(): # needs fixed
    search = """SELECT  FROM borrowed_books WHERE customer_id = %s"""
  
  def search_borrowed_book_name():
    pass

class Adding_information:
  def users_name_authenticator(user_name):
    users_name_standard = r"^\w{2,15}\s\w{2,15}$"
    matching_users_name = re.match(users_name_standard,user_name)
    if matching_users_name:
      return True
    else:
      return False

  def add_book():
    try:
      title = input("Enter Title of book: ").title()
      author = input("Enter Author of book: ").title()
      isbn = int(input("Enter ISBN: ")) 
      genre = input("Enter Genre of book: ").title()
      publication_date = input("Enter Publication Date [YYYY-MM-DD]: ").title()
      author_id = Author.search_author_name_for_id(author)
      genre_id = Genre.search_genre_name_for_id(genre)
      if author_id == False:
        Author.create_authors(author,None)
        author_id = Author.search_author_name_for_id(author)
      if genre_id == False:
        Genre.create_genres(genre,None,None)
        genre_id = Genre.search_genre_name_for_id(genre)
      if genre == "Fiction":
        FictionBook.create_book(title, author_id, isbn, genre_id, publication_date)
      elif genre == "Non-Fiction":
        NonFictionBook.create_book(title, author_id, isbn, genre_id, publication_date)
      elif genre == "Biography":
        BiographyBook.create_book(title, author_id, isbn, genre_id, publication_date)
      else:
        Book.create_book(title, author_id, isbn, genre_id, publication_date)
        
    except ValueError:
      print("Enter a 'Number' for the ISBN")

  def add_user():
    try:
      user_name = input("Enter First and Last Name of user to be added: ").title()
      if Adding_information.users_name_authenticator(user_name):    
        library_id = int(input("Enter Library I.D. Number: "))
        if User.search_library_ids(library_id):
          print(f"Library I.D. '{library_id}' is already taken")
        else:
          User.create_users(user_name,library_id)
      else:
        print("Format of Users Name is wrong. [Ex. Daniel Durant]")
    except ValueError:
      print("Enter a 'Number' for the Library I.D.")

  def add_author():
    author_name = input("Enter Name of Author to be added: ").title()
    biography = input("Enter biography for Author: ")
    Author.create_authors(author_name, biography)

  def add_genre():
    genre_name = input("Enter Genre: ").title()
    description = input("Enter Description of Genre: ").capitalize()
    category = input("Enter Genre Category: ").title()
    Genre.create_genres(genre_name,description,category)

class BookProcessing:

  def checking_book_out(): # need to get this into database user id FK and book ID FK date borrowed and return(make the return auto) use string minpulation to do so
    user_search = input("Enter in User checking out book: ").title()
    book_search = input("Enter book name to Borrow: ").title()
    book_id = Book.get_book_id(book_search)
    user_id = User.get_user_id(user_search)
    if book_id is not True:
      print(f"'{book_search} is not in Inventory'")
    if user_id is not True:
      print(f"{user_search} is not a User")
    



  def returning_book(book_inventory,user_information,current_loans): # delete the borrowed book from the database
    user_returning_book = input("Enter Person Returning Book: ").title()
    book_return = input("Enter Book being returned: ").title()

class EditInfo:

  def edit_book():
    book_name = input("Enter Book to Edit: ").title()
    check_book = Book.get_book_id(book_name)
    if check_book == False:
      print(f"{book_name} Not Found Book Database")
    else:
      while True:
        try:
          print("Book Edit Menu:\n1. Author\n2. ISBN\n3. Genre\n4. Publication Date\n5. Change User Name\n6. Exit")
          book_edit_choice = input("Choose an option: ")
          if book_edit_choice == "1":
            author_edit = input("Enter Author Edit: ").title()
            author_id = Author.get_author_id(author_edit)
            if author_id == False:
              pass

          elif book_edit_choice == "2":
            isbn_edit = int(input("Enter New ISBN"))
            
          elif book_edit_choice == "3":
            genre_edit = input("Enter New Genre: ").title()
            genre_id = Genre.get_genre_id(genre_edit)
            if genre_id == False:
              pass 

          elif book_edit_choice == "4":
            publication_date_edit = input("Enter New Publication Date YYYY-MM-DD: ")
     
          elif book_edit_choice =="5":
            title_edit = ("Enter title edit: ").title()

          elif book_edit_choice == "6":
            print("Return to Book Menu...")
            break
          else:
            print("Invalid Choice")
        except ValueError:
          print("Enter a 'Number for ISBN")

  def edit_user():
    try:
      user_name = input("Enter Users First and Last Name to Edit: ").title()
      user_id = User.get_user_id(user_name)
      if user_id == False:
        print(f"'{user_name}' Not Found in User Database")
      else:
        while True:
          print("User Edit Menu:\n1. Edit Name\n2. Edit Library I.D.\n3. Exit")
          edit_user_choice = input("Choose Menu Option: ")
          if edit_user_choice == "1":
            pass
          elif edit_user_choice == "2":
            user_new_id= int(input("Enter new Library I.D. Number: "))
          elif edit_user_choice == "3":
            print("Returning to User Menu...")
            break
          else:
            print("Invalid Choice")
    except ValueError:
      print("Enter a 'Number' for the Library I.D.")

  def edit_author(author_info):
    author_name = input("Enter Author to edit: ").title()
    author_search = Author.get_author_id(author_name)
    if author_search == False:
      print(f"{author_name} Not Found in Author Database")
    else:
      while True:
        print("Author Edit Menu:\n1. Edit Name\n2. Edit Biography\n3. Exit")
        author_edit_choice = input("Choose Menu Option: ")
        if author_edit_choice == "1":
          pass
        elif author_edit_choice == "2":
          author_edit = input("Enter New Biography: ")
        elif author_edit_choice == "3":
          print("Returning to Author Menu...")
          break
        else:
          print("Invalid Choice")

  def edit_genre(genre_information):
    genre_name = input("Enter Genre to edit: ").title()
    search_genre = Genre.get_genre_id(genre_name)
    if search_genre == False:
      print(f"{genre_name} Not Found in Genre Database")
    else:
      while True:
        print("Edit Genre Menu:\n1. Edit Genre Name\n2. Edit Description\n3. Edit Category\n4. Exit")
        edit_choice = input("Choose Menu Option: ")
        if edit_choice == "1":
          pass 
        elif edit_choice == "2":
          new_description = input(f"Enter new Description for {genre_name}: ").capitalize()
          
        elif edit_choice == "2":
          new_category = input(f"Enter new Category for {genre_name}: ").title()
          
        elif edit_choice == "3":
          print("Returning to Genre Menu...")
          break
        else:
          print("Invalid Input")