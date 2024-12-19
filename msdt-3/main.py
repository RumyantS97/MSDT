from functions import *
from paths import *


file = read_csv(CSV)
patterns = read_json(PATTERNS)
result = get_list(file, patterns)
print(len(result))