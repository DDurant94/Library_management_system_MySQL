from Book import Book as B
from BorrowedBooks import BorrowedBooks as BOB
from User import User as U
from DataError import BookError,UserError,BorrowedBookError

class BookProcessing:

  def checking_book_out(book_inventory):
    # checking books out of the Library
    try:
      user_search = input("Enter in User checking out book: ").title()
      user_id = U.search_user_name_for_id(user_search)
      book_search = input("Enter book name to Borrow: ").title()
      book_id = B.search_book_name_for_id(book_search)
      book_inventory[book_search].searching_book_availability(book_id)
      date = input("Enter todays Date [YYYY-MM-DD]: ")
      book_inventory[book_search].borrow_book()
      book_inventory[book_search].update_book_save()
      BOB.create_borrowed_books(user_id,book_id,date)
      print(f"'{book_search}' has been Checked Out to '{user_search}' on '{date}'")     
    except BookError as be:
      print(be)
    except UserError as ue:
      print(ue)
    except BorrowedBookError as bbe:
      print(bbe)
     
  def returning_book(book_inventory,borrowed_books):
    # Checking books back into library
    try:
      user_returning_book = input("Enter Person Returning Book: ").title()
      user_id = U.search_user_name_for_id(user_returning_book)
      book_return = input("Enter Book being returned: ").title()
      book_id = B.search_book_name_for_id(book_return)
      borrowed_book_id = BOB.getting_borrowed_book_id(book_id,user_id)
      if borrowed_book_id == False:
        print(f"'{book_return}' is not out on loan to '{user_returning_book}'")
      else:
        book_inventory[book_return].return_book()
        book_inventory[book_return].update_book_save()
        borrowed_books[borrowed_book_id].deleting_borrowed_book(borrowed_book_id)
        print(f"'{book_return}' has been Checked In")
    except BookError as be:
      print(be)
    except UserError as ue:
      print(ue)