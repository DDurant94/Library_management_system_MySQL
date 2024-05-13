# Error Handling classes for each type of object that is created
class UserError(Exception):
  def __init__ (self,value):
    self.value = value

class BookError(Exception):
  def __init__ (self,value):
    self.value = value

class BorrowedBookError(Exception):
  def __init__ (self,value):
    self.value = value

class GenreError(Exception):
  def __init__ (self,value):
    self.value = value

class AuthorsError(Exception):
  def __init__ (self,value):
    self.value = value