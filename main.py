self.final_guesses = set()
    used_letters = set()

    while True:
        if len(used_letters) >= self.word_length:  # Prevent infinite loops
            break

        # Get the next optimal letter
        self.optimal_letter = self.get_optimal_letter_using_entropy()

        # Ensure it's a new letter
        while self.optimal_letter in used_letters:
            self.optimal_letter = self.get_optimal_letter_using_entropy()

        used_letters.add(self.optimal_letter)
        self.guessed_letters.add(self.optimal_letter)

        # **Add ALL words containing the newly found optimal letter**
        new_words = {word for word in self.remaining_words if self.optimal_letter in word}
        self.final_guesses.update(new_words)

        # Reduce remaining lives
        self.remaining_lives -= 1

        # Stop when the number of words is small enough
        if len(self.final_guesses) <= self.remaining_lives:
            break

    # **If too many words remain, rank and keep only the top 6**
    if len(self.final_guesses) > self.remaining_lives:
        def word_probability(word):
            entropy_score = sum(
                self.get_optimal_letter_using_entropy(get_entropy=True)[1] for letter in set(word)
            )
            match_strength = sum(1 for i in self.given_indices if word[i] == self.word[i])
            return entropy_score + match_strength  # Higher score = more probable word

        # Keep only the **most probable** 6 words
        self.final_guesses = set(
            sorted(self.final_guesses, key=word_probability, reverse=True)[:6]
        )

    return self.final_guesses
