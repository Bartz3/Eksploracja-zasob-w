import os
from collections import Counter
import re

def read_and_merge_txt_files(folder_path):
    # Lista na przechowywanie całej zawartości plików
    merged_text = ""

    # Iterowanie przez pliki w podanym folderze
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                merged_text += file.read() + " "

    return merged_text

def preprocess_text(text, stopWordsOn):
    text = re.sub(r'[^\w\s]', '', text)  # Usuwa znaki interpunkcyjne
    text = re.sub(r'\d+', '', text)      # Usuwa liczby
    words = text.lower().split()         # Konwertuje na małe litery i dzieli na słowa

    if stopWordsOn:
        filtered_words = [word for word in words if word not in stopwords]
        return filtered_words
    else:
        return words

def get_most_common_words(words, top_n=10):
    # Liczenie wystąpień słów
    word_counts = Counter(words)
    # Zwrócenie top_n najczęściej występujących słów
    return word_counts.most_common(top_n)


def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return stopwords


if __name__ == "__main__":
    folder_path = "C:\\Users\\Bartucci\\Desktop\\EZI\\1\\WIiZ"
    stopwords_file = "polish.stopwords.txt"
    stopWordsOn=False

    stopwords = load_stopwords(stopwords_file)
    merged_text = read_and_merge_txt_files(folder_path)
    words = preprocess_text(merged_text,stopWordsOn)
    most_common_words = get_most_common_words(words, top_n=10)

    print("Najczęściej występujące słowa z topwords:" if stopWordsOn else
          "Najczęściej występujące słowa bez stopwords:")
    for word, count in most_common_words:
        print(f"{word}: {count}")
