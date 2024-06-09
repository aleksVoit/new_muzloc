import logging

from faker import Faker
import random
import psycopg2
from psycopg2 import sql, DatabaseError

# Соединяемся с базой данных
conn = psycopg2.connect(host='localhost', database="muzloc", user="postgres", password="0000")

# Создаем курсор для выполнения SQL-запросов
cur = conn.cursor()


def update_photo():
    user_id = 1  # Это пример, используйте реальный ID пользователя
    photo_path = '/fake_photos/logo.png'
    cur.execute("UPDATE profiles SET photo = %s WHERE account_id = %s", (photo_path, user_id))



try:
    # Фиксируем изменения
    update_photo()
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закрываем соединение с базой данных
    cur.close()
    conn.close()
