from english_words import get_english_words_set


class Hangman:
    def __init__(self, word, lives=6):
        self.word = word.lower()
        self.word_length = len(self.word)
        self.remaining_lives = lives
        self.game_over = False
        self.remaining_words = []
        self.given_indices = [i for i in range(self.word_length) if self.word[i] != "_"]
        self.guessed_letters = {self.word[index] for index in self.given_indices}

    def _remove_nones(self, lst):
        return [item for item in lst if item is not None]

    def start_game(self):
        self.filter_dictionary()

    def filter_dictionary(self):
        dict_words = get_english_words_set(["web2"], lower=True)
        self.remaining_words = [
            word for word in dict_words if len(word) == len(self.word)
        ]

        for dict_word in self.remaining_words:
            match = True
            for i in self.given_indices:
                if dict_word[i] != self.word[i]:
                    match = False
                    break
            if not match:
                self.remaining_words[self.remaining_words.index(dict_word)] = None

        self.remaining_words = self._remove_nones(self.remaining_words)

        for word in self.remaining_words:
            for letter in self.guessed_letters:
                if word.count(letter) != self.word.count(letter):
                    self.remaining_words[self.remaining_words.index(word)] = None
                    break

        self.remaining_words = self._remove_nones(self.remaining_words)


if __name__ == "__main__":
    game = Hangman("a__l_")
    game.start_game()
    print(game.guessed_letters)
    print(game.remaining_words)
