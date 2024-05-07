from Library import UserInterface as UI

def main():
  start_up = UI()
  print("Welcome to the Library Management System!")
  while True:
    print("\nMain Menu:\n1. Book Operations\n2. User Operations\n3. Author Operations\n4. Genre Operations\n5. Quit")
    menu_choice = input("Please choose a menu option: ")
    if menu_choice == "1":
      UI.book_operations(start_up)
    elif menu_choice == "2":
      UI.user_operations(start_up)
    elif menu_choice == "3":
      UI.author_operations(start_up)
    elif menu_choice == "4":
      UI.genre_operations(start_up)
    elif menu_choice == "5":
      print("Thank you for using Library Management System")
      break
    else:
      print("Invalid Choice")

main()