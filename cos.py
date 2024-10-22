import os
import re
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


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
        return ' '.join(filtered_words)  # Zwraca tekst jako string (potrzebne do wektoryzacji)
    else:
        return ' '.join(words)


# Funkcja do wczytywania stopwords
def load_stopwords(stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return stopwords


# Funkcja do porównania za pomocą podobieństwa cosinusowego
def compare_departments_cosine_similarity(department_texts, method='tfidf'):
    department_names = list(department_texts.keys())
    documents = list(department_texts.values())

    # Wybór metody wektoryzacji: Bag of Words lub TF-IDF
    if method == 'bow':
        vectorizer = CountVectorizer()
    elif method == 'tfidf':
        vectorizer = TfidfVectorizer()

    # Konwersja tekstów do macierzy wektorów
    vectors = vectorizer.fit_transform(documents)

    # Obliczenie macierzy podobieństwa cosinusowego
    cosine_sim = cosine_similarity(vectors)

    # Wyświetlenie wyników podobieństwa cosinusowego
    for i in range(len(department_names)):
        for j in range(i + 1, len(department_names)):
            dep1 = department_names[i]
            dep2 = department_names[j]
            similarity = cosine_sim[i][j]
            print(f"Podobieństwo cosinusowe między {dep1} a {dep2}: {similarity:.4f}")


# Główna funkcja
def most_popular_words(stopwords, stopWordsOn, method='tfidf'):
    department_texts = {}

    # Lista ścieżek do folderów wydziałów
    link_list = [arch_path, bud_path, elek_path, inf_path, mech_path, zarz_path]

    # Przetwarzanie każdego wydziału
    for path in link_list:
        merged_text = read_and_merge_txt_files(path)
        processed_text = preprocess_text(merged_text, stopWordsOn, stopwords)

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

        # Zachowujemy przetworzony tekst dla danego wydziału
        department_texts[department_name] = processed_text

    # Porównanie wydziałów za pomocą podobieństwa cosinusowego
    compare_departments_cosine_similarity(department_texts, method)


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
    # Użyj 'bow' (Bag of Words) lub 'tfidf' (TF-IDF)
    most_popular_words(stopwords, stopWordsOn, method='bow')
