import pymorphy3


class WordExistenceChecker:
    def __init__(self):
        self.morph = pymorphy3.MorphAnalyzer()

    def is_valid_word(self, word: str) -> bool:
        """
        :param word: Входное слово
        :return: Является ли слово существительным
        """
        res = self.morph.parse(word)
        for i in res:
            if {"NOUN"} in i.tag and i.normal_form.lower().replace("ё", "е") == word:
                return True
            else:
                print(f"Incorrect tags: {i}")
        print("--------------")
        return False
