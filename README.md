# Library Managment System

Author: Daniel Durant

# Imports/Installs:
Python: https://www.python.org/downloads/
MySQL: https://dev.mysql.com/downloads/
PIP: https://packaging.python.org/en/latest/tutorials/installing-packages/
pip install mysql-connector-python
Import: mysql.connector, from mysql.connector import Error, and Regex (import re)



# Intro:
LIbrary Management System is a Python based program that is integrated with a MySQL database to allow for a smooth and safe storage of information. This is a Command line program for
Library Management allowing for Books, Authors, Genres, and Users to be added and used within this system. This is a program that a Librarian would use to manage their 
Library. The program can eaisly be scaled up to allow for a user interface program to be added in the future. Making the information that only customers would be able to see 
and interact with within the library. The module disign of this program allows for programers to move between each of the functions and make changes as needed or add 
new functions to the program with easy. 

# Intergration of Library Managment System:
Installation and Setup:
First, ensure you have Python installed on your system (it usually comes pre-installed on most Linux computers and Macs).
Next, install the MySQL Connector/Python library. You can obtain it from the official MySQL website or use pip to install it directly:
pip install mysql-connector-python
Verify your installation by importing the library in your Python script.
Connecting to MySQL:
To establish a connection to your MySQL server, use the necessary connection details (hostname, username, password, etc.): (Provided once customer decides to use this program 
within their system) Once LMS is intergraded the staff of the library will be able to add in information regarding to that library or transfer information from their old database.

# Library Managment System Features:
Books:
1. Adding:
Each book needs a Title, Author, ISBN, Genre, Publication Date, Availability (auto set availabile when adding a new book). When adding a book it will auto add a Genre and or
Author to the database. That is not the case when editing but only when adding a book into the database.
3. Editing:
Each book can be edited from the title the availability.
4. Viewing:
Each book can be viewed on its own or the user can view the whole library. (Future updates of viewing: View By Author, View By Genre, View By Letter/Letters, View By Availability)
5. Checking in/out:
Ability to check books in or out.
6. Delteing Book:
Ability to remove books

Users:
1. Adding:
Each users needs a First and Last name (authenticator for name to chack if it meets standards), and Library ID. (Future updates: Account Balance for Late Fees.
After a set amount user can not check out books)
2. Editing:
Each user can be edited and ajusted in all aspects.
3. Viewing:
Each user can be viewed showing Name, Library ID, Database ID, and Book that person has checked out.
4. Deleting:
Ability to remove users

Genres:
1. Adding:
Each Genre only needs a name. The Category and Description are optional. Both can be added in at the time being add or later Date.
2. Editing:
Each Genre can be edited and ajusted in all aspects.
3. Viewing:
Each Genre when view shows Genre Name, ID, Category, and Description (Future updates of viewing: Showing all book in Genre)
4. Deleting:
Deleteing a Genre can only be done if there is no book in the database with that Genre. 

Authors:
1. Adding:
Each Author only needs a Name. The Biography is optional and can be added at a later date.
2. Editing:
Each Author can be edited and ajusted in all aspects.
3. Viewing:
Each Author when view shows Author Name, ID, and Biography (Future updates of viewing: Showing all book That have the Author linked to them)
4. Deleting:
Deleteing a Genre can only be done if there is no book in the database with that Author. 

Borrowed Books:
1. Adding:
When adding a borrowed book from Borrowed Books Menu, it's to be noted that it is doing so manually and not from the book oporations. Checking in or out a book you will need User
First and Last Name, Title, and Date of check out (Return date is auto set to none). When Adding Menually the same will apply.
(Future updates: Adding Auto Return Date (Length set by Library), Late Fees (Amount set by Library), and Warnings for users with outstanding balance) 
2. Editing:
When editing a book that is out on loan you can change User, Checkout Date, and Return Date.
3. Viewing:
When viewing borrowed books you can either search for a book thats been checked out or view all books that are out on loan. When viewing you will see Book Title, Book ID, User Name,
User ID, Borrow Date, Return Date, Borrow ID. (Future updates of viewing: View by due date, and View by checkout date) 
4. Deleting:
Deleteing a Borrowed book is done manually or when the book is checked back in.

Error Handling:
When the program runs into a issue with user input the program will prompt the user with a message explaining what has happened and in some case what they can do to fix the problem 
(Ex. 'Author' is not in Database. Add 'Author' or choose a different Author)

# How to Use Library Management System:
The user will be promped with menu options and inputs that will need to be followed. The program has ex. for the user to see and will need to match for the program to under stand 
the input. The command line program makes it easy for the user to follow along and run. If the user enters in the wrong kind of input the program will let them know what they have
done wrong.

# Menu Options:
Main Menu:
1. Book Operations
2. User Operations
3. Author Operations
4. Genre Operations
5. Borrowed Book Operations
6. Quit

Book Operations:                    Book Edit Menu:
1. Add New Book                     1. Edit Author
2. Borrow Book                      2. Edit ISBN
3. Return Book                      3. Edit Genre
4. Search For Book                  4. Edit Publication Date
5. Display All Books                5. Edit Title
6. Edit Book                        6. Exit
8. Delete Book
9. Exit

User Operations:                    User Edit Menu:
1. Add New User                     1. Edit Name
2. View User Details                2. Edit Library I.D.
3. Display All Users                3. Exit
4. Edit User
5. Delete User
6. Exit

Author Operations:                  Author Edit Menu:
1. Add New Author                   1. Edit Name
2. View Author Details              2. Edit Biography
3. Display All Authors              3. Exit
4. Edit Author
5. Delete Author
6. Exit

Genre Operations:                   Edit Genre Menu:
1. Add New Genre                    1. Edit Genre Name
2. View Genre Details               2. Edit Description
3. Display All Genres               3. Edit Category
4. Edit Genre                       4. Exit
5. Delete Genre
6. Exit

Borrowed Books Operations:          Borrowed Book Menu:
1. Add Borrowed Book Manually       1. Edit User
2. Edit Borrowed Book               2. Edit Borrow Date
3. View Borrowed Book               3. Edit Return Date
4. View All Borrowed Books          4. Exit
5. Delete Borrowed Book             
6. Exit

# Conclusion
Congratulations! You now have a basic understanding of the Library Management System. Feel free to explore and enhance the system as needed. Happy managing!
