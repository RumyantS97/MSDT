WEATHER = ['жарко',  # [0; 30] градусов
           'тепло',
           'холодно']

EMPLOYMENT = ['свободен',  # [0; 24] часы
              'есть время',
              'занят']

PICNIC = ['едем',  # [0; 1]
          'вероятно поедем',
          'не едем']

KNOWLEDGE_BASE = {'Если жарко и свободен, то': 'вероятно едем',
                  'Если холодно или занят, то': 'не едем',
                  'Если тепло и свободен, то': 'едем',
                  'Если тепло и есть время, то': 'вероятно едем',
                  'Если холодно и есть время, то': 'не едем',
                  'Если тепло и занят, то': 'не едем'}


def weather(temperature):
    if temperature < 15:
        if temperature > 0 and temperature < 15:
            return 1 - temperature / 15
        else:
            return 0
    elif temperature >= 15 and temperature <= 25:
        if temperature < 15 or temperature > 25:
            return 0
        elif temperature >= 15 and temperature < 17:
            return 0.5 * temperature - 7.5
        elif temperature >= 17 and temperature <= 23:
            return 1
        elif temperature > 23 and temperature <= 25:
            return 12.5 - 0.5 * temperature
    elif temperature > 25:
        if temperature < 25:
            return 0
        elif temperature >= 25 and temperature < 27:
            return 0.5 * temperature - 12.5
        elif temperature >= 27:
            return 1


def employment(hours):
    if hours == 0:
        if hours == 0:
            return 1
        else:
            return 0
    elif hours > 0 and hours < 6:
        if hours < 2 or hours > 6:
            return 0
        elif hours >= 2 and hours < 4:
            return 0.5 * hours - 1
        elif hours >= 4 and hours < 6:
            return 3 - 0.5 * hours
    elif hours >= 6:
        if hours < 6:
            return 0
        elif hours >= 6 and hours <= 8:
            return 0.5 * hours - 3
        elif hours > 8:
            return 1


def picnic(probability):
    if probability >= 0.8:
        if probability == 1:
            return 1
        elif probability < 1 and probability >= 0.8:
            return 5 * probability - 4
        elif probability < 0.8:
            return 0
    elif probability < 0.8 and probability >= 0.4:
        if probability < 0.4 or probability > 0.6:
            return 0
        elif probability >= 0.4 and probability <= 0.5:
            return 10 * probability - 4
        elif probability > 0.5 and probability <= 0.6:
            return 6 - 10 * probability
    elif probability < 0.4:
        if probability == 0:
            return 1
        elif probability > 0 and probability <= 0.2:
            return 1 - 5 * probability
        elif probability > 0.2:
            return 0


def interpretator(temperature, hour):
    if temperature < 15:
        t = WEATHER[2]
    elif temperature >= 15 and temperature <= 25:
        t = WEATHER[1]
    elif temperature > 25:
        t = WEATHER[0]

    if hour == 0:
        emp = EMPLOYMENT[2]
    elif hour > 0 and hour < 6:
        emp = EMPLOYMENT[1]
    elif hour >= 6:
        emp = EMPLOYMENT[0]

    key = KNOWLEDGE_BASE.keys()
    for k in key:
        if t in k and emp in k: return k
    return 0


def calculation(temperature, hours):
    return weather(temperature), employment(hours)