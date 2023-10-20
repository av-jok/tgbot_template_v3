from typing import Optional

from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

from infrastructure.database.models.base import TimestampMixin, TableNameMixin, Base
from typing import Optional

from sqlalchemy import text, BIGINT, Boolean, true


DATABASE = {
    'drivername': 'postgres',
    'host': 'localhost',
    'port': '5432',
    'username': 'joker',
    'password': 'Mrj0keer155',
    'database': 'bot'
}


class Post(Base, TimestampMixin, TableNameMixin):
    __tablename__ = 'posts'

    id: Mapped[int] = mapped_column(BIGINT, primary_key=True, autoincrement=False)
    name: Mapped[Optional[str]] = mapped_column(String(128))
    url: Mapped[str] = mapped_column(String(128))


def main():
    # Создаем объект Engine, который будет использоваться объектами ниже для связи с БД
    # engine = create_engine(URL(**DATABASE))
    engine = create_engine('postgresql+asyncpg://joker:Mrj0keer155@localhost:5439/bot')
    engine.connect()

    # Метод create_all создает таблицы в БД, определенные с помощью  DeclarativeBase
    # Post.metadata.create_all(engine)

    # Создаем фабрику для создания экземпляров Session. Для создания фабрики в аргументе
    # bind передаем объект engine
    sess = sessionmaker(bind=engine)

    # Создаем объект сессии из вышесозданной фабрики Session
    session = sess()

    # Создаем новую запись.
    new_post = Post(name='Two record', url="http://testsite.ru/first_record")

    # Добавляем запись
    session.add(new_post)

    # Благодаря этой строчке мы добавляем данные в таблицу
    session.commit()

    # А теперь попробуем вывести все посты, которые есть в нашей таблице
    for post in session.query(Post):
        print(post)


if __name__ == "__main__":
    main()
