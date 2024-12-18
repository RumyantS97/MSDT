import numpy as np
import math
import random
import scipy.stats as st
import unittest

# Первый номер 🌈
print("\n====================Первый номер====================\n")
data1 = [3, 4, 6, 8, 2, 3, 7, 5, 6]

# Среднее арифметическое
mean1 = np.mean(data1)
print("Среднее арифметическое: ", mean1)

# Дисперсия
variance1 = np.var(data1)
print("Дисперсия: ", variance1)

# Среднее квадратическое отклонение
std_deviation1 = np.std(data1)
print("Среднее квадратическое отклонение: ", std_deviation1)

# Коэффициент вариации
cv1 = (std_deviation1 / mean1) * 100
print("Коэффициент вариации: ", cv1)

# Доверительный интервал
alpha1 = 0.95
std_err1 = st.sem(data1)
interval1 = st.norm.interval(alpha1, loc=mean1, scale=std_err1)
print("95% доверительный интервал: ", interval1)

# Второй номер 🌈
print("\n====================Второй номер====================\n")
data2 = [12, 14, 22, 26, 30, 35, 40, 45, 50]
weights = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]

# Среднее значение
mean2 = np.average(data2, weights=weights)
print("Среднее значение: ", mean2)

# Дисперсия
variance2 = np.sum([(x - mean2)**2 * weights[i] for i, x in enumerate(data2)])
print("Дисперсия: ", variance2)

# Среднее квадратическое отклонение
std_deviation2 = math.sqrt(variance2)
print("Среднее квадратическое отклонение: ", std_deviation2)

# Коэффициент вариации
cv2 = (std_deviation2 / mean2) * 100
print("Коэффициент вариации: ", cv2)

# Доверительный интервал
alpha2 = 0.95
std_err2 = st.sem(data2)
interval2 = st.norm.interval(alpha2, loc=mean2, scale=std_err2)
print("95% доверительный интервал: ", interval2)

# Третий номер
print("\n====================Третий номер====================\n")
data3 = [3, 6, 7, 12, 14, 17, 19, 24, 28, 30]
probabilities = [0.1, 0.15, 0.1, 0.1, 0.1, 0.15, 0.1, 0.1, 0.05, 0.05]

# Математическое ожидание
m_exp = np.sum([data3[i] * probabilities[i] for i in range(len(data3))])
print("Математическое ожидание: ", m_exp)

# Дисперсия
variance3 = np.sum([((data3[i] - m_exp) ** 2) * probabilities[i] for i in range(len(data3))])
print("Дисперсия: ", variance3)

# Среднее квадратическое отклонение
std_deviation3 = math.sqrt(variance3)
print("Среднее квадратическое отклонение: ", std_deviation3)

# Коэффициент вариации
cv3 = (std_deviation3 / m_exp) * 100
print("Коэффициент вариации: ", cv3)

# Доверительный интервал
mean3 = np.mean(data3)
std_err3 = st.sem(data3)
alpha3 = 0.95
interval3 = st.norm.interval(alpha3, loc=mean3, scale=std_err3)
print("95% доверительный интервал для математического ожидания: ", interval3)

# Четвёртый номер 🌈
print("\n====================Четвёртый номер====================\n")
arr_income = [3, 4, 6, 8, 2, 3, 7, 5, 6]
arr_expense = [2, 3, 5, 7, 1, 2, 6, 4, 5]

# Средний доход и расход
avg_income = np.mean(arr_income)
avg_expense = np.mean(arr_expense)
print("Средний доход: ", avg_income)
print("Средний расход: ", avg_expense)

# Средняя прибыль
profit = [arr_income[i] - arr_expense[i] for i in range(len(arr_income))]
avg_profit = np.mean(profit)
print("Средняя прибыль: ", avg_profit)

# Дисперсия прибыли
disp_profit = np.var(profit)
print("Дисперсия прибыли: ", disp_profit)

# Среднее квадратическое отклонение прибыли
std_profit = np.std(profit)
print("Среднее квадратическое отклонение прибыли: ", std_profit)

# Коэффициент вариации прибыли
cv_profit = (std_profit / avg_profit) * 100
print("Коэффициент вариации прибыли: ", cv_profit)

