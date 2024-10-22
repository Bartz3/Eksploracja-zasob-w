import os
from collections import Counter
import re
import glob
import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import pandas as pd

from typing import List


global merged_text
arch_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Arch"
bud_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Bud"
elek_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Elek"
inf_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Inf"
mech_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Mech"
zarz_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Zarz"
main_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11"

link_list = [arch_path, bud_path, elek_path, inf_path, mech_path, zarz_path]

# Funkcja do wczytywania wszystkich plików tekstowych z folderów i podfolderów
def load_text_from_folders(main_folder_path):
    all_text = []  # Lista do przechowywania tekstu z wszystkich plików

    for folder in os.listdir(main_folder_path):
        folder_path = os.path.join(main_folder_path, folder)
        if os.path.isdir(folder_path):
            txt_files = glob.glob(os.path.join(folder_path, '*.txt'))
            for file_path in txt_files:
                with open(file_path, 'r', encoding='utf-8') as file:
                    file_content = file.read()
                    all_text.append(file_content)
    return "\n".join(all_text)
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
    #print(words)
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

def most_popular_words(num_words):
    for path in link_list:
        print(path)
        merged_text = read_and_merge_txt_files(elek_path)
        words = preprocess_text(merged_text,stopWordsOn)
        most_common_words = get_most_common_words(words, num_words)
        print("Najczęściej występujące słowa z stopwords:" if stopWordsOn else
              "Najczęściej występujące słowa bez stopwords:")
        for word, count in most_common_words:
            print(f"{word}: {count}")
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()  # Czytamy plik i tworzymy listę słów
    return stopwords
def clean_text(text):
    # Usuwanie znaków interpunkcyjnych
    text = re.sub(r'[^\w\s]', '', text)
    # Usuwanie liczb
    text = re.sub(r'\d+', '', text)
    # Konwersja na małe litery i dzielenie na słowa
    words = text.lower().split()
    return words

if __name__ == "__main__":
    #departments = ["Arch", "Bud", "Elek", "Inf", "Mech", "Zarz"]
    #folder_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Inf"
    stopwords_file = "polish.stopwords.txt"

    stopwords = load_stopwords("polish.stopwords.txt")
    stopWordsOn=False
    # most_popular_words(10)

    # documents = [
    #     "Szybki brązowy lis przeskoczył nad leniwym psem.",
    #     "Nigdy nie przeskakuj nad leniwym psem szybko.",
    #     "Lisy są szybkie i sprytne.",
    #     "Psy są lojalne i leniwe."
    # ]
    all_text = load_text_from_folders(main_path)

    # Wyświetlenie części wynikowego tekstu (opcjonalnie)
    #print(all_text[:1000])  # Wyświetla pierwsze 1000 znaków wczytanego tekstu

    # merged_text = read_and_merge_txt_files(elek_path)
    # words = clean_text(merged_text)
    #
    # documents = words
    # # print(merged_text)
    #
    # vectorizer_bow = CountVectorizer(stop_words=stopwords)  # Bag of words
    # vectorizer_binary = CountVectorizer(stop_words=stopwords, binary=True)  # Binarny
    #
    #
    # vectorizer_tfidf = TfidfVectorizer(stop_words=stopwords)
    #
    #
    # X_bow = vectorizer_bow.fit_transform(documents)  # Bag of words
    # X_binary = vectorizer_binary.fit_transform(documents)  # Binary
    # X_tfidf = vectorizer_tfidf.fit_transform(documents)  # TF-IDF
    #
    #
    # df_bow = pd.DataFrame(X_bow.toarray(), columns=vectorizer_bow.get_feature_names_out())
    # df_binary = pd.DataFrame(X_binary.toarray(), columns=vectorizer_binary.get_feature_names_out())
    # df_tfidf = pd.DataFrame(X_tfidf.toarray(), columns=vectorizer_tfidf.get_feature_names_out())
    #
    # df_bow.to_csv("bag_of_words.csv", index=False)
    # df_binary.to_csv("binary_representation.csv", index=False)
    # df_tfidf.to_csv("tfidf_representation.csv", index=False)