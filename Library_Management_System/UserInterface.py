from AddingInfo import AddingInfo as AI
from Author import Author as A
from Book import Book as B,FictionBook as FB,NonFictionBook as NF,BiographyBook as BB
from BookProcessing import BookProcessing as BP
from BorrowedBooks import BorrowedBooks as BOB
from connect_mysql import connect_database
from DataError import GenreError
from DeleteInfo import DeleteInfo as DI
from EditInfo import EditInfo as EI
from Genre import Genre as G
from User import User as U
conn = connect_database()
cursor = conn.cursor()
# main user interface all modules run out of this collection of functions
class UserInterface:
  def __init__ (self):
    self.book_inventory = {}
    self.user_information = {}
    self.author_information = {}
    self.genre_information = {}
    self.borrowed_books_information = {}
    self.conn = connect_database()
    self.cursor = conn.cursor()

  def book_operations(self):
    if self.conn is not None:
      self.conn = connect_database()
    try:
      while True:
        self.populating_dicts()
        self.cursor = conn.cursor()
        print("\nBook Operations Menu:\n1. Add New Book\n2. Borrow Book\n3. Return Book\n4. Search For Book\n5. Display All Books\n6. Edit Book\n7. Delete Book\n8. Exit")
        book_operation_choice = input("Please choose a menu option: ")
        if book_operation_choice == "1":
          AI.add_book(self.author_information,self.genre_information,self.book_inventory)
        elif book_operation_choice == "2":
          BP.checking_book_out(self.book_inventory)
        elif book_operation_choice == "3":
          BP.returning_book(self.book_inventory,self.borrowed_books_information)
        elif book_operation_choice == "4":
          book_search = input("Enter book name to search: ").title()
          if book_search in self.book_inventory.keys():
            BB.view_book(self.book_inventory[book_search])
          else:
            print(f"'{book_search}' not found in Library Book Database")  
        elif book_operation_choice == "5":
          for book_ in self.book_inventory.values():
            BB.view_book(book_) 
        elif book_operation_choice == "6":
          EI.edit_book(self.book_inventory)
        elif book_operation_choice == "7":
          DI.delete_book()
        elif book_operation_choice == "8":
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
        self.populating_dicts()
        self.cursor = conn.cursor()
        print("\nUser Operations Menu:\n1. Add New User\n2. View User Details\n3. Display All Users\n4. Edit User\n5. Delete User\n6. Exit")
        user_operation_choice = input("Please choose a menu option: ")
        if user_operation_choice == "1":
          AI.add_user()
        elif user_operation_choice == "2":
          users_name = input("Enter users First and Last Name: ").title()
          if users_name in self.user_information.keys():
            U.view_user_details(self.user_information[users_name])
          else:
            print(f"'{users_name}' is not found in Users Database")
        elif user_operation_choice == "3":
          users_ = U.get_users_rows()
          if users_ is not None:
            [U.view_user_details(user_) for user_ in users_[0]]
        elif user_operation_choice == "4":
          EI.edit_user(self.user_information)
        elif user_operation_choice == "5":
          DI.delete_user()
        elif user_operation_choice == "6":
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
        self.populating_dicts()
        self.cursor = conn.cursor()
        print("\nAuthor Operations:\n1. Add New Author\n2. View Author Details\n3. Display All Authors\n4. Edit Author\n5. Delete Author\n6. Exit")
        author_operation_choice = input("Please choose a menu option: ")
        if author_operation_choice == "1":
          AI.add_author()
        elif author_operation_choice == "2":
          author_name = input("Enter Authors name: ").title()
          if author_name in self.author_information.keys():
            A.view_author_details(self.author_information[author_name])
          else:
            print(f"'{author_name}' is not in Author Database")
        elif author_operation_choice == "3":
          authors_ = A.get_authors_rows()
          if authors_ is not None:
            [A.view_author_details(author_) for author_ in authors_[0]]
        elif author_operation_choice == "4":
          EI.edit_author(self.author_information)
        elif author_operation_choice == "5":
          DI.delete_author()
        elif author_operation_choice == "6":
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
          self.populating_dicts()
          self.cursor = conn.cursor()
          print("\nGenre Operations:\n1. Add New Genre\n2. View Genre Details\n3. Display All Genres\n4. Edit Genre\n5. Delete Genre\n6. Exit")
          genre_operation_choice = input("Please choose a menu option: ")
          if genre_operation_choice == "1":
            AI.add_genre()
          elif genre_operation_choice == "2":
            genre_name = input("Enter Genre: ").title()
            if genre_name in self.genre_information.keys():
              G.view_genre_details(self.genre_information[genre_name])
            else:
              print(f"'{genre_name}' is not in Genre Database")
          elif genre_operation_choice == "3":
            genres_ = G.get_genres_rows()
            if genres_ is not None:
              [G.view_genre_details(genre) for genre in genres_[0]]
          elif genre_operation_choice == "4":
            EI.edit_genre(self.genre_information)
          elif genre_operation_choice == "5":
            DI.delete_genre()
          elif genre_operation_choice == "6":
            print("Returning to Main Menu...")
            self.conn.commit()
            break
          else:
            print("Invalid Choice")
      except GenreError as ge:
        print(ge)
      except Exception as e:
        print(f"Error: {e}")
      finally:
        self.cursor.close()
        self.conn.close()

  def borrowed_books_operations(self):
      if self.conn is not None:
        self.conn = connect_database()
      try:
        while True:
          self.populating_dicts()
          print("Borrowed Books Menu:\n1. Add Borrowed Book Manually\n2. Edit Borrowed Book\n3. View Borrowed Book\n4. View All Borrowed Books\n5. Delete Borrowed Book\n6. Exit")
          borrowed_book_menu_option = input("Choose Menu Option: ")
          if borrowed_book_menu_option == "1":
            AI.add_borrowed_book(self.book_inventory)
          elif borrowed_book_menu_option == "2":
            EI.edit_borrowed_book(self.borrowed_books_information)
          elif borrowed_book_menu_option == "3":
            book_title = input("Enter Book Title to search: ").title()
            book_id = B.search_book_name_for_id(book_title)
            if book_id == None:
              print(f"'{book_title}' is not out on loan")
            else:
              BOB.view_borrowed_books(self.borrowed_books_information[book_id])
          elif borrowed_book_menu_option == "4":
            borrowed_books_ = BOB.get_borrowed_books_rows()
            if borrowed_books_ is not None:
              [BOB.view_borrowed_books(borrowed_book) for borrowed_book in borrowed_books_[0]]
            else:
              print("\nNo Books Checked Out\n")
          elif borrowed_book_menu_option == "5":
            DI.delete_borrowed_book(self.book_inventory)
          elif borrowed_book_menu_option == "6":
            self.conn.commit()
            print("Returning to Main Menu...")
            break
          else:
            print("Invalid Input")
      except Exception as e:
        print(f"Error: {e}")
      finally:
        self.cursor.close
        self.conn.close()

  def populating_dicts(self):
    # This function populates all of my dicts from MySQL
    # Genres
    genres = G.get_genres_rows()
    for genre in genres[0]:
      self.genre_information[genre.get_genre_name()] = genre

    # Authors
    authors = A.get_authors_rows()
    for author in authors[0]:
      self.author_information[author.get_author_name()] = author

    # Base Book Class
    books = B.get_book_rows()
    for book in books[0]:
      if book is not None:
        self.book_inventory[book.get_title()] = book

    # Fiction Book Class
    fic_books = FB.get_book_rows()
    for fic_book in fic_books[0]:
      if fic_book is not None:
        self.book_inventory[fic_book.get_title()] = fic_book

    # Biography Book Class
    bio_books = BB.get_book_rows()
    for bio_book in bio_books[0]:
      if bio_book is not None:
        self.book_inventory[bio_book.get_title()] = bio_book

    # Non Fiction Book Class
    non_fic_books = NF.get_book_rows()
    for non_book in non_fic_books[0]:
      if non_book is not None:
        self.book_inventory[non_book.get_title()] = non_book

    # Borrowed Book Class    
    borrowed_books = BOB.get_borrowed_books_rows()
    if borrowed_books is not None:
      for borrowed_book in borrowed_books[0]:
        self.borrowed_books_information[borrowed_book.get_id()] = borrowed_book
        
    # Users Class
    users = U.get_users_rows()
    for user in users[0]:
      self.user_information[user.get_user_name()] = user