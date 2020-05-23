import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import and_

DB_PATH = "sqlite:///albums.sqlite3"
Base = declarative_base()


class Album(Base):
    """
    Описывает структуру таблицы album для хранения записей музыкальной библиотеки
    """
    __tablename__ = "album"

    id = sa.Column(sa.INTEGER, primary_key=True)
    year = sa.Column(sa.INTEGER)
    artist = sa.Column(sa.TEXT)
    genre = sa.Column(sa.TEXT)
    album = sa.Column(sa.TEXT)

    # Вызывается при bool(object) и if obj
    def __bool__(self):
        if ((self.year == None) | (self.artist == None) | (self.genre == None) | (self.year == None)):
            return False
        else:
            return True

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()


def find(artist):
    """
    Находит все альбомы в базе данных по заданному артисту
    """
    session = connect_db()
    albums = session.query(Album).filter(Album.artist == artist).all()
    return albums

def find_album(album_data):
    """
    Находит альбом по совпадению всех параметров
    """
    session = connect_db()
    album_f = session.query(Album).filter(and_(Album.year == album_data["year"], Album.artist == album_data["artist"], Album.genre == album_data["genre"], Album.album == album_data["album"])).first()
    return album_f

def save(album_data):
    """
    сохраняем новый альбом
    """
    session = connect_db()
    new_album = Album(year=album_data["year"], artist=album_data["artist"], genre=album_data["genre"], album=album_data["album"])
    session.add(new_album)
    session.commit()
