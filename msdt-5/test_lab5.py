import numpy as np
import math
import random
import scipy.stats as st
import unittest
from unittest.mock import patch
from parameterized import parameterized


@parameterized.expand([
    ([3, 4, 6, 8, 2, 3, 7, 5, 6], 4.888, 3.765, 1.940, 39.678),
    ([10, 20, 30, 40, 50], 30.0, 200.0, 14.142, 47.140)
])
def test_calculate_statistics_parametrized(self, data, expected_mean, expected_variance, expected_std, expected_cv):
    mean, variance, std_deviation, cv = calculate_statistics(data)
    self.assertAlmostEqual(mean, expected_mean, places=3)
    self.assertAlmostEqual(variance, expected_variance, places=3)
    self.assertAlmostEqual(std_deviation, expected_std, places=3)
    self.assertAlmostEqual(cv, expected_cv, places=3)


def test_confidence_interval(self):
    data = [3, 4, 6, 8, 2, 3, 7, 5, 6]
    interval = confidence_interval(data, 0.95)
    self.assertAlmostEqual(interval[0], 4.023, places=3)
    self.assertAlmostEqual(interval[1], 5.754, places=3)


def test_weighted_statistics(self):
    data = [12, 14, 22, 26, 30, 35, 40, 45, 50]
    weights = [0.05, 0.1, 0.15, 0.2, 0.2, 0.15, 0.1, 0.05]
    mean, variance, std_deviation, cv = weighted_statistics(data, weights)
    self.assertAlmostEqual(mean, 27.7, places=1)
    self.assertAlmostEqual(variance, 78.81, places=2)
    self.assertAlmostEqual(std_deviation, 8.87, places=2)
    self.assertAlmostEqual(cv, 32.03, places=2)


def test_analyze_profit(self):
    incomes = [3, 4, 6, 8, 2, 3, 7, 5, 6]
    expenses = [2, 3, 5, 7, 1, 2, 6, 4, 5]
    profit, mean, variance, std_deviation, cv = analyze_profit(incomes, expenses)
    self.assertAlmostEqual(mean, 1.0, places=1)
    self.assertAlmostEqual(variance, 0.888, places=3)
    self.assertAlmostEqual(std_deviation, 0.942, places=3)
    self.assertAlmostEqual(cv, 94.248, places=3)


@patch('random.gauss')
def test_simulate_data_with_mock(self, mock_gauss):
    mock_gauss.side_effect = [10, 20, 30, 40, 50]  # Подменяем вызов random.gauss
    data = simulate_data(0, 0, 5)
    self.assertEqual(data, [10, 20, 30, 40, 50])
    self.assertEqual(mock_gauss.call_count, 5)  # Проверяем, что функция вызвалась 5 раз


def test_detect_outliers(self):
    data = [10, 12, 14, 18, 19, 22, 24, 28, 30, 150]
    outliers = detect_outliers(data)
    self.assertIn(150, outliers)


def test_combined_case(self):  # Сложный тест с несколькими проверками
    incomes = [10, 20, 30, 40, 50]
    expenses = [5, 10, 15, 20, 25]
    profit, mean_profit, var_profit, std_profit, cv_profit = analyze_profit(incomes, expenses)
    interval = confidence_interval(profit, 0.90)
    self.assertAlmostEqual(mean_profit, 20, places=1)
    self.assertAlmostEqual(var_profit, 50, places=1)
    self.assertTrue(18 <= interval[0] <= 22)
    self.assertTrue(18 <= interval[1] <= 22)