# Доверительный интервал прибыли
mean_profit = np.mean(profit)
std_err_profit = st.sem(profit)
alpha4 = 0.90
interval4 = st.norm.interval(alpha4, loc=mean_profit, scale=std_err_profit)
print("90% доверительный интервал для прибыли: ", interval4)

# Пятый номер 🌈
print("\n====================Пятый номер====================\n")

# Имитация случайных данных
simulated_data = [random.gauss(50, 15) for _ in range(100)]
print("Симулированные данные: ", simulated_data[:10], "... (всего 100)")

# Оценка характеристик данных
mean_sim = np.mean(simulated_data)
std_dev_sim = np.std(simulated_data)
print("Среднее значение симулированных данных: ", mean_sim)
print("Среднее квадратическое отклонение симулированных данных: ", std_dev_sim)

# Доверительный интервал для среднего
std_err_sim = st.sem(simulated_data)
alpha5 = 0.95
interval5 = st.norm.interval(alpha5, loc=mean_sim, scale=std_err_sim)
print("95% доверительный интервал для симулированных данных: ", interval5)

# Анализ выбросов
q1, q3 = np.percentile(simulated_data, [25, 75])
iqr = q3 - q1
lower_bound = q1 - 1.5 * iqr
upper_bound = q3 + 1.5 * iqr
outliers = [x for x in simulated_data if x < lower_bound or x > upper_bound]
print("Выбросы: ", outliers)

# Четвёртый номер 🌈
print("\n====================Четвёртый номер====================\n")
array_time = [round(random.uniform(4.0, 4.5), 1), round(random.uniform(4.5, 5.0), 1), round(random.uniform(5.0, 5.5), 1), round(random.uniform(5.5, 6.0), 1), round(random.uniform(6.0, 6.5), 1), round(random.uniform(6.5, 7.0), 1), round(random.uniform(7.0, 7.5), 1), round(random.uniform(7.5, 8.0), 1), round(random.uniform(8.0, 9.5), 1)]
array_worker = [4, 14, 55, 92, 160, 96, 66, 11, 2]
array = []
for nn in range(len(array_worker) - 1):
    for MMM in range(array_worker[nn]):
        array.append(array_time[nn])

# Среднее время, которое рабочий тратит на изготовление детали 🐳
sred_znach = 0
for nnn in range (len(array)):
    sred_znach += array[nnn]
sred_znach = sred_znach / len(array)

# Доверительный интервал для cреднего времени, которое рабочий тратит на изготовление детали 🎋
mean = np.mean(sred_znach)
std_err = st.sem(array)
loc=mean
alpha=0.999
scale=std_err
interval4 = st.norm.interval(alpha, loc, scale)
print("99.9% доверительный интервал для cреднего времени, которое рабочий тратит на изготовление детали:", interval4)


# Пятый номер 🌈
print("\n====================Пятый номер====================\n")

count_items = np.array([8, 42, 51, 37, 12])
average_meaning = np.array([12, 14, 16, 18, 20])


# Общее количество изделий 🍉
n = np.sum(count_items)
# Дисперсия n/n-1
# Средний процент влажности 🥑
average_procent = np.sum(count_items * average_meaning) / n

# Стандартное отклонение 🍅
standart_otklonenie = np.sqrt(np.sum(count_items * (average_meaning - average_procent) ** 2) / n)

print("Средний процент влажности:", average_procent)
print("Стандартное отклонение:", standart_otklonenie)

# а) Вероятность того, что средний процент влажности заключен в границах от 12.5 до 17.5 🍎
down_border = 12.5
top_border = 17.5
probability = (top_border - average_procent) / standart_otklonenie - (down_border - average_procent) / standart_otklonenie
print("Вероятность:", probability)

# б) Границы, в которых с вероятностью 0.95 будет заключен средний процент влажности изделий во всей партии 🍍
border_95 = np.percentile(count_items, [2.5, 97.5], interpolation='nearest')
print("Границы:", average_procent + border_95 * standart_otklonenie)



