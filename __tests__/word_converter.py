class WordConverter:
    def __init__(self, word:str):
        self.word = word

    def snakecase(self, suffix:str='_') -> str:
        formatted_word = self.word
        word_length = len(self.word)
        new_first_index = 0

        for index in range(word_length):
            letter:str = self.word[index]
            if letter == letter.upper():

                # More than two words
                if formatted_word.rfind(suffix) == len(formatted_word) - 1:
                    formatted_word = f"{formatted_word}{self.word[new_first_index:index]}_"
                # Exactly two words
                else:
                    formatted_word = f"{self.word[new_first_index:index]}{suffix}"

                new_first_index = index

            if index+1 == word_length:
                formatted_word += self.word[new_first_index:word_length]
        return formatted_word

def sample_conversion_snakecase():
    list = (
        "apiKey",
        "authDomain",
        "projectId",
        "storageBucket",
        "messagingSenderId",
        "appId",
        "measurementId",
    )

    for entry in list:
        formatted_word = WordConverter(entry).snakecase()
        print(formatted_word.upper()+'= ')