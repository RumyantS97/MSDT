class CharacterFinder:
    @staticmethod
    def fetch_data_from_server(url: str) -> str:
        pass

    @staticmethod
    def find_character(input_str: str, target: str) -> int:
        for i in range(len(input_str)):
            if input_str[i] == target:
                return i
        return -1

    @staticmethod
    def find_character_from_url(url: str, target: str) -> int:
        data = CharacterFinder.fetch_data_from_server(url)
        return CharacterFinder.find_character(data, target)