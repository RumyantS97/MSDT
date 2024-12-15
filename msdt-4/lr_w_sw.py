from __future__ import division
from __future__ import print_function
import nltk
import os
import sys
from nltk.tokenize import RegexpTokenizer
from nltk.stem import LancasterStemmer
import glob
import math
import numpy
import random
import logging


# Настройка конфигурации логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 0=ham
# 1=spam


def lr():
    # Логируем начало обучения
    logging.info("Начало процесса обучения логистической регрессии.")
    ham_files = len(glob.glob("train/ham/*.txt"))
    spam_files = len(glob.glob("train/spam/*.txt"))
    total_no_of_files = ham_files + spam_files

    # Логируем количество найденных файлов ham и spam
    logging.info(f"Всего файлов: {total_no_of_files} (Нормальные: {ham_files}, Спам: {spam_files})")
    eta = 0.01
    lamb = [0.1, 0.2, 0.3, 0.4, 0.5]
    all_words = {}
    all_words = stem("train/*/*", all_words)
    no_of_unique_training_words = len(all_words)

    # Логируем количество уникальных слов в обучающей выборке
    logging.info(f"Количество уникальных слов в обучающей выборке: {no_of_unique_training_words}")

    data = numpy.zeros((total_no_of_files, no_of_unique_training_words+2))
    data = populate_data("train/*/*", all_words, data, no_of_unique_training_words)

    for lb in lamb:
        pr = [random.random() for i in range(total_no_of_files)]
        w = [random.random() for i in range(no_of_unique_training_words+1)]

        for conv in range(80):
            for i in range(total_no_of_files):
                pr[i] = compute_pr(data, w, i, no_of_unique_training_words)
            dw = [0 for i in range(no_of_unique_training_words+1)]
            for j in range(no_of_unique_training_words + 1):
                for i in range(total_no_of_files):
                    dw[j] = dw[j] + (data[i][j] * (data[i][no_of_unique_training_words + 1] - pr[i]))
            for i in range(no_of_unique_training_words + 1):
                w[i] = w[i] + ((eta)*(dw[i] - ((lb)*w[i])))
        accuracy = test(w, all_words)

        # Логируем точность для каждого значения lambda
        logging.info(f"Lambda: {lb}, Точность: {accuracy:.2f}%")


def compute_pr(data, w, i, no_of_unique_training_words):
    sum = 0
    for j in range(no_of_unique_training_words+1):
        sum += (data[i][j]*w[j])
    try:
        pr = (math.exp(sum)/(1+math.exp(sum)))
    except OverflowError:
        # Логируем ошибку переполнения
        logging.error("Ошибка переполнения при вычислении вероятности.")
        pr = 0.99

        # Логируем вычисленную вероятность
        logging.debug(f"Вычисленная вероятность для индекса {i}: {pr:.4f}")
    return pr


def test(w, all_words):
    # Логируем начало тестирования
    logging.info("Начало этапа тестирования.")
    filepath = glob.glob("test-2/ham/*.txt")
    test_file_count = len(filepath)

    # Логируем количество тестовых файлов в директории ham
    logging.info(f"Тестируем на {test_file_count} файлах ham.")

    wrong_decision = 0
    for file in filepath:
        file = file.rstrip(".txt")
        pr_o = get_prediction(file, w, all_words)
        if (pr_o >= 0):
            wrong_decision += 1

    filepath = glob.glob("test-2/spam/*")
    test_file_count += len(filepath)
    # Логируем количество спам-файлов для тестирования
    logging.info(f"Тестирование на {len(filepath_spam)} спам-файлах.")
    for file in filepath:
        file = file.rstrip(".txt")
        pr_o = get_prediction(file, w, all_words)
        if (pr_o < 0):
            wrong_decision += 1
    accuracy = (test_file_count - wrong_decision) / test_file_count
    # Логируем итоговую точность тестирования
    logging.info(f"Тестирование завершено с точностью: {accuracy}%")
    return accuracy*100


def get_prediction(file, w, all_words):
    words_count = {}
    words_count = stem(file, words_count)
    pr_o = w[0]
    for words in words_count:
        if words in all_words:
            pr_o += (w[all_words.keys().index(words)+1] * words_count[words])
    # Логируем предсказанную вероятность для файла
    logging.debug(f"Предсказание для файла '{file}': {pr_o}")
    return pr_o


def stem(path, bag_of_words):
    filepath = glob.glob(path + ".txt")
    tokenizer = RegexpTokenizer("[a-zA-Z]+")
    stemmer = LancasterStemmer()
    for file in filepath:
        if not os.path.isfile(file):
            # Логируем ошибку отсутствия файла
            logging.error(f"Путь к файлу {file} не существует. Завершение...")
            sys.exit()
        with open(file, 'r') as fp:
            for line in fp:
                tokens = tokenizer.tokenize(line)
                stemmed = [stemmer.stem(t) for t in tokens]
                record_word_cnt(stemmed, bag_of_words)
    # Логируем количество обработанных файлов
    logging.info(f"Обработано {processed_files_count} файлов во время стемминга.")
    return bag_of_words


def record_word_cnt(words, bag_of_words):
    for word in words:
        if word != '':
            if word.lower() in bag_of_words:
                bag_of_words[word.lower()] += 1
            else:
                bag_of_words[word.lower()] = 1


def populate_data(path, bag_of_words, data, no_of_unique_training_words):
    filepath = glob.glob(path + ".txt")
    tokenizer = RegexpTokenizer("[a-zA-Z]+")
    stemmer = LancasterStemmer()
    i = 0
    for file in filepath:
        word_store = {}
        if not os.path.isfile(file):
            # Логируем ошибку отсутствия файла
            logging.error(f"Путь к файлу {file} не существует. Завершение...")
            sys.exit()

        with open(file, 'r') as fp:
            for line in fp:
                tokens = tokenizer.tokenize(line)
                stemmed = [stemmer.stem(t) for t in tokens]
                record_word_cnt(stemmed, word_store)
        if "train/ham/" in file:
            data[i][no_of_unique_training_words+1] = 0
        elif "train/spam/" in file:
            data[i][no_of_unique_training_words + 1] = 1
        for words in word_store:
            data[i][bag_of_words.keys().index(words)+1] = word_store[words]
        data[i][0] = 1
        i += 1

    # Логируем количество заполненных данных
    logging.info(f"Данные заполнены из {processed_files_count} файлов.")
    return data
