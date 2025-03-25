from english_words import get_english_words_set


class Hangman:
    def __init__(self, word, lives=6):
        self.word = word.lower()
        self.word_length = len(self.word)
        self.remaining_lives = lives
        self.game_over = False
        self.remaining_words = set()
        self.given_indices = [i for i in range(self.word_length) if self.word[i] != "_"]
        self.guessed_letters = {self.word[index] for index in self.given_indices}

    def start_game(self):
        self.filter_dictionary(self.word_length)

    def filter_dictionary(self, word_length):
        dict_words = get_english_words_set(["web2"], lower=True)
        filtered_words = {word for word in dict_words if len(word) == word_length}

        for dict_word in filtered_words:
            match = True
            for i in self.given_indices:
                if dict_word[i] != self.word[i]:
                    match = False
                    break
            if match:
                self.remaining_words.add(dict_word)

        filtered_words = self.remaining_words.copy()

        for letter in self.guessed_letters:
            for word in filtered_words:
                if word.count(letter) != self.word.count(letter):
                    self.remaining_words.remove(word)


if __name__ == "__main__":
    game = Hangman("s_mm_tr_")
    game.start_game()
    print(game.guessed_letters)
    print(game.remaining_words)
