from english_words import get_english_words_set


class Hangman:
    def __init__(self, word, liv=6):
        self.word = word.lower()
        self.word_length = len(self.word)
        self.remaining_lives = liv
        self.game_over = False
        self.remaining_words = set()
        self.final_words = set()
        self.given_indices = [i for i in range(self.word_length) if self.word[i] != "_"]
        self.guessed_letters = [self.word[index] for index in self.given_indices]

    def start_game(self):
        self.filter_dictionary(self.word_length)

    def filter_dictionary(self, word_length):
        dict_words = list(get_english_words_set(["web2"], lower=True))
        filtered_words = {word for word in dict_words if len(word) == word_length}

        for dict_word in filtered_words:
            match = True
            for i in self.given_indices:
                if dict_word[i] != self.word[i]:
                    match = False
                    break
            if match:
                self.remaining_words.add(dict_word)

        for dict_word in self.remaining_words:
            match = True
            for i in range(word_length):
                if self.word[i] == "_":
                    continue
                if dict_word[i] != self.word[i]:
                    match = False
                    break
            if match:
                self.final_words.add(dict_word)


if __name__ == "__main__":
    game = Hangman("a_pl_")
    game.start_game()
    print(game.guessed_letters)
    print(game.final_words)
