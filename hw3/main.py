"""Задача 1: Создайте экземпляр движка для подключения к SQLite базе данных в памяти.

Задача 2: Создайте сессию для взаимодействия с базой данных, используя созданный движок.

Задача 3: Определите модель продукта Product со следующими типами колонок:

id: числовой идентификатор

name: строка (макс. 100 символов)

price: числовое значение с фиксированной точностью

in_stock: логическое значение

Задача 4: Определите связанную модель категории Category со следующими типами колонок:

id: числовой идентификатор

name: строка (макс. 100 символов)

description: строка (макс. 255 символов)

Задача 5: Установите связь между таблицами Product и Category с помощью колонки category_id."""

from sqlalchemy import create_engine

#Создание SQLite db в памяти, которая исчезнет после завершения программы
engine = create_engine("sqlite:///:memory:", echo=True) #+ вывод sql команд в консоль

from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base() # Базовый класс для моделей
Session = sessionmaker(bind=engine)
session = Session() #Создание сессии для общения с бд

from sqlalchemy import Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import relationship

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")#1:M

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, default=True)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products") #M:1

Base.metadata.create_all(engine) # Создание таблиц

new_category = Category(name="Electronics", description="Gadgets and tech")
session.add(new_category)
session.commit()