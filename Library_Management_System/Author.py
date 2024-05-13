from DataError import AuthorsError
from connect_mysql import connect_database
conn = connect_database()
cursor = conn.cursor()

class Author:
  def __init__ (self, author_name, biography,id = None):
    self.__id = id
    self._author_name = author_name
    self._biography = biography

  def update_author_save(self):
    # Updating info that has been edited and saving it back to MySQL
    updating_author = '''UPDATE authors SET name = %s,biography = %s WHERE id = %s'''
    cursor.execute(updating_author,(self.get_author_name(),self.get_biography(),self.get_author_id()))
    conn.commit()
    print(f"'{self.get_author_name()}' as been Updated")
    
  def save_authors_sql(self):
    # saving info that is has be added in when making an object with a fail safe to check if the author is already in database
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
    # saving info that is add and saving it to MySQL database
    new_instance_authors = cls(name,biography)
    new_instance_authors.save_authors_sql()
    return new_instance_authors
  
  @classmethod
  def create_from_database_authors(cls,authors_rows):
    # creating info from database making that info into a class object
    new_instance_authors_ = cls(authors_rows[1],authors_rows[2])
    new_instance_authors_.__id = authors_rows[0]
    return new_instance_authors_

  @classmethod
  def get_authors_rows(cls):
    # grabbing all rows from author in Database
    fetching_authors = '''SELECT * FROM authors'''
    cursor.execute(fetching_authors)
    authors_table_rows = cursor.fetchall()
    return [cls.create_from_database_authors(row) for row in authors_table_rows],[row[1] for row in authors_table_rows]
  
  @classmethod
  def search_author_name_for_id(cls,name):
    # getting id by using author name
    search = """SELECT id FROM authors WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching: 
      return matching[0]
    else:
      raise AuthorsError(f"'{name}' Not Found in Author Database")
    
  @classmethod
  def search_author_id_for_name(cls,id):
    # getting name of author by using the author ID
    search = """SELECT name FROM authors WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return True, matching[0]
    else:
      raise AuthorsError(f"'{cls.get_author_name()}' Not Found in Author Database")
    
  @classmethod
  def getting_titles_author_wrote(cls,author_id):
    # Grabbing all title that author has wrote
    search = """SELECT b.title
    from books as b
    JOIN authors as a
    ON b.author_id = a.id
    WHERE a.id = %s
    """
    cursor.execute(search,(author_id,))
    matching = cursor.fetchall()
    return matching

  @classmethod
  def deleting_author(cls,author_id):
    delete = """DELETE FROM authors WHERE id = %s"""
    cursor.execute(delete,(author_id,))
    conn.commit()

  def get_author_id(self):
    return self.__id

  def get_author_name(self):
    return self._author_name
  
  def get_biography(self):
    return self._biography
  
  def set_author_name(self,new_name):
    self._author_name = new_name
  
  def set_biography(self,new_biography):
    self._biography = new_biography
  
  def view_author_details(self):
    print(f"Name: {self.get_author_name()}\nAuthor I.D.: {self.get_author_id()}\nBiography:\n{self.get_biography()}\n")