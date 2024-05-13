from Author import Author as A
from Book import Book as B
from BorrowedBooks import BorrowedBooks as BOB
from DataError import AuthorsError,BookError,GenreError,UserError
from Genre import Genre as G
from User import User as U

class EditInfo:

  def edit_book(book_inventory):
    try:
      book_name = input("Enter Book Title to Edit: ").title()
      B.search_book_name_for_id(book_name)
      while True:
          print("Book Edit Menu:\n1. Edit Author\n2. Edit ISBN\n3. Edit Genre\n4. Edit Publication Date\n5. Edit Title\n6. Exit")
          book_edit_choice = input("Choose an option: ")
          if book_edit_choice == "1":
            try:
              author_edit = input("Enter Author First and Last To Change To: ").title()
              author_id = A.search_author_name_for_id(author_edit)
              book_inventory[book_name].set_author_id(author_id)
            except AuthorsError as ae:
              print(f"{ae}. Add '{author_edit}' or Choose Author that is in Author Database")
          elif book_edit_choice == "2":
            isbn_edit = int(input("Enter New ISBN: "))
            checking_isbn = B.matching_isbn(isbn_edit)
            if checking_isbn == False:
              book_inventory[book_name].set_isbn(isbn_edit)
            else:
              print(f"I.S.B.N. number '{isbn_edit}' is already linked to '{checking_isbn[0]}' choose different I.S.B.N.")
          elif book_edit_choice == "3":
            try:
              genre_edit = input("Enter New Genre: ").title()
              genre_id = G.search_genre_name_for_id(genre_edit)
              book_inventory[book_name].set_genre_id(genre_id)
            except GenreError as ge:
              print(ge)
          elif book_edit_choice == "4":
            publication_date_edit = input("Enter New Publication Date [YYYY-MM-DD]: ")
            book_inventory[book_name].set_publication_date(publication_date_edit)
          elif book_edit_choice == "5":
            title_edit = input("Enter Title edit: ").title()
            book_inventory[book_name].set_title(title_edit)
          elif book_edit_choice == "6":
            book_inventory[book_name].update_book_save()
            print("Return to Book Menu...")
            break
          else:
            print("Invalid Choice")
    except ValueError:
      print("Enter a 'Number for ISBN")
    except BookError as be:
      print(be)

  def edit_user(user_info):
    try:
      user_name = input("Enter Users First and Last Name to Edit: ").title()
      U.search_user_name_for_id(user_name)
      while True:
        print("User Edit Menu:\n1. Edit Name\n2. Edit Library I.D.\n3. Exit")
        edit_user_choice = input("Choose Menu Option: ")
        if edit_user_choice == "1":
          new_name = input(f"Enter '{user_name}s' new First and Last Name: ").title()
          if new_name in user_info:
            print(f"'{new_name}' is already in User Database")
          else:
            user_info[user_name].set_users_name(new_name)
        elif edit_user_choice == "2":
          user_new_id= int(input("Enter new Library I.D. Number: "))
          if U.search_library_ids(user_new_id):
            print(f"Library I.D. '{user_new_id}' is already taken")
          else:
            user_info[user_name].set_library_id(user_new_id)
        elif edit_user_choice == "3":
          user_info[user_name].update_users_save()
          print("Returning to User Menu...")
          break
        else:
          print("Invalid Choice")
    except ValueError:
      print("Enter a 'Number' for the Library I.D.")
    except UserError as ue:
      print(ue)

  def edit_author(author_info):
    try:
      author_name = input("Enter Author First and Last Name to edit: ").title()
      A.search_author_name_for_id(author_name)
      while True:
        print("Author Edit Menu:\n1. Edit Name\n2. Edit Biography\n3. Exit")
        author_edit_choice = input("Choose Menu Option: ")
        if author_edit_choice == "1":
          new_author_name = input(f"Enter '{author_name}s' First and Last Name: ").title()
          if new_author_name in author_info:
            print(f"'{new_author_name}' already in Author Data Base")
          else:
            author_info[author_name].set_author_name(new_author_name)
        elif author_edit_choice == "2":
          author_edit = input("Enter New Biography: ")
          author_info[author_name].set_biography(author_edit)
        elif author_edit_choice == "3":
          author_info[author_name].update_author_save()
          print("Returning to Author Menu...")
          break
        else:
          print("Invalid Choice")
    except AuthorsError as ae:
      print(ae)

  def edit_genre(genre_information):
    try:
      genre_name = input("Enter Genre to edit: ").title()
      G.search_genre_name_for_id(genre_name)
      while True:
        print("Edit Genre Menu:\n1. Edit Genre Name\n2. Edit Description\n3. Edit Category\n4. Exit")
        edit_choice = input("Choose Menu Option: ")
        if edit_choice == "1":
          new_name = input(f"Enter '{genre_name}' new Name: ").title()
          if new_name in genre_information:
            print(f"'{new_name}' is already in Genre Database")
          else:
            genre_information[genre_name].set_genre_name(new_name)
        elif edit_choice == "2":
          new_description = input(f"Enter new Description for '{genre_name}': ").capitalize()
          genre_information[genre_name].set_description(new_description)
        elif edit_choice == "3":
          new_category = input(f"Enter new Category for '{genre_name}': ").title()
          genre_information[genre_name].set_category(new_category)
        elif edit_choice == "4":
          genre_information[genre_name].update_genres_save()
          print("Returning to Genre Menu...")
          break
        else:
          print("Invalid Input")
    except GenreError as ge:
      print(ge)

  def edit_borrowed_book(borrowed_books_information):
    try:
      book_title = input("Enter Borrowed Book Title to Edit: ")
      book_id = B.search_book_name_for_id(book_title)
      borrowed_book_id = BOB.getting_borrowed_book_id_delete_edit(book_id)
      if borrowed_book_id == False:
        print(f"'{book_title}' is not in Borrowed Books")
      else:
        while True:
          print("Borrowed Book Menu:\n1. Edit User\n2. Edit Borrow Date\n3. Edit Return Date\n4. Exit")
          borrowed_book_edit_choice = input("Choose Menu Option: ")
          if borrowed_book_edit_choice == "1":
            try:
              user_edit = input(f"Enter New User First and Last Name Who Loaned '{book_title}': ")
              user_id = U.search_user_name_for_id(user_edit)
              borrowed_books_information[borrowed_book_id].set_user_id(user_id)
            except UserError as ue:
              print(f"{ue}")
          elif borrowed_book_edit_choice == "2":
            new_borrow_date = input("Enter New Borrow Date [YYYY-MM-DD]: ")
            borrowed_books_information[borrowed_book_id].set_borrow_date(new_borrow_date)
          elif borrowed_book_edit_choice == "3":
            new_return_date = input("Enter New Return Date [YYYY-MM-DD]: ")
            borrowed_books_information[borrowed_book_id].set_return_date(new_return_date)
          elif borrowed_book_edit_choice == "4":
            borrowed_books_information[borrowed_book_id].update_borrowed_books_save()
            print("Returning Borrowed Book Menu...")
            break
          else:
            print("Invalid Input")
    except BookError as be:
      print(be)