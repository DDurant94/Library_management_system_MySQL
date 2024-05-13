from DataError import GenreError
from connect_mysql import connect_database
conn = connect_database()
cursor = conn.cursor()

class Genre:
  def __init__(self,genre_name,description,category,id = None):
    self._id = id
    self._genre_name = genre_name
    self._description = description
    self._category = category

  def update_genres_save(self):
    # updating MySQL after editing 
    updating_genre = '''UPDATE genres SET name = %s, description = %s, category = %s WHERE id = %s'''
    cursor.execute(updating_genre,(self.get_genre_name(),self.get_description(),self.get_category(),self.get_genre_id()))
    conn.commit()
    print(f"'{self.get_genre_name()}' as been Updated")
 
  def save_genres_sql(self):
    # Saving to MySQL when adding info with a fail safe to check if genre is in database
    search = " SELECT name FROM genres WHERE name = %s"
    cursor.execute(search,(self.get_genre_name(),))
    matching = cursor.fetchone()
    if matching:
      print(f"'{self.get_genre_name()}' is already in Database")
    else:
      adding_genres_sql = """INSERT INTO genres (name,description,category) VALUES (%s,%s,%s)"""
      cursor.execute(adding_genres_sql,(self.get_genre_name(),self.get_description(),self.get_category()))
      conn.commit()
      print(f"Genre '{self.get_genre_name()}' was added to Database")

  @classmethod
  def create_genres(cls,name,description,category):
    # making info enter into an object of genres and then runs info into MySQL to be saved
    new_instance_genres = cls(name,description,category)
    new_instance_genres.save_genres_sql()
    return new_instance_genres

  @classmethod 
  def create_from_database_genres(cls,genres_rows):
    # making rows in class objects to than be used within the program with dicts
    new_instance_genres_ = cls(genres_rows[1],genres_rows[2],genres_rows[3])
    new_instance_genres_._id = genres_rows[0]
    return new_instance_genres_

  @classmethod 
  def get_genres_rows(cls):
    # taking each row from MySql and passing it to create_from_database_genres and returning info to my dicts as objects
    fetching_genres = '''SELECT * FROM genres'''
    cursor.execute(fetching_genres)
    genres_table_rows = cursor.fetchall()
    return [cls.create_from_database_genres(row) for row in genres_table_rows],[row[1] for row in genres_table_rows]
  
  @classmethod 
  def search_genre_name_for_id(cls,name):
    # taking a genre name and searching for its id
    search = """SELECT id FROM genres WHERE name = %s"""
    cursor.execute(search,(name,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      raise GenreError(f"'{name}' not found in Genre Database")
    
  @classmethod 
  def search_genre_id_for_name(cls,id):
    # taking a genre id and searching for its name
    search = """SELECT name FROM genres WHERE id = %s"""
    cursor.execute(search,(id,))
    matching = cursor.fetchone()
    if matching:
      return matching[0]
    else:
      raise GenreError(f"'{cls.get_genre_name()}' not found in Genre Database")
    
  @classmethod
  def deleting_genre(cls,genre_id):
    delete = """DELETE FROM genres WHERE id = %s"""
    cursor.execute(delete,(genre_id,))
    conn.commit()

  @classmethod 
  def getting_titles_with_genre(cls,genre_id):
    # getting all the books that are linked to this genre
    search = """SELECT b.title
    from books as b
    JOIN genres as g
    ON b.genre_id = g.id
    WHERE g.id = %s
    """
    cursor.execute(search,(genre_id,))
    matching = cursor.fetchall()
    return matching

  def get_genre_id(self):
    return self._id

  def get_genre_name(self):
        return self._genre_name

  def get_description(self):
      return self._description

  def get_category(self):
      return self._category
  
  def set_genre_name(self,new_name):
    self._genre_name = new_name

  def set_description(self, new_description):
      self._description = new_description

  def set_category(self, new_category):
      self._category = new_category

  def view_genre_details(self):
    print(f"\nGenre: {self.get_genre_name()}\nGenre I.D. Number: {self.get_genre_id()}\nDescription:\n{self.get_description()}\nCategory: {self.get_category()}\n")