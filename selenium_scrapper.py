from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import pandas as pd
import time


def selenium_scrapper(path_to_driver, query, ya_log, ya_pass, yandex_folder_path):
    # инициализируем драйвер
    driver = webdriver.Chrome(executable_path=path_to_driver)

    driver.get('https://wordstat.yandex.ru/#!/history?period=weekly&words={}'\
               .format(query.replace(" ", "%20")))
    # вводим реальные креды тк при запуске селениума яндекс вынуждает логинится
    log = ya_log
    password = ya_pass
    elem_log  =  driver.find_element(By.ID,  'b-domik_popup-username' )
    elem_log.send_keys(log + Keys.RETURN)
    time.sleep(2)
    # Спим чтобы обмануть яндекс, чтобы он не понял что это не живой человек запросил страницу
    elem_pass  =  driver.find_element("name","passwd")
    elem_pass.send_keys(password + Keys.RETURN)
    time.sleep(2)
    # Опять спим
    elem_log  =  driver.find_element(By.ID,  'login' )
    elem_log.send_keys(log + Keys.RETURN)
    time.sleep(10)

    data =  driver.find_element(By.CLASS_NAME,  'b-history__table-box' )
    element_text = data.text
    # Сохраняем в текстовый файл тк потом проще работать через пандас выбирая сепаратор пробел
    text_file = open("{}/{}.csv".format(yandex_folder_path, query),
                     "w", encoding='utf-8')
    text_file.write(element_text)
    text_file.close()

    df = pd.read_csv("{}/{}.csv".format(yandex_folder_path, query), sep =' ')
    for x in range(len(df)):
        df.iloc[x,0] = df.index[x][0] + df.index[x][1] + df['Период'][x]
    df = df.reset_index(drop=True)
    # Удаляем лишнюю строчку которая сохранилась при парсинге
    df = df.drop([26])
    df.to_csv("{}/{}.csv".format(yandex_folder_path, query), index = False)