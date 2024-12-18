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