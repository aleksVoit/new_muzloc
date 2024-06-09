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


# Удаляем таблицы, если сузществуют
def drop_accounts():
    cur.execute(
        'drop table if exists accounts cascade'
    )


def drop_profiles():
    cur.execute(
        'drop table if exists profiles'
    )


def drop_registrations():
    cur.execute(
        'drop table if exists registrations'
    )


# Генерируем случайные данные для предметов
def create_accounts_table():
    cur.execute(
        'CREATE table if not exists accounts ( \
            account_id	serial constraint account_id_key PRIMARY key, \
            name        varchar(30) NOT NULL, \
            email       varchar(100) NOT NULL, \
            phone   	varchar(30) NOT NULL \
        )'
    )


def create_profiles_table():
    cur.execute(
        'CREATE table if not exists profiles ( \
            profile_id	serial PRIMARY key, \
            birthday    date, \
            bio         varchar(500), \
            location    varchar(500), \
            photo	    varchar(100), \
            music       varchar(100), \
            video    	varchar(100), \
            post		varchar(500), \
            account_id  Integer REFERENCES accounts(account_id) on delete cascade \
        )'
    )


def create_registrations_table():
    cur.execute(
        'CREATE table if not exists registrations ( \
            id	        serial PRIMARY key, \
            password    varchar(100), \
            account_id  Integer REFERENCES accounts(account_id) on delete cascade \
        )'
    )


try:
    # Фиксируем изменения
    drop_accounts()
    drop_profiles()
    drop_registrations()
    create_accounts_table()
    create_profiles_table()
    create_registrations_table()
    conn.commit()
except DatabaseError as e:
    logging.error(e)
    conn.rollback()
finally:
    # Закрываем соединение с базой данных
    cur.close()
    conn.close()
