Этот проект представляет собой стримлит приложения для парсинга поисковой выдачи
Google а так же сложной визуализации по странам, месяцам и годам.
app.py
Так же проект представляет собой ipynb с исследованием динамики запросов
поисковой выдачи наиболее популярных университетов мира, тоже с визуализацией соответсвенно
(university_trends.ipynb)
При работе использовался Селениум для парсинга поисковой выдачи яндекса
(selenium_parser.py)
в качестве движка использовался хромдрайвер
MySQL хранения и обработки данных
Streamlit - для быстрого развертывания дата приложения и удобного интерфейса
Geopandas - для визуализации данных по миру

Google Trends API (Py Trends) - для парсинга данных из поисковой системы гугл

Так же в проекте реализована система логирования и считывания конфигов из файла
что в теории более безопасно

ИНСТРУКЦИЯ ПО ЗАПУСКУ

1. pip install -r req.txt
2. необходимо иметь развернутую базу данных MySQL локально или удаленно не важно - главное заполнить конфиг для подключения
3. https://chromedriver.chromium.org/
4. https://www.google.ru/chrome/thank-you.html?statcb=1&installdataindex=empty&defaultbrowser=0
5. streamlit run app.py