import re
from Book import Book as B
from Book import FictionBook as FB
from Book import NonFictionBook as NFB
from Book import BiographyBook as BB
from DataError import BookError,UserError
from Genre import Genre as G
from User import User as U
from Author import Author as A
from BorrowedBooks import BorrowedBooks as BOB

class AddingInfo:
  def users_name_authenticator(user_name):
    users_name_standard = r"^\w{2,15}\s\w{2,15}$"
    matching_users_name = re.match(users_name_standard,user_name)
    if matching_users_name:
      return True
    else:
      return False

  def add_book(author_information,genre_information,book_inventory):
    try:
      title = input("Enter Title of book: ").title()
      if title in book_inventory:
        print(f"'{title}' is in Library Inventory Database")
      else:
        author = input("Enter Author First and Last Name of book: ").title()
        isbn = int(input("Enter ISBN: "))
        checking_isbn = B.matching_isbn(isbn)
        if checking_isbn == False:
          genre = input("Enter Genre of book: ").title()
          publication_date = input("Enter Publication Date [YYYY-MM-DD]: ").title()
          if genre in genre_information:
            print("right path")
            genre_id = G.search_genre_name_for_id(genre)
          else:
            G.create_genres(genre,None,None)
            genre_id = G.search_genre_name_for_id(genre)
          if author in author_information:
            author_id = A.search_author_name_for_id(author)
          else:
            A.create_authors(author,None)
            author_id = A.search_author_name_for_id(author)
          if genre == "Fiction":
            FB.create_book(title, author_id, genre_id, isbn, publication_date)
          elif genre == "Non-Fiction":
            NFB.create_book(title, author_id, genre_id, isbn, publication_date)
          elif genre == "Biography":
            BB.create_book(title, author_id, genre_id, isbn, publication_date)
          else:
            B.create_book(title, author_id, genre_id, isbn, publication_date)
        else:
          print(f"I.S.B.N. number '{isbn}' is already linked to '{checking_isbn[0]}' choose different I.S.B.N.")      
    except ValueError:
      print("Enter a 'Number' for the I.S.B.N.")

  def add_user():
    try:
      user_name = input("Enter First and Last Name of user to be added: ").title()
      if AddingInfo.users_name_authenticator(user_name):    
        library_id = int(input("Enter Library I.D. Number: "))
        if U.search_library_ids(library_id):
          print(f"Library I.D. '{library_id}' is already taken")
        else:
          U.create_users(user_name,library_id)
      else:
        print("Format of Users Name is wrong. [Ex. Daniel Durant]")
    except ValueError:
      print("Enter a 'Number' for the Library I.D.")

  def add_author():
    author_name = input("Enter First and Last Name of Author to be added: ").title()
    biography = input("Enter biography for Author: ")
    A.create_authors(author_name, biography)

  def add_genre():
    genre_name = input("Enter Genre: ").title()
    description = input("Enter Description of Genre: ").capitalize()
    category = input("Enter Genre Category: ").title()
    G.create_genres(genre_name,description,category)

  def add_borrowed_book(book_inventory):
    try:
      book_title = input("Enter Book Title: ").title()
      book_id = B.search_book_name_for_id(book_title)
      user_name = input(f"Enter Users First and Last name Borrowing '{book_title}': ").title()
      user_id = U.search_user_name_for_id(user_name)
      if book_inventory[book_title].searching_book_availability(book_id):
        date = input("Enter todays Date [YYYY-MM-DD]: ")
        book_inventory[book_title].borrow_book()
        book_inventory[book_title].update_book_save()
        BOB.create_borrowed_books(user_id,book_id,date)
        print(f"'{book_title}' was manual borrowed out to '{user_name}' on '{date}'")
    except BookError as be:
      print(be)
    except UserError as ue:
      print(ue)
