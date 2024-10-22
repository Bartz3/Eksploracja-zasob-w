import os
import re
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer


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


# Funkcja do wyświetlania top 10 słów w różnych reprezentacjach dokumentu
def display_top_words(department_texts, stopwords, stopWordsOn):
    department_names = list(department_texts.keys())
    documents = list(department_texts.values())

    # Reprezentacja Bag of Words
    vectorizer_bow = CountVectorizer(binary=False)
    X_bow = vectorizer_bow.fit_transform(documents)
    feature_names_bow = vectorizer_bow.get_feature_names_out()

    # Reprezentacja Binary
    vectorizer_binary = CountVectorizer(binary=True)
    X_binary = vectorizer_binary.fit_transform(documents)
    feature_names_binary = vectorizer_binary.get_feature_names_out()

    # Reprezentacja TF-IDF
    vectorizer_tfidf = TfidfVectorizer()
    X_tfidf = vectorizer_tfidf.fit_transform(documents)
    feature_names_tfidf = vectorizer_tfidf.get_feature_names_out()

    # Reprezentacja TF (CountVectorizer bez binary)
    vectorizer_tf = CountVectorizer(binary=False)
    X_tf = vectorizer_tf.fit_transform(documents)
    feature_names_tf = vectorizer_tf.get_feature_names_out()

    # Wyświetlenie top 10 słów dla każdego wydziału w każdej reprezentacji
    for i, department_name in enumerate(department_names):
        print(f"\n--- {department_name} ---")

        # Top 10 Bag of Words
        print("Bag of Words:")
        top_bow_indices = X_bow[i].toarray()[0].argsort()[-10:][::-1]
        top_bow_words = [(feature_names_bow[idx], X_bow[i, idx]) for idx in top_bow_indices]
        for word, count in top_bow_words:
            print(f"{word}: {count}")

        # Top 10 Binary
        print("\nBinary:")
        top_binary_indices = X_binary[i].toarray()[0].argsort()[-10:][::-1]
        top_binary_words = [(feature_names_binary[idx], X_binary[i, idx]) for idx in top_binary_indices]
        for word, count in top_binary_words:
            print(f"{word}: {count}")

        # Top 10 TF-IDF
        print("\nTF-IDF:")
        top_tfidf_indices = X_tfidf[i].toarray()[0].argsort()[-10:][::-1]
        top_tfidf_words = [(feature_names_tfidf[idx], X_tfidf[i, idx]) for idx in top_tfidf_indices]
        for word, score in top_tfidf_words:
            print(f"{word}: {score:.4f}")

        # Top 10 TF
        print("\nTF (Term Frequency):")
        top_tf_indices = X_tf[i].toarray()[0].argsort()[-10:][::-1]
        top_tf_words = [(feature_names_tf[idx], X_tf[i, idx]) for idx in top_tf_indices]
        for word, count in top_tf_words:
            print(f"{word}: {count}")


# Główna funkcja
def most_popular_words(stopwords, stopWordsOn):
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

    # Wyświetlenie top 10 słów dla każdej reprezentacji
    display_top_words(department_texts, stopwords, stopWordsOn)


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

    # Uruchomienie analizy i porównania
    most_popular_words(stopwords, stopWordsOn)
