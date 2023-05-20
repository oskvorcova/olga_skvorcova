# -*- coding: utf-8 -*-
import streamlit as st
from pytrends.request import TrendReq
import geopandas as gpd
import matplotlib.pyplot as plt
import time
from selenium_scrapper import selenium_scrapper
import configparser
import logging
from logging import Formatter
from logging.handlers import RotatingFileHandler


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
    yandex_login = config.get('TOKENS', 'yandex_log')
    yandex_password = config.get('TOKENS', 'yandex_pass')
    selenium_executor = config.get('FOLDERS', 'selenium_executor')  # каталог с входными файлами

except Exception as e:
    print('can not get params from ini, exit: {ex}'.format(ex=str(e)))

st.sidebar.title('Google Trends API')
keyword = st.sidebar.text_input('Enter a keyword')
timeframe = st.sidebar.selectbox('Select a timeframe', ['today 5-y', 'today 1-m', 'today 3-m', 'today 12-m'])
country = st.sidebar.selectbox('Select a country code', ['UA', 'CA', 'CN', 'US', 'BR', 'AU', 'GB', 'IN', 'AR', 'KZ', 'DE'])
time.sleep(5)

# вытаскиваем данные из АПИ гугла с помощью Pytrends
pytrends = TrendReq(hl='en-US', tz=360)
pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo='')
data = pytrends.interest_by_region()
interest_over_time_df = pytrends.interest_over_time()
st.dataframe(data.sort_values(by=keyword, ascending=False))
data = data.rename(index={"United States": "United States of America"})
# визуализируем с  Geopandas
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world = world.merge(data, how='left', left_on='name', right_index=True)
world = world.fillna(0)
world.plot(column=keyword, cmap='Blues', legend=True, figsize=(10, 6))
plt.title(f'Google Trends for "{keyword}" ({timeframe})')
plt.axis('off')
fig = plt.gcf()
st.pyplot(fig)

fig2, ax2 = plt.subplots()
ax2.plot(interest_over_time_df.index, interest_over_time_df[keyword])
ax2.set_title(f'Interest over time for "{keyword}" ({timeframe}) (WORLD)')
# выводим с помощью Streamlit
st.pyplot(fig2)

time.sleep(5)
pytrends.build_payload([keyword], cat=0, timeframe=timeframe, geo=country)
interest_over_time_df = pytrends.interest_over_time()

fig1, ax1 = plt.subplots()
ax1.plot(interest_over_time_df.index, interest_over_time_df[keyword])
ax1.set_title(f'Interest over time for "{keyword}" ({timeframe}) ({country})')
st.pyplot(fig1)


# Пришлось закомментировать тк яндекс стал банить при использовании селениума и невозможно ничего сделать оставаясь только на капче
# selenium_scrapper(selenium_executor, keyword, yandex_login, yandex_password, yandex_data)
# data = pandas.read_csv(f'yandex_data/{keyword}.csv')
# fig3, ax3 = plt.subplots()
# ax3.plot(data['Период'], data['Абсолютное'])
# st.pyplot(fig3)
