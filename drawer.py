import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('yandex_data/harvard.csv')

#  график
plt.plot(data['Период'], data['Абсолютное'])

# добавить заголовок и метки осей
plt.title('График временного ряда по запросу Гарвард')
plt.xlabel('Период')
plt.ylabel('Абсолютное')

# сохранить график на компьютере
plt.savefig('my_plot.png')