import os
from collections import Counter
import re

global merged_text

arch_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Arch"
bud_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Bud"
elek_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Elek"
inf_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Inf"
mech_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Mech"
zarz_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Zarz"

link_list = [arch_path, bud_path, elek_path, inf_path, mech_path, zarz_path]
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
link_list = [arch_path, bud_path, elek_path, inf_path, mech_path, zarz_path]
def most_popular_words(num_words):
    for path in link_list:
        print(path)
        merged_text = read_and_merge_txt_files(path)
        words = preprocess_text(merged_text,stopWordsOn)
        most_common_words = get_most_common_words(words, num_words)
        if path == arch_path:  print("Wydział Architektury")
        elif path == bud_path: print("Wydział Budownictwa ")
        elif path == elek_path:print("Wydział Elektryczny ")
        elif path == inf_path: print("Wydział Informatyki ")
        elif path == mech_path: print("Wydział Mechaniczny")
        elif path == zarz_path: print("Wydział Inżynierii i Zarządzania")
        for word, count in most_common_words:
            print(f"{word}: {count}")
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()  # Czytamy plik i tworzymy listę słów
    return stopwords


if __name__ == "__main__":
    #departments = ["Arch", "Bud", "Elek", "Inf", "Mech", "Zarz"]
    #folder_path = "C:\\Users\\Bartucci\\Desktop\\Mag2\\EZI\\11\\Inf"
    stopwords_file = "polish.stopwords.txt"

    stopwords = load_stopwords("polish.stopwords.txt")
    stopWordsOn=True
    most_popular_words(10)

