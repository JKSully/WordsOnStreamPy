import sys
import getopt
import string
from collections import defaultdict
from operator import itemgetter


class WordPlayer:
    def __init__(self):
        self.dictionary = []
        self.min_length = 4
        self.missing = False
        self.fake = False
        self.to_sort = False
        self.letter_count = defaultdict(int)
        self.letter_bank = ''

    def play_words(self, letter_bank):
        valid_words = [word for word in self.dictionary if len(word) >= self.min_length and self.is_valid_word(word, letter_bank)]
        valid_words.sort()
        return valid_words

    def is_valid_word(self, word, letter_bank):
        bank = list(letter_bank)
        for char in word:
            if char not in bank:
                return False
            bank.remove(char)
        return True

    def num_words_valid(self, letter_bank):
        valid_words = self.play_words(letter_bank)
        return len(valid_words)

    def init(self, argv):
        self.letter_bank = argv[-1]
        try:
            opts, args = getopt.getopt(argv, "l:msf", ["length=", "missing", "fake", "sort"])
        except getopt.GetoptError:
            self.show_usage_and_exit()

        for opt, arg in opts:
            if opt in ("-l", "--length"):
                self.min_length = int(arg)
            elif opt in ("-m", "--missing"):
                self.missing = True
            elif opt in ("-f", "--fake"):
                self.fake = True
            elif opt in ("-s", "--sort"):
                self.to_sort = True

    def load_dictionary(self, dictionary_file):
        for line in dictionary_file:
            word = line.strip()
            self.dictionary.append(word)
            if self.fake or self.missing:
                for char in word:
                    self.letter_count[char] += 1

    def play(self):
        valid_words = self.play_words(self.letter_bank)

        print("VALID WORDS")
        count = 0

        if self.to_sort:
            valid_words.sort(key=lambda x: (len(x), x))

        for word in valid_words:
            print(f"{word:<4}", end='\t')
            count += 1
            if count == 5:
                count = 0
                print()

        print()

        if self.fake:
            self.calculate_letter_probabilities()

        if self.missing:
            self.calculate_missing_letter_counts()

    def calculate_letter_probabilities(self):
        print("Probability of real letter")
        total_count = sum(self.letter_count[char] for char in self.letter_bank)
        for char in self.letter_bank:
            percent = (self.letter_count[char] / total_count) * 100
            print(f"{char}: {percent:.1f}%")
        print()

    def calculate_missing_letter_counts(self):
        cool_bank = [(i, self.num_words_valid(self.letter_bank + i)) for i in string.ascii_lowercase]
        cool_bank.sort(key=itemgetter(1, 0), reverse=True)
        counter = 0

        print("Number of words added with each missing letter")
        for k in cool_bank:
            print(f"{k[0]}: {k[1]}\t", end='')
            counter += 1
            if counter == 5:
                print()
                counter = 0

    def show_usage_and_exit(self):
        print("Usage: word_player.py [-l <length>] [-m] [-f] [-s] <letter_bank>")
        sys.exit(2)


def main(argv):
    try:
        player = WordPlayer()
        player.init(argv)

        with open("words.txt", "r") as file:
            player.load_dictionary(file)

        player.play()
    except Exception as e:
        print(e)
        sys.exit(-1)


if __name__ == "__main__":
    main(sys.argv[1:])

