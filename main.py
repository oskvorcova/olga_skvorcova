# -*- coding: utf-8 -*-
import configparser
import logging
import sys
from logging import Formatter
from logging.handlers import RotatingFileHandler
import mysql.connector
from selenium_scrapper import selenium_scrapper


config = configparser.RawConfigParser()
config.read('conf.ini')

try:
    logger = logging.getLogger('logger')
    logger.setLevel(config.get('LOGGING', 'level'))
    handler = RotatingFileHandler(config.get('LOGGING', 'filename'), maxBytes=1000000, backupCount=10)
    formatter = Formatter(fmt='[%(asctime)s] %(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S', )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # получаем данные из файла настроек
    yandex_data = config.get('FOLDERS', 'yandex_data')  # каталог для исходящих данных
    google_data = config.get('FOLDERS', 'google_data')  # каталог для архивного хранения исходящих данных
    yandex_login = config.get('TOKENS', 'yandex_log')
    yandex_password = config.get('TOKENS', 'yandex_pass')
    selenium_executor = config.get('FOLDERS', 'selenium_executor')  # каталог с входными файлами
    create_db_sql = config.get('SQL', 'create_db')  # путь до большого скрипта необходимого при загрузке
    create_table_searches = config.get('SQL', 'create_table_searches')
    cnx = mysql.connector.connect(
        host=config.get('DB', 'host'),
        user=config.get('DB', 'user'),
        password=config.get('DB', 'sql_pass'),
        database="webscrapper"
    )  # конфиг для подключения к БД
except Exception as e:
    print('can not get params from ini, exit: {ex}'.format(ex=str(e)))



def main():
        try:
            cursor = cnx.cursor()

            # Execute a query
            query = "SELECT * FROM searches"
            cursor.execute(query)

            # Fetch the results
            for row in cursor.fetchall():
                print(row)

            # Close the cursor and connection
            cursor.close()
            cnx.close()
            logger.info('===THE END===')
        except Exception as e:
            logger.error('cannot reach DB: {ex}'.format(ex=str(e)))
            sys.exit(1)
        selenium_scrapper(selenium_executor, "абоба",yandex_login, yandex_password, yandex_data)
        sys.exit(1)



if __name__ == '__main__':
    main()
