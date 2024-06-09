import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import sql, DatabaseError

fake = Faker()

# Соединяемся с базой данных
conn = psycopg2.connect(host='localhost', database="muzloc", user="postgres", password="0000")

# Создаем курсор для выполнения SQL-запросов
cur = conn.cursor()

# Генерируем случайные данные для групп
for i in range(1, 4):
    cur.execute(
        "INSERT INTO accounts (name,  email, phone) VALUES (%s, %s, %s)",
        (fake.name(), fake.email(), fake.phone_number())
    )

# Генерируем случайные данные для предметов
for account_id in range(1, 4):
    cur.execute(
        "INSERT INTO profiles (bio, location, birthday, post, account_id) VALUES (%s, %s, %s, %s, %s)",
        (fake.word(), fake.address(), fake.date(), fake.word(), account_id)
    )

for account_id in range(1, 4):
    cur.execute(
        "INSERT INTO registrations (password, account_id) VALUES (%s, %s)",
        (fake.word(), account_id)
    )

try:
    # Фиксируем изменения
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закрываем соединение с базой данных
    cur.close()
    conn.close()
