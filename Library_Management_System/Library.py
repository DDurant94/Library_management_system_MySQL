import re
from connect_mysql import connect_database
# needs fixed
class Book:
  def __init__ (self,title, author, isbn, genre, publication_date):
    self.__id = 0
    self.__title = title
    self.__author = author
    self.__isbn = isbn
    self.__genre = genre
    self.__publication_date = publication_date
    self.availability_status = "Available"

  def get_id(self):
    return self.__id

  def get_title(self):
    return self.__title
  
  def get_author(self):
    return self.__author
  
  def get_isbn(self):
    return self.__isbn
  
  def get_genre(self):
    return self.__genre
  
  def get_publication_date(self):
    return self.__publication_date

  def borrow_book(self):
    if self.availability_status == "Available":
      self.availability_status = "Borrowed"
      return True
    return False

  def return_book(self):
    self.availability_status = "Available" 

  def set_author(self,new_author):
    self.__author = new_author

  def set_isbn(self,new_isbn):
    self.__isbn = new_isbn

  def set_genre(self,new_genre):
    self.__genre = new_genre

  def set_publication_date(self,new_publication_date):
    self.__publication_date = new_publication_date

  def set_genre_(self):
    return self.get_genre() + ": No additional info at this moment"
  
  def view_book(self):
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class FictionBook(Book):

  def set_genre_(self):
    if self.get_genre() == "Fiction":
      return self.get_genre() + "- Is a fake story"
  
  def view_book(self):
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class NonFictionBook(FictionBook):

  def set_genre_(self):
    if self.get_genre() == "Non-Fiction":
      return self.get_genre() + "- Is factual events or information"
  
  def view_book(self):
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class BiographyBook(NonFictionBook):
  
  def set_genre_(self):
    if self.get_genre() == "Biography":
      return self.get_genre() + "- Is about what a person has done in their life"
  
  def view_book(self):
    print(f"\nTitle: {self.get_title()} Author: {self.get_author()}\nBook Number: {self.get_isbn()}\nGenre: {self.set_genre_()}\nPublished: {self.get_publication_date()}\nAvailability: {self.availability_status}")

class User:
  def __init__ (self,user_name,library_id):
    self._user_name = user_name
    self._library_id =library_id
    self.borrowed_books = []

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
    print(f"{self.get_user_name()}s User I.D. Number: {self.get_library_id()}")
    print(f"Borrowed Books: {', '.join(self.get_borrowed_books())}\n")

class Author:
  def __init__ (self, author_name, biography):
    self._author_name = author_name
    self._biography = biography

  def get_author_name(self):
    return self._author_name
  
  def get_biography(self):
    return self._biography
  
  def set_biography(self,new_biography):
    self._biography = new_biography
  
  def view_author_details(self):
    print(f"{self.get_author_name()}\nBiography:\n{self.get_biography()}")

class Genre:
  def __init__(self,genre_name,description,category):
    self._genre_name = genre_name
    self._description = description
    self._category = category

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
    print(f"{self.get_genre_name()}:\nDescription- {self.get_description()}\nCategory: {self.get_category()}")

class UserInterface:
  def __init__ (self):
    self.book_inventory = {}
    self.user_information = {}
    self.author_information = {}
    self.genre_information = {}
    self.current_loans = {}
    self.conn = connect_database()
    self.cursor = self.conn.cursor(dictionary = True)

  def book_operations(self):
    if self.conn is not None:
      self.conn = connect_database()
    try:
      while True:
        self.cursor = self.conn.cursor()
        print("\nBook Operations Menu:\n1. Add a new book\n2. Borrow a book\n3. Return a book\n4. Search for a book\n5. Display all books\n6. Edit Book\n7. Exit")
        book_operation_choice = input("Please choose a menu option: ")
        if book_operation_choice == "1":
          Adding_information.add_book(self.book_inventory)
        elif book_operation_choice == "2":
          BookProcessing.checking_book_out(self.book_inventory, self.user_information, self.current_loans)
        elif book_operation_choice == "3":
          BookProcessing.returning_book(self.book_inventory, self.user_information, self.current_loans)
        elif book_operation_choice == "4":
          book_search = input("Enter book name to search: ").title()
          if book_search in self.book_inventory:
            BiographyBook.view_book(self.book_inventory[book_search])
          else:
            print("Book Not Found")
        elif book_operation_choice == "5":
          for info in self.book_inventory.values():
            BiographyBook.view_book(info)
        elif book_operation_choice == "6":
          EditInfo.edit_book(self.book_inventory)
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
        self.cursor = self.conn.cursor()
        print("\nUser Operations Menu:\n1. Add a new user\n2. View user details\n3. Display all users\n4. Edit User\n5. Exit")
        user_operation_choice = input("Please choose a menu option: ")
        if user_operation_choice == "1":
          Adding_information.add_user(self.user_information)
        elif user_operation_choice == "2":
          users_name = input("Enter users First and Last Name: ").title()
          if users_name not in self.user_information:
            print(f"{users_name} not found in User Data Base")
          else:
            User.view_user_details(self.user_information[users_name])
        elif user_operation_choice == "3":
          for user, user_info in self.user_information.items():
            User.view_user_details(user_info)
        elif user_operation_choice == "4":
          EditInfo.edit_user(self.author_information)
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
        self.cursor = self.conn.cursor()
        print("\nAuthor Operations:\n1. Add a new author\n2. View author details\n3. Display all authors\n4. Edit Author\n5. Exit")
        author_operation_choice = input("Please choose a menu option: ")
        if author_operation_choice == "1":
          Adding_information.add_author(self.author_information)
        elif author_operation_choice == "2":
          author_name = input("Enter Authors name: ").title()
          if author_name not in self.author_information:
            print(f"{author_name} not found in Author Data Base")
          else:
            Author.view_author_details(self.author_information[author_name])
        elif author_operation_choice == "3":
          for author, author_info in self.author_information.items():
            Author.view_author_details(author_info)
        elif author_operation_choice == "4":
          EditInfo.edit_author(self.author_information)
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
        self.cursor = self.conn.cursor()
        print("\nGenre Operations:\n1. Add a new genre\n2. View genre details\n3. Display all genres\n4. Edit Genre\n5. Exit")
        genre_operation_choice = input("Please choose a menu option: ")
        if genre_operation_choice == "1":
          Adding_information.add_genre(self.genre_information)
        elif genre_operation_choice == "2":
          genre_name = input("Enter Genre: ").title()
          if genre_name not in self.genre_information:
            print(f"{genre_name} not found in Genre Data Base")
          else:
            Genre.view_genre_details(self.genre_information[genre_name])
        elif genre_operation_choice == "3":
          for genre, genre_info in self.genre_information.items():
            Genre.view_genre_details(genre_info)
        elif genre_operation_choice == "4":
          EditInfo.edit_genre(self.genre_information)
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

  def adding_book_database(title,author_id,genre_id,isbn,publication_date,availability,cursor):
    search = " SELECT title FROM books WHERE title = %s"
    cursor.execute(search,(title,))
    matching = cursor.fetchone()
    if matching:
      print(f"'{title}' is already in Database")
    else:
      query = """INSERT INTO books (title,author_id,genre_id,isbn,publication_date,availability) VALUES (%s,%s,%s,%s,%s,%s)"""
      cursor.execute(query,(title,author_id,genre_id,isbn,publication_date,availability))
      

  def adding_user_database(name,library_id,cursor):
    search = " SELECT name FROM users WHERE name = %s"
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      print(f"'{name}' is already in Database")
    else:
      query = """INSERT INTO users (name,library_id) VALUES (%s,%s)"""
      cursor.execute(query,(name,library_id))


  def adding_author_database(name,biography,cursor):
    search = " SELECT name FROM authors WHERE name = %s"
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      print(f"'{name}' is already in Database")
    else:
      query = """INSERT INTO authors (name,biography) VALUES (%s,%s)"""
      cursor.execute(query,(name,biography))
      

  def adding_genre_database(name,description,category,cursor):
    search = " SELECT name FROM genres WHERE name = %s"
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      print(f"'{name}' is already in Database")
    else:
      query = """INSERT INTO genres (name,description,category) VALUES (%s,%s,%s)"""
      cursor.execute(query,(name,description,category))

  # def adding_borrowed_book_database(current_loans,cursor): # needs rework
  #   search = """SELECT user_id FROM borrowed_books WHERE user_id = %s and book_id = %s"""
  #   cursor.execute(search,(user_id,book_id))
  #   matching = cursor.fetchone()
  #   if matching:
  #     print(f"User with I.D. Number {user_id} or Book with I.D. Number {book_id}is not Checked out")
  #   else:
  #     query = """INSERT INTO borrowed_books (user_id,book_id,borrow_date,return_date) VALUES (%s,%s,%s,%s)"""
  #     cursor.execute(query,(user_id,book_id,borrow_date,return_date))

  def search_author_id():
    search = """SELECT name FROM authors WHERE id = %s"""

  def search_genre_id():
    search = """SELECT name FROM genres WHERE id = %s"""

  def search_user_id():
    search = """SELECT name FROM users WHERE id = %s"""

  def search_book_id():
    search = """SELECT title FROM books WHERE id = %s"""
  
  def search_borrowed_book_id(): # needs fixed
    search = """SELECT  FROM borrowed_books WHERE customer_id = %s"""

  def search_author_name(name,cursor):
    search = """SELECT id FROM authors WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching: 
      print(matching)
      return False
    else:
      return True

  def search_genre_name(name,cursor):
    search = """SELECT id FROM genres WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      print(matching)
      return False
    else:
      return True

  def search_user_name(name,cursor):
    search = """SELECT id FROM users WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      print(matching)
      return False
    else:
      return True

  def search_book_name(title,cursor):
    search = """SELECT id FROM books WHERE title = %s"""
    cursor.execute(search,(title,))
    matching = cursor.fetchone()
    if matching:
      print(matching)
      return False
    else:
      return True
  
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

  def add_book(book_inventory): # get this to add to data base but search author id with name and genre id with type of genre
    try:
      title = input("Enter Title of book: ").title()
      if title not in book_inventory:
        author = input("Enter Author of book: ").title()
        isbn = int(input("Enter ISBN: ")) 
        genre = input("Enter Genre of book: ").title()
        publication_date = input("Enter Publication Date [YYYY-MM-DD]: ").title()
        if genre == "Fiction":
          UserInterface.book_inventory[title] = FictionBook(title, author, isbn, genre, publication_date)
        elif genre == "Non-Fiction":
          UserInterface.book_inventory[title] = NonFictionBook(title, author, isbn, genre, publication_date)
        elif genre == "Biography":
          UserInterface.book_inventory[title] = BiographyBook(title, author, isbn, genre, publication_date)
        else:
          UserInterface.book_inventory[title] = Book(title, author, isbn, genre, publication_date)
      else:
        print(f"{title} is already in Book Database")
        
    except ValueError:
      print("Enter a 'Number' for the ISBN")

  def add_user(user_information):
    try:
      user_name = input("Enter First and Last Name of user to be added: ").title()
      if Adding_information.users_name_authenticator(user_name):
        if user_name not in user_information:
          library_id = int(input("Enter Library I.D. Number: ")) # UNIQUE need to run it up against other users
          user_information[user_name] = User(user_name,library_id)
        else:
          print(f"{user_name} is already in User Database")
    except ValueError:
      print("Enter a 'Number' for the Library I.D.")

  def add_author(author_information): # add into database
    author_name = input("Enter Name of Author to be added: ").title()
    if author_name not in author_information:
      biography = input("Enter biography for Author: ")
      author_information[author_name] = Author(author_name, biography)
    else:
      print(f"{author_name} is already in Author Data Base")

  def add_genre(genre_information): # add into database
    genre_name = input("Enter Genre: ").title()
    if genre_name not in genre_information:
      description = input("Enter Description of Genre: ").capitalize()
      category = input("Enter Genre Category: ").title()
      genre_information[genre_name] = Genre(genre_name,description,category)
    else:
      print(f"{genre_name} is already in Genre Data Base")

class BookProcessing:

  def checking_book_out(book_inventory,user_information,current_loans): # need to get this into database user id FK and book ID FK date borrowed and return(make the return auto) use string minpulation to do so
    user_search = input("Enter in User checking out book: ").title()
    book_search = input("Enter book name to Borrow: ").title()
    if book_search in book_inventory and user_search in user_information:
      if book_inventory[book_search].borrow_book():
        current_loans[book_search] = user_search
        user_information[user_search].adding_borrowed_books(book_search)
      else:
        print(f"'{book_search}' is already Checked Out")
    else:
      print(f"'{book_search}' is not in Library Data Base or '{user_search}' is not in Library Data Base")

  def returning_book(book_inventory,user_information,current_loans): # delete the borrowed book from the database
    user_returning_book = input("Enter Person Returning Book: ").title()
    book_return = input("Enter Book being returned: ").title()
    if book_return in current_loans and book_return in book_inventory and user_returning_book in user_information:
      book_inventory[book_return].return_book()
      user_information[user_returning_book].returning_borrowed_book(book_return)
      del current_loans[book_return]
    else:
      print(f"'{book_return}' is not checked out or '{user_returning_book}' is not in Library Data Base")

class EditInfo:

  def edit_book(book_info):
    book_name = input("Enter Book to Edit: ").title()
    if book_name not in book_info:
        print(f"{book_name} not found in Library Data Base")
    else:
      while True:
        try:
          print("Book Edit Menu:\n1. Author\n2. ISBN\n3. Genre\n4. Publication Date\n5. Change User Name\n6. Exit")
          book_edit_choice = input("Choose an option: ")
          if book_edit_choice == "1":
            author_edit = input("Enter Author Edit: ").title()
            book_info[book_name].set_author(author_edit)
          elif book_edit_choice == "2":
            isbn_edit = int(input("Enter New ISBN"))
            book_info[book_name].set_isbn(isbn_edit)
          elif book_edit_choice == "3":
            genre_edit = input("Enter New Genre: ").title()
            book_info[book_name].set_genre(genre_edit)
          elif book_edit_choice == "4":
            publication_date_edit = input("Enter New Publication Date YYYY-MM-DD: ")
            book_info[book_name].set_publication_date(publication_date_edit)
          elif book_edit_choice =="5":
            print("Coming Soon...")
            pass
          elif book_edit_choice == "6":
            print("Return to Book Menu...")
            break
          else:
            print("Invalid Choice")
        except ValueError:
          print("Enter a 'Number for ISBN")

  def edit_user(user_info):
    try:
      user_name = input("Enter Users First and Last Name to Edit: ").title()
      if user_name not in user_info:
        print(f"{user_name} not found in User Data Base")
      else:
        user_new_id= int(input("Enter new Library I.D. Number: "))
        user_info[user_name].set_library_id(user_new_id)
    except ValueError:
      print("Enter a 'Number' for the Library I.D.")

  def edit_author(author_info):
    author_name = input("Enter Author to edit: ").title()
    if author_name not in author_info:
      print(f"{author_name} not found in Author Data Base")
    else:
      author_edit = input("Enter New Biography: ")
      author_info[author_name].set_biography(author_edit)

  def edit_genre(genre_information):
    genre_name = input("Enter Genre to edit: ").title()
    if genre_name not in genre_information:
      print(f"{genre_name} not found in Genre Data Base")
    else:
      while True:
        print("Edit Genre Menu:\n1. Description\n2. Category\n3. Exit")
        edit_choice = input("Choose Menu Option: ")
        if edit_choice == "1":
          new_description = input(f"Enter new Description for {genre_name}: ").capitalize()
          genre_information[genre_name].set_description(new_description)
        elif edit_choice == "2":
          new_category = input(f"Enter new Category for {genre_name}: ").title()
          genre_information[genre_name].set_category(new_category)
        elif edit_choice == "3":
          print("Returning to Genre Menu...")
          break
        else:
          print("Invalid Input")