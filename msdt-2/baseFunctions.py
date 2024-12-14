# Pls add comment about program
"""
This program...
"""

# 1. It's good idea to add comment why we use this packages
# 2. And it's not good idea to import all package.
#    Import only methods that you have used in your code.
import librosa
import os

from scipy.signal import spectrogram
from display import read_file


# It's good idea to add annotations
# E.g.
# get_data_set(directory: str) -> tuple:
#   ...
def get_data_set(directory):
    """
    It's good practice to add comments about what
    your function does. Remember that you work
    not only with computer, but also with peoples ;)
    """
    files_name = os.listdir(directory)
    # It's not good idea to naming fields like this.
    # The name of field should describe what field does
    # and why it creates.
    y = []
    files_names = []
    srs = []
    for file in files_name:
        # It's good idea to work with situation, when
        # directory already have /. For example
        # when we called get_data_set('/etc/')
        # And what about if we work in Windows system?
        # In Windows path includes \ instead /.
        path = directory + "/" + file
        [a, b] = read_file(path)
        y.append(a)
        files_names.append(file)
        srs.append(b)

    return y, files_names, srs

# It's good idea to add annotations
# Why we use this function if we use only 1 method from package?
# Why we cant use only this method (don't forget about comments)
def audio_to_mel(y, sr):
    return librosa.feature.melspectrogram(y=y, sr=sr, n_mels=128, fmax=8000)

# It's good idea to add annotations
def define_class(y1, y2):
    """
    Pls add some comments what this function does.
    """
    dec = 0
    # 1. You can use syntax for check like
    # if first_str and second_str in some_list:
    #      ...
    # instead: first_str in some_list, second_str in some_list etc...
    # 2. It's not good idea to hardcode. You should create universal method.
    # 3. You can use method any() for your function.
    # https://docs-python.ru/tutorial/vstroennye-funktsii-interpretatora-python/funktsija-any/
    # 4. Don't forget about operator ELIF. You don't need to check
    # 2 situations, if one of them already, e.g. TRUE.
    if (("kitchen" in y1) and ("kitchen" in y2)) and (
        ("mi" in y1) and ("mi" in y2)
    ):
        dec = 1
    if (("kitchen" in y1) and ("kitchen" in y2)) and (
        ("android" in y1) and ("android" in y2)
    ):
        dec = 1
    if (("kitchen" in y1) and ("kitchen" in y2)) and (
        ("iphone" in y1) and ("iphone" in y2)
    ):
        dec = 1
    if (("room" in y1) and ("room" in y2)) and (("mi" in y1) and ("mi" in y2)):
        dec = 1
    if (("room" in y1) and ("room" in y2)) and (
        ("android" in y1) and ("android" in y2)
    ):
        dec = 1
    if (("room" in y1) and ("room" in y2)) and (
        ("iphone" in y1) and ("iphone" in y2)
    ):
        dec = 1
    if ("electro" in y1) and ("electro" in y2):
        dec = 1
    if ("second_pink" in y1) and ("second_pink" in y2):
        dec = 1

    return dec

# It's good idea to add annotations.
# It's not idea to write double code. Why we
# use this function, if we already have function
# spectrogram()? And it's not good idea to naming
# new function as spectogramM. You and other
# people can be confused, when they or you will
# be work with that.
def spectrogramm(x):
    f1, t1, s1 = spectrogram(x)
    return f1, t1, s1
