import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from datetime import datetime

DB_PATH = 'sqlite:///sochi_athletes.sqlite3'
Base = declarative_base()

class Athlete(Base):
    __tablename__='athelete'
    id = sa.Column(sa.Integer, primary_key=True)
    age = sa.Column(sa.Integer)
    birthdate = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    height = sa.Column(sa.Float)
    name = sa.Column(sa.Text)
    weight = sa.Column(sa.Integer)
    gold_medals = sa.Column(sa.Integer)
    silver_medals = sa.Column(sa.Integer)
    bronze_medals = sa.Column(sa.Integer)
    total_medals = sa.Column(sa.Integer)
    sport = sa.Column(sa.Text)
    country = sa.Column(sa.Text)

class User(Base):
    """
    Описывает структуру таблицы user для хранения регистрационных данных пользователей
    """
    # задаем название таблицы
    __tablename__='user'
    id = sa.Column(sa.Integer, primary_key=True)
    first_name = sa.Column(sa.Text)
    last_name = sa.Column(sa.Text)
    gender = sa.Column(sa.Text)
    email = sa.Column(sa.Text)
    birthdate = sa.Column(sa.Text)
    height = sa.Column(sa.Float)

def request_data():
    user_id = input("Введите идентификатор (id) пользователя, который вас интересует: ")
    return int(user_id)

def connect_db():
    """
    Устанавливает соединение к базе данных, создает таблицы, если их еще нет и возвращает объект сессии 
    """
    # создаем соединение к базе данных
    engine = sa.create_engine(DB_PATH)
    # создаем описанные таблицы
    Base.metadata.create_all(engine)
    # создаем фабрику сессию
    session = sessionmaker(engine)
    # возвращаем сессию
    return session()

def get_date_birthdate(str_date):
    date_birthdate = datetime.strptime(str_date, '%Y-%m-%d')
    return (date_birthdate)

def neighbor_height(athletes, user_height, session):
    # ближайщий возраст будем искать по минимальноому квадрату разности
    dict_height = {athlete.id: (athlete.height-user_height)**2 for athlete in athletes}
    #определяем минимальный квадрат разности роста
    list_height = [height for height in dict_height.values()]
    min_difference = min(list_height)
    
    for id, dif in dict_height.items():
        if dif == min_difference:
            id_athlete = id
            break
    athlete = session.query(Athlete).filter(Athlete.id == id_athlete).first()
    return athlete

def neighbor_birthdate(athletes, user_birthdate, session):
    # разность между датами в днях
    dict_birthdate = {athlete.id: (get_date_birthdate(athlete.birthdate)- user_birthdate).days ** 2 for athlete in athletes}
    
    #определяем минимальный квадрат разности в днях
    list_birthdate = [day for day in dict_birthdate.values()]
    min_difference = min(list_birthdate)
    
    for id, dif in dict_birthdate.items():
        if dif == min_difference:
            id_athlete = id
            break
    athlete = session.query(Athlete).filter(Athlete.id == id_athlete).first()
    return athlete

def main():
    '''
    Основная программа
    '''
    session = connect_db()
    user_id = request_data()
    # ищем пользователя с заданным идентификатором
    user = session.query(User).filter(User.id == user_id).first()
    # список атлетов, у которых указан рост
    athletes = session.query(Athlete).filter(Athlete.height)

    # neighbor_height первый параметр = список пользователей в базе данных, второй параметр = рост заданного пользователя
    if user:
        print(f"Рост  {user.height}")
        athlete_h = neighbor_height(athletes, user.height, session)
        print(f"Ближайшем по росту к пользователю {user.first_name} {user.last_name} (рост = {user.height}) является атлет {athlete_h.name} с ростом {athlete_h.height}")
        
        # user_birthdate в формате даты
        user_birthdate = get_date_birthdate(user.birthdate)
        athlete_b = neighbor_birthdate(session.query(Athlete).all(), user_birthdate, session)
        print(f"Ближайшем по дате рождения к пользователю {user.first_name} {user.last_name} (дата рождения = {user.birthdate}) является атлет {athlete_b.name} с датой рождения {athlete_b.birthdate}")
    else:
        print(f"Пользователь с id = {user_id} не найден.")

if __name__ == "__main__":
    main()
