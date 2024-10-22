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
import os
import re
from collections import Counter


# Funkcja do wczytywania i łączenia plików z folderu
def read_and_merge_txt_files(folder_path):
    merged_text = ""
    for filename in os.listdir(folder_path):
        if filename.endswith(".txt"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, 'r', encoding='utf-8') as file:
                merged_text += file.read() + " "
    return merged_text


# Funkcja do przetwarzania tekstu
def preprocess_text(text, stopWordsOn, stopwords):
    text = re.sub(r'[^\w\s]', '', text)  # Usuwa znaki interpunkcyjne
    text = re.sub(r'\d+', '', text)  # Usuwa liczby
    words = text.lower().split()  # Konwertuje na małe litery i dzieli na słowa
    if stopWordsOn:
        filtered_words = [word for word in words if word not in stopwords]
        return filtered_words
    else:
        return words


# Funkcja do liczenia wystąpień słów
def get_word_frequencies(words):
    return Counter(words)


# Funkcja do wczytywania stopwords
def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return stopwords


# Funkcja do porównania wystąpień słów między wydziałami, wypisuje tylko ilość wspólnych słów
def compare_departments_word_frequencies(department_word_counts):
    department_names = list(department_word_counts.keys())

    # Porównanie każdego wydziału z każdym
    for i in range(len(department_names)):
        for j in range(i + 1, len(department_names)):
            dep1 = department_names[i]
            dep2 = department_names[j]
            common_words = set(department_word_counts[dep1].keys()) & set(department_word_counts[dep2].keys())

            # Wypisujemy tylko liczbę wspólnych słów
            print(f"\nPorównanie: {dep1} vs {dep2}")
            print(f"Liczba wspólnych słów: {len(common_words)}")


# Główna funkcja
def most_popular_words(stopwords, stopWordsOn, num_words):
    department_word_counts = {}

    # Lista ścieżek do folderów wydziałów
    link_list = [arch_path, bud_path, elek_path, inf_path, mech_path, zarz_path]

    # Przetwarzanie każdego wydziału
    for path in link_list:
        merged_text = read_and_merge_txt_files(path)
        words = preprocess_text(merged_text, stopWordsOn, stopwords)
        word_frequencies = get_word_frequencies(words)

        # Pobieranie nazwy wydziału na podstawie ścieżki
        if path == arch_path:
            department_name = "Architektura"
        elif path == bud_path:
            department_name = "Budownictwo"
        elif path == elek_path:
            department_name = "Elektryczny"
        elif path == inf_path:
            department_name = "Informatyka"
        elif path == mech_path:
            department_name = "Mechaniczny"
        elif path == zarz_path:
            department_name = "Zarządzanie"

        # Zachowujemy dane dla danego wydziału
        department_word_counts[department_name] = word_frequencies

    # Porównanie wystąpień słów między wydziałami
    compare_departments_word_frequencies(department_word_counts)


# Funkcja wczytująca stopwords
def load_stopwords(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        stopwords = file.read().splitlines()  # Czytamy plik i tworzymy listę słów
    return stopwords


if __name__ == "__main__":
    # Ścieżki do folderów z danymi wydziałów
    arch_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Arch"
    bud_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Bud"
    elek_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Elek"
    inf_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Inf"
    mech_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Mech"
    zarz_path = "E:\\OneDrivePB\\OneDrive - Politechnika Białostocka\\Pulpit\\Dane\\Zarz"

    stopwords_file = "polish.stopwords.txt"

    # Wczytaj stopwords
    stopwords = load_stopwords(stopwords_file)
    stopWordsOn = True

    # Uruchomienie porównania słów między wydziałami
    most_popular_words(stopwords, stopWordsOn, 10)
