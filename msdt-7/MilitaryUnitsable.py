class MilitaryUnitsable:
    def length(self):
        raise NotImplementedError

    def set_number_units(self, index, num):
        raise NotImplementedError

    def get_number_units(self, index):
        raise NotImplementedError

    def set_name(self, name):
        raise NotImplementedError

    def get_name(self):
        raise NotImplementedError

    def set_civil(self, civil):
        raise NotImplementedError

    def get_civil(self):
        raise NotImplementedError

    def total_number(self):
        raise NotImplementedError