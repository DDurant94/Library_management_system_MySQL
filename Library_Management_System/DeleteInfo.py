from Author import Author as A
from Book import Book as B
from BorrowedBooks import BorrowedBooks as BOB
from DataError import AuthorsError,BookError,GenreError,UserError
from Genre import Genre as G
from User import User as U

class DeleteInfo:
  def delete_book():
    try:
      title = input("Enter Book Title To Delete: ").title()
      book_id = B.search_book_name_for_id(title)
      B.deleting_book(book_id)
      print(f"'{title}' has been Deleted from Book Inventory")
    except BookError as be:
      print(be)
    except Exception:
      print(f"'{title}' is checked out and can not be Deleted")

  def delete_user():
    try:
      user_name = input("Enter User To Delete: ").title()
      user_id = U.search_user_name_for_id(user_name)
      U.deleting_user(user_id)
      print(f"'{user_name}' has been Deleted from Users")
    except UserError as ue:
      print(ue)
    except Exception:
      print(f"'{user_name}' Can not be delete with books checked out")

  def delete_author():
    try:
      author_name = input("Enter Author To Delete: ").title()
      author_id = A.search_author_name_for_id(author_name)
      A.deleting_author(author_id)
      print(f"'{author_name}' has been Deleted From Authors")
    except AuthorsError as ae:
      print(ae)
    except Exception:
      print(f"Can not Delete '{author_name}'! They are linked to:")
      for match in A.getting_titles_author_wrote(author_id):
        print(f"'{match[0]}'")

  def delete_genre():
    try:
      genre_title = input("Enter Genre To Delete: ").title()
      genre_id = G.search_genre_name_for_id(genre_title)
      G.deleting_genre(genre_id)
      print(f"'{genre_title}' has been Deleted from Genres")
    except GenreError as ge:
      print(ge)
    except Exception:
      print(f"Can not Delete '{genre_title}'! '{genre_title}' is linked to:")
      for match in G.getting_titles_with_genre(genre_id):
        print(f"'{match[0]}'")
      
  def delete_borrowed_book(book_inventory):
    try:
      book_title = input("Enter Book Title to Delete: ").title()
      book_id = B.search_book_name_for_id(book_title)
      borrowed_book_id = BOB.getting_borrowed_book_id_delete(book_id)
      if borrowed_book_id == False:
        print(f"'{book_title}' not found in borrowed book Database")
      else:
        book_inventory[book_title].return_book()
        book_inventory[book_title].update_book_save()
        BOB.deleting_borrowed_book(borrowed_book_id)
        print(f"'{book_title}' has been Deleted from Borrowed Books")
    except BookError as be:
      print(be)