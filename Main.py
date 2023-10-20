import random as rand
from WordState import WordState  # Use as needed.
import string
import nltk
from nltk.corpus import stopwords
from collections import Counter
import re

# Some sentences to test your code on...
test_sentences = [
    "hello there friend",
    "hello there good friend",
    "hello there my good friend",
    "hello my friend",
    "hello my good friend",
    "good day friend",
    "good morning friend",
    "good morning to you my friend",
    "good morning to you my good friend",
]

# A simple "pre-trained model"/graph derived from above sentences with words and corresponding frequencies.
states = {
    "#": {"hello": 5, "good": 4},
    "hello": {"there": 3, "my": 2},
    "good": {"friend": 4, "day": 1, "morning": 3},
    "there": {"friend": 1, "good": 1, "my": 1},
    "my": {"good": 2, "friend": 2},
    "friend": {},
    "day": {"friend": 1},
    "morning": {"friend": 1, "to": 2},
    "to": {"you": 2},
    "you": {"my": 1},
}


# Write your implementation here...
def read_and_parse(text_from_file):
    # Lower casing
    text_from_file = [line.lower() for line in text_from_file]

    PUNCT_TO_REMOVE = string.punctuation

    # Punctuations Removal
    def remove_punctuation(text):
        return text.translate(str.maketrans("", "", PUNCT_TO_REMOVE))

    text_from_file = [remove_punctuation(line) for line in text_from_file]

    # Stopwords Removal
    nltk.download("stopwords")
    STOPWORDS = set(stopwords.words("english"))

    def remove_stopwords(text):
        return " ".join([word for word in text.split() if word not in STOPWORDS])

    text_from_file = [remove_stopwords(line) for line in text_from_file]

    # Frequent words removal

    all_words = " ".join(text_from_file).split()
    cnt = Counter(all_words)

    FREQWORDS = set([w for (w, wc) in cnt.most_common(5)])

    def remove_freqwords(text):
        return " ".join([word for word in text.split() if word not in FREQWORDS])

    text_from_file = [remove_freqwords(line) for line in text_from_file]

    # Rare words removal
    n_rare_words = 10
    RAREWORDS = set([w for (w, wc) in cnt.most_common()[: -n_rare_words - 1 : -1]])

    def remove_rarewords(text):
        return " ".join([word for word in text.split() if word not in RAREWORDS])

    text_from_file = [remove_rarewords(line) for line in text_from_file]

    # Emojis and emoticons removal
    def remove_emoji(string):
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F1E0-\U0001F1FF"
            "\U00002702-\U000027B0"
            "\U000024C2-\U0001F251"
            "]+",
            flags=re.UNICODE,
        )
        return emoji_pattern.sub(r"", string)

    text_from_file = [remove_emoji(line) for line in text_from_file]

    # Urls removal
    def remove_urls(text):
        url_pattern = re.compile(r"https?://\S+|www\.\S+")
        return url_pattern.sub(r"", text)

    text_from_file = [remove_urls(line) for line in text_from_file]

    # remove empty strings
    text_from_file = [line for line in text_from_file if line.strip() != ""]

    # Save preprocessed text to new file
    with open("preprocessed.txt", "w") as out_file:
        for line in text_from_file:
            out_file.write(line + "\n")
    return text_from_file


def construct_weighted_graph(sentences):
    graph = {}

    for sentence in sentences:
        words = sentence.split()
        for i in range(len(words)):
            if i == 0:
                graph.setdefault("#", {}).setdefault(words[i], 0)
                graph["#"][words[i]] += 1
            else:
                graph.setdefault(words[i - 1], {}).setdefault(words[i], 0)
                graph[words[i - 1]][words[i]] += 1

    return graph


def generate_random_sentence(graph, max_length=10):
    current_word = "#"
    sentence = []

    while len(sentence) < max_length:
        if current_word not in graph:
            break

        word_state = WordState()

        # Populate the word_state instance with next words from the graph
        for next_word, freq in graph[current_word].items():
            for _ in range(freq):
                word_state.add_next_word(next_word)

        if not word_state.has_next():
            break

        next_word = word_state.get_next()
        if next_word == "#":
            break

        sentence.append(next_word)
        current_word = next_word

    return " ".join(sentence)


def generate_sentences(graph, num_sentences=5):
    sentences = []
    for _ in range(num_sentences):
        sentences.append(generate_random_sentence(graph))
    return sentences
