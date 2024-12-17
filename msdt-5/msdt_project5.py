class TrimSpaces:
    @staticmethod
    def trim_extra_spaces(text: str) -> str:
        return ' '.join(text.split())