# Вторая практика 🌈
print("\n====================Вторая практика====================\n")
# Первый номер 🍅
print("\nПервый номер:")
empire_arr = [14, 18, 32, 70, 36, 20, 10]
teory_arr = [10, 24, 34, 80, 22, 18, 12]
IhateCarrots = [0] * 7
empire_sum = 0
teory_sum = 0
nabludaemoe = 0
s = 7 # Запомним, в будущем нам это пригодится
for i in range(len(empire_arr)):
    empire_sum += empire_arr[i]
for i in range(len(empire_arr)):
    teory_sum += empire_arr[i]
for i in range(len(empire_arr)):
    IhateCarrots[i] = ((empire_arr[i] - teory_arr[i])**2)/teory_arr[i]
    nabludaemoe += IhateCarrots[i]
if (teory_sum != empire_sum):
    print("Сумма частот различается и дальше нет смысла проводить исследование")
else:
    print("Сумма частот совпадает")
    Hi = 9.48773
    if (Hi < nabludaemoe):
        print("Хи критическое меньше наблюдаемого, следовательно, H0 отвергается и принимается H1")
    elif (Hi > nabludaemoe):
        print("Хи критическое больше наблюдаемого, следовательно, H1 отвергается и принимается H0")

# Второй номер 🍅
print("\n\nВторой номер:")
# Данные
X = np.array([7.8, 8.2, 9.1, 8.9, 8.6])
Y = np.array([6.6, 7.1, 6.3, 7, 6.2, 5.8])

# t-критерий Стьюдента для независимых выборок и соответсвующего p-значения
t_statistic, p_value = st.ttest_ind(X, Y)

# Определение уровня значимости
alpha = 0.05

# Проверка статистической значимости
if p_value < alpha:
    print("Отвергаем нулевую гипотезу. Станки не обладают одинаковой точностью.")
else:
    print("Принимаем нулевую гипотезу. Станки обладают одинаковой точностью.")

print("t-статистика:", t_statistic)
print("p-значение:", p_value)


# Третий номер 🍅
print("\n\nТретий номер:")
# Данные
x_mean = 4.85
y_mean = 5.07
Sx = 0.94
Sy = 1.02
n_x = 15
n_y = 12

# Расчет t-статистики и p-значения
t_statistic, p_value = st.ttest_ind_from_stats(x_mean, Sx, n_x, y_mean, Sy, n_y)

# Определение уровня значимости
alpha = 0.01

# Проверка статистической значимости
if p_value < alpha:
    print("Отвергаем нулевую гипотезу. Существует существенное различие средней себестоимости единицы продукции на предприятиях.")
else:
    print("Принимаем нулевую гипотезу. Различие средней себестоимости единицы продукции на предприятиях несущественно.")

print("t-статистика:", t_statistic)
print("p-значение:", p_value)




# Четвёртый номер 🍅
print("\n\nЧетвёртый номер:")
# Данные для первой группы
x_values = [34, 35, 37, 39]
n_x = [2, 3, 4, 1]

# Данные для второй группы
y_values = [32, 34, 36]
n_y = [2, 2, 8]

# Расчет среднего и стандартного отклонения для каждой группы
mean_x = sum([x * n for x, n in zip(x_values, n_x)]) / sum(n_x)
mean_y = sum([y * n for y, n in zip(y_values, n_y)]) / sum(n_y)

# Стандартное отклонение и среднее для каждой выборки
S_x = (sum([n * ((x - mean_x) ** 2) for x, n in zip(x_values, n_x)]) / (sum(n_x) - 1)) ** 0.5
S_y = (sum([n * ((y - mean_y) ** 2) for y, n in zip(y_values, n_y)]) / (sum(n_y) - 1)) ** 0.5

# Расчет t-статистики и p-значения
t_statistic, p_value = st.ttest_ind_from_stats(mean_x, S_x, sum(n_x), mean_y, S_y, sum(n_y))

# Определение уровня значимости
alpha = 0.05

# Проверка статистической значимости
if p_value < alpha:
    print("Отвергаем нулевую гипотезу. Существует существенное различие средних значений дебиторской задолженности в группах.")
else:
    print("Принимаем нулевую гипотезу. Различие средних значений дебиторской задолженности в группах несущественно.")

print("t-статистика:", t_statistic)
print("p-значение:", p_value)



# Пятый номер 🍅
print("\n\nПятый номер:")
# Данные для первой группы
x_values = [139, 137, 134, 134, 137, 137, 135, 137, 135, 135]
mean_x = sum(x_values) / len(x_values)

# Данные для второй группы
y_values = [136, 136, 132, 134, 136, 136, 134, 132, 136, 136, 136, 136]
mean_y = sum(y_values) / len(y_values)

# Расчет t-статистики и p-значения
t_statistic, p_value = st.ttest_ind(x_values, y_values)

# Определение уровня значимости
alpha = 0.05

# Проверка статистической значимости
if p_value < alpha:
    print("Отвергаем нулевую гипотезу. Существует существенное различие средних значений средней выручки в группах.")
else:
    print("Принимаем нулевую гипотезу. Различие средних значений средней выручки в группах несущественно.")

print("t-статистика:", t_statistic)
print("p-значение:", p_value)

# Основные функции анализа

def calculate_statistics(data):
    mean = np.mean(data)
    variance = np.var(data)
    std_deviation = np.std(data)
    cv = (std_deviation / mean) * 100
    std_err = st.sem(data)
    alpha = 0.95
    interval = st.norm.interval(alpha, loc=mean, scale=std_err)
    return mean, variance, std_deviation, cv, interval

def weighted_statistics(data, weights):
    mean = np.average(data, weights=weights)
    variance = np.sum([(x - mean)**2 * weights[i] for i, x in enumerate(data)])
    std_deviation = math.sqrt(variance)
    cv = (std_deviation / mean) * 100
    return mean, variance, std_deviation, cv

def profit_analysis(income, expense):
    profit = [income[i] - expense[i] for i in range(len(income))]
    avg_profit = np.mean(profit)
    disp_profit = np.var(profit)
    std_profit = np.std(profit)
    cv_profit = (std_profit / avg_profit) * 100
    std_err = st.sem(profit)
    alpha = 0.90
    interval = st.norm.interval(alpha, loc=avg_profit, scale=std_err)
    return avg_profit, disp_profit, std_profit, cv_profit, interval

def simulate_data(size, mean, std_dev):
    simulated_data = [random.gauss(mean, std_dev) for _ in range(size)]
    q1, q3 = np.percentile(simulated_data, [25, 75])
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = [x for x in simulated_data if x < lower_bound or x > upper_bound]
    return simulated_data, lower_bound, upper_bound, outliers

# Тесты
class TestStatistics(unittest.TestCase):

    def test_calculate_statistics(self):
        data = [3, 4, 6, 8, 2, 3, 7, 5, 6]
        mean, variance, std_dev, cv, interval = calculate_statistics(data)
        self.assertAlmostEqual(mean, 4.8888, places=4)
        self.assertAlmostEqual(variance, 3.7654, places=4)
        self.assertAlmostEqual(std_dev, 1.9405, places=4)
        self.assertAlmostEqual(cv, 39.6837, places=4)

    def test_weighted_statistics(self):
        data = [12, 14, 22, 26, 30, 35, 40, 45, 50]
        weights = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
        mean, variance, std_dev, cv = weighted_statistics(data, weights)
        self.assertAlmostEqual(mean, 27.7, places=1)
        self.assertAlmostEqual(variance, 101.36, places=2)
        self.assertAlmostEqual(std_dev, 10.0679, places=4)
        self.assertAlmostEqual(cv, 36.3483, places=4)

    def test_profit_analysis(self):
        income = [3, 4, 6, 8, 2, 3, 7, 5, 6]
        expense = [2, 3, 5, 7, 1, 2, 6, 4, 5]
        avg_profit, disp_profit, std_profit, cv_profit, interval = profit_analysis(income, expense)
        self.assertAlmostEqual(avg_profit, 1.1111, places=4)
        self.assertAlmostEqual(disp_profit, 0.7654, places=4)
        self.assertAlmostEqual(std_profit, 0.8744, places=4)
        self.assertAlmostEqual(cv_profit, 78.662, places=3)

    def test_simulate_data(self):
        simulated_data, lower_bound, upper_bound, outliers = simulate_data(100, 50, 15)
        self.assertEqual(len(simulated_data), 100)
        self.assertIsInstance(outliers, list)

if __name__ == "__main__":
    unittest.main()
