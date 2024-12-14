# Pls add comment about program
"""
This program...
"""

# 1. It's good idea to add comment why we use this packages
# 2. And it's not good idea to import all package.
#    Import only methods that you have used in your code.
import statistics
from baseFunctions import get_data_set, define_class
import numpy as np
import pandas
# See, this is good information about imports
# -> https://peps.python.org/pep-0008/#imports
# Don't forget add comments why we need this packages.
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_score
from sklearn.metrics import recall_score
from sklearn.ensemble import RandomForestClassifier as classifier
from sklearn.model_selection import train_test_split


np.seterr(divide="ignore", invalid="ignore")

data_set, files, srs = get_data_set("dataset")

chi_points = []
unman_points = []
student_points = []
labels = []
middles = []
all_vec = []

train_len = round(len(data_set))

train_split = data_set[0:]

for i in range(len(train_split)):
    for j in range(i + 1, len(train_split)):
        # It's not good idea to naming fields like this.
        # The name of field should describe what field does
        # and why it creates.
        [a, b, c] = statistics.use_stat_for_spectr(
            train_split[i], train_split[j]
        )
        label = define_class(files[i], files[j])
        labels.append(label)
        middle = (a + b + c) / 3
        middles.append(middle)
        chi_points.append(a)
        unman_points.append(b)
        student_points.append(c)
        vec = [a, b, c]
        all_vec.append(vec)

df = pandas.DataFrame(
    {
        "chi": chi_points,
        "unamm": unman_points,
        "stud": student_points,
        "pair": labels,
        "middle": middles,
    }
)
df.to_csv("stats.csv")

inside_points_chi = []
inside_points_student = []
inside_points_umann = []

outside_points_chi = []
outside_points_student = []
outside_points_umann = []
predicted = []

chi_model = classifier()
unman_model = classifier()
stud_model = classifier()
mid_model = classifier()
all_model = classifier()

chi_points = np.array(chi_points)
chi_points = chi_points.reshape(-1, 1)
unman_points = np.array(unman_points)
unman_points = chi_points.reshape(-1, 1)
student_points = np.array(student_points)
student_points = chi_points.reshape(-1, 1)
middles = np.array(middles)
middles = chi_points.reshape(-1, 1)
all_vec = np.array(all_vec)
all_vec = chi_points.reshape(-1, 1)


chi_x_train, chi_x_test, chi_y_train, chi_y_test = train_test_split(
    chi_points, labels, test_size=0.30
)
unman_x_train, unman_x_test, unman_y_train, unman_y_test = train_test_split(
    unman_points, labels, test_size=0.30
)
stud_x_train, stud_x_test, stud_y_train, stud_y_test = train_test_split(
    student_points, labels, test_size=0.30
)
mid_x_train, mid_x_test, mid_y_train, mid_y_test = train_test_split(
    middles, labels, test_size=0.30
)
all_x_train, all_x_test, all_y_train, all_y_test = train_test_split(
    all_vec, labels, test_size=0.30
)

chi_model.fit(chi_x_train, chi_y_train)
unman_model.fit(unman_x_train, unman_y_train)
stud_model.fit(stud_x_train, stud_y_train)
mid_model.fit(mid_x_train, mid_y_train)
all_model.fit(X=all_x_train, y=all_y_train)


chi_pred = chi_model.predict(chi_x_test)
stud_pred = stud_model.predict(stud_x_test)
unman_pred = unman_model.predict(unman_x_test)
middles_pred = mid_model.predict(mid_x_test)
all_pred = all_model.predict(all_x_test)

report_chi = [
    accuracy_score(chi_y_test, chi_pred),
    f1_score(chi_y_test, chi_pred),
    precision_score(chi_y_test, chi_pred),
    recall_score(chi_y_test, chi_pred),
]
report_uman = [
    accuracy_score(unman_y_test, unman_pred),
    f1_score(unman_y_test, unman_pred),
    precision_score(unman_y_test, unman_pred),
    recall_score(unman_y_test, unman_pred),
]
report_stud = [
    accuracy_score(stud_y_test, stud_pred),
    f1_score(stud_y_test, stud_pred),
    precision_score(stud_y_test, stud_pred),
    recall_score(stud_y_test, stud_pred),
]
report_mid = [
    accuracy_score(mid_y_test, middles_pred),
    f1_score(mid_y_test, middles_pred),
    precision_score(mid_y_test, middles_pred),
    recall_score(mid_y_test, middles_pred),
]
report_all = [
    accuracy_score(all_y_test, all_pred),
    f1_score(all_y_test, all_pred),
    precision_score(all_y_test, all_pred),
    recall_score(all_y_test, all_pred),
]

print("1", report_chi)
print("2", report_uman)
print("3", report_stud)
print("4", report_mid)
print("5", report_all)
