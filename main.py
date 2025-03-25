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
        """
        Returns log2 of x if x > 0, else returns 0. Conventional in entropy calculations.
        """
        return math.log2(x) if x > 0 else 0

    @staticmethod
    def _remove_nones(lst):
        """
        Removes all None values from a list. Used to filter out words that don't match the pattern.
        """
        return [item for item in lst if item is not None]

    def start_game(self):
        self.filter_dictionary()

    def filter_dictionary(self):
        """
        Filters the dictionary of English words based on the current game state.
        This method applies multiple filtering criteria to narrow down potential word matches:
        1. Filters words to match the length of the target word
        2. Ensures known letter positions (given indices) match with the target word
        3. Verifies the count of guessed letters matches with the target word

        The filtering process modifies self.remaining_words to contain only valid candidates
        that could be the target word based on current game knowledge.

        Attributes:
            self.word (str): The target word with underscores (_) for unknown letters till now
            self.given_indices (list): Indices where letters are already known
            self.guessed_letters (list): Letters that have been guessed
            self.remaining_words (list): List of potential word matches
        Returns:
            None: Updates self.remaining_words in place
        """
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
        """
        Determines the optimal letter to guess next based on information entropy.
        This method uses information theory principles to calculate the most informative letter
        to guess. It does this by:
        1. Calculating position-based patterns for each potential letter
        2. Computing Shannon entropy for these patterns
        3. Selecting the letter that provides maximum information gain

        The entropy calculation considers both the frequency of letters and their positions
        in words, making it more sophisticated than simple frequency analysis.

        Args:
            get_entropy (bool, optional): If True, returns both the optimal letter and its
                entropy value. If False, returns only the letter. Defaults to False.
        Returns:
            Union[Tuple[str, float], str]: If get_entropy is True, returns a tuple of
                (optimal_letter, entropy_value). If False, returns just the optimal_letter.
                Returns None if no remaining words are available.
        Example:
            >>> solver = Hangman(...)
            >>> letter = solver.get_optimal_letter_using_entropy()
            >>> letter, entropy = solver.get_optimal_letter_using_entropy(get_entropy=True)
        """
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
        return (
            optimal_letter
            if not get_entropy
            else (optimal_letter, letter_entropy[optimal_letter])
        )


if __name__ == "__main__":
    game = Hangman("a__l_")
    game.start_game()
    print(game.guessed_letters)
    print(game.remaining_words)
    print(game.get_optimal_letter_using_entropy(get_entropy=True))
