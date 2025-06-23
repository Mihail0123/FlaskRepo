"""Задача 1: Наполнение данными
Добавьте в базу данных следующие категории и продукты
Добавление категорий: Добавьте в таблицу categories следующие категории:

Название: "Электроника", Описание: "Гаджеты и устройства."

Название: "Книги", Описание: "Печатные книги и электронные книги."

Название: "Одежда", Описание: "Одежда для мужчин и женщин."

Добавление продуктов: Добавьте в таблицу products следующие продукты, убедившись, что каждый продукт связан с соответствующей категорией:

Название: "Смартфон", Цена: 299.99, Наличие на складе: True, Категория: Электроника

Название: "Ноутбук", Цена: 499.99, Наличие на складе: True, Категория: Электроника

Название: "Научно-фантастический роман", Цена: 15.99, Наличие на складе: True, Категория: Книги

Название: "Джинсы", Цена: 40.50, Наличие на складе: True, Категория: Одежда

Название: "Футболка", Цена: 20.00, Наличие на складе: True, Категория: Одежда

Задача 2: Чтение данных
Извлеките все записи из таблицы categories. Для каждой категории извлеките и выведите все связанные с ней продукты, включая их названия и цены.


Задача 3: Обновление данных
Найдите в таблице products первый продукт с названием "Смартфон". Замените цену этого продукта на 349.99.


Задача 4: Агрегация и группировка
Используя агрегирующие функции и группировку, подсчитайте общее количество продуктов в каждой категории.


Задача 5: Группировка с фильтрацией
Отфильтруйте и выведите только те категории, в которых более одного продукта."""

from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=False)
Session = sessionmaker(bind=engine)
session = Session()

class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255))

    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    in_stock = Column(Boolean, nullable=False, default=False)

    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("Category", back_populates="products")

Base.metadata.create_all(engine)


#napolnenie categories

electronics = Category(name="Electronics", description="Gadgets and tech")
books = Category(name="Books", description="Books and ebooks")
clothing = Category(name="Clothing", description="Male and female clothing")
session.add_all([electronics, books, clothing])
session.commit()

#napolnenie products

products = [
    Product(name="Smartphone", price=299.99, in_stock=True, category=electronics),
    Product(name="Laptop", price=499.99, in_stock=True, category=electronics),
    Product(name="Sci-Fi novel", price=15.99, in_stock=True, category=books),
    Product(name="Jeans", price=40.50, in_stock=True, category=clothing),
    Product(name="T-Shirt", price=20.00, in_stock=True, category=clothing),
]
session.add_all(products)
session.commit()

print("\n 2.Categories and products")
categories = session.query(Category).all()
for cat in categories:
    print(f"Category: {cat.name}")
    for prod in cat.products:
        print(f"     {prod.name}: {prod.price}")


print("3. Smartphone price update")
phone = session.query(Product).filter_by(name="Smartphone").first()
if phone:
    phone.price = 349.99
    session.commit()
    print(f"New price: {phone.price}")


print("4. Product amount by category")
counts = session.query(Category.name, func.count(Product.id)).join(Product).group_by(Category.id).all()
for name, count in counts:
    print(f"{name}: {count} products")

print("5. Categories with more than one product")
filtered = session.query(Category.name, func.count(Product.id)).join(Product).group_by(Category.id).having(func.count(Product.id) > 1).all()
for name, count in filtered:
    print(f"{name}: {count} products")