from english_words import get_english_words_set
import math


class Hangman:
    def __init__(self, word, lives=6):
        self.word = word.lower()
        self.word_length = len(self.word)
        self.remaining_lives = lives
        self.game_over = False
        self.remaining_words = []
        self.given_indices = [i for i in range(self.word_length) if self.word[i] != "_"]
        self.guessed_letters = {self.word[index] for index in self.given_indices}

    @staticmethod
    def _safe_log2(x):
        return math.log2(x) if x > 0 else 0

    @staticmethod
    def _remove_nones(lst):
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

    def get_optimal_letter_using_entropy(self, get_entropy=False):
        letter_entropy = {}
        total_words = len(self.remaining_words)

        if total_words == 0:
            return None

        for letter in set("".join(self.remaining_words)):
            if letter in self.guessed_letters:
                continue

            # Create position-based patterns for each word
            pattern_counts = {}
            for word in self.remaining_words:
                # Create pattern of positions where letter appears
                pattern = tuple(i for i, char in enumerate(word) if char == letter)
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1

            # Calculate entropy using position patterns
            entropy = 0
            for count in pattern_counts.values():
                p = count / total_words
                if p > 0:
                    entropy -= p * self._safe_log2(p)

            letter_entropy[letter] = entropy

        optimal_letter = max(letter_entropy, key=letter_entropy.get)
        return optimal_letter, (
            letter_entropy[optimal_letter] if get_entropy else optimal_letter
        )


if __name__ == "__main__":
    game = Hangman("a__l_")
    game.start_game()
    print(game.guessed_letters)
    print(game.remaining_words)
    print(game.get_optimal_letter_using_entropy(get_entropy=True))
