from english_words import get_english_words_set


# brute = input("Enter the word: ")
class Hangman:
    # whats the idea
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
            for i in self.given_indices:
                if dict_word[i] == self.word[i]:
                    self.remaining_words.add(dict_word)

        for dict_word in self.remaining_words:
            for letter in self.guessed_letters:
                if dict_word.count(letter) == self.word.count(letter):
                    self.final_words.add(dict_word)
        # _ _ a _ n  -> Make the engine filter out words that match this pattern, and extract them.


if __name__ == "__main__":
    game = Hangman("a__")
    game.start_game()
    print(game.guessed_letters)
    print(game.final_words)
