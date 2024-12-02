from seconds_to_time import seconds_to_dhms


class TimeInput:
    def __init__(self, seconds):
        if not isinstance(seconds, int) or seconds < 0:
            raise ValueError("Ввод должен быть положительным целым числом.")
        self.seconds = seconds

    def convert_to_dhms(self):
        return seconds_to_dhms(self.seconds)