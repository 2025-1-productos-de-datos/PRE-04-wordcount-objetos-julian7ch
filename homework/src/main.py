import os
import sys


class ParseArgsMixin:
    def parse_args(self):

        if len(sys.argv) != 3:
            print("Usage: python3 -m homework <input_folder> <output_folder>")
            sys.exit(1)

        self.input_folder = sys.argv[1]
        self.output_folder = sys.argv[2]


class CountWordsMixin:
    def count_words(self):
        """Count occurrences of each word using a plain dictionary."""
        word_counts = {}
        for word in self.words:
            word_counts[word] = word_counts.get(word, 0) + 1
        self.word_counts = word_counts


class PreprocessLinesMixin:
    def preprocess_lines(self):
        """Preprocess lines by normalizing and cleaning text."""

        self.preprocessed_lines = [line.lower().strip() for line in self.lines]


class ReadAllLinesMixin:

    def read_all_lines(self):
        """Read all lines from all files in the input folder."""

        lines = []
        for filename in os.listdir(self.input_folder):
            file_path = os.path.join(self.input_folder, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                lines.extend(f.readlines())

        self.lines = lines


class SplitIntoWordsMixin:
    def split_into_words(self):
        """Split lines into individual words and clean punctuation."""

        words = []

        for line in self.preprocessed_lines:
            words.extend(word.strip(",.!?") for word in line.split())

        self.words = words


class WriteWordCountsMixin:
    def write_word_counts(self):
        """Write word counts to a file in the output folder."""

        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

        output_file = os.path.join(self.output_folder, "wordcount.tsv")

        with open(output_file, "w", encoding="utf-8") as f:
            for word, count in self.word_counts.items():
                f.write(f"{word}\t{count}\n")


class WordCountApp(
    ParseArgsMixin,
    ReadAllLinesMixin,
    PreprocessLinesMixin,
    SplitIntoWordsMixin,
    CountWordsMixin,
    WriteWordCountsMixin,
):
    def __init__(self):
        self.input_folder = None
        self.output_folder = None
        self.lines = None
        self.preprocessed_lines = None
        self.words = None
        self.word_counts = None

    def run(self):

        self.parse_args()
        self.read_all_lines()
        self.preprocess_lines()
        self.split_into_words()
        self.count_words()
        self.write_word_counts()


if __name__ == "__main__":
    WordCountApp().run()
