import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from scipy.sparse import save_npz
import arff


# Funkcja do wczytywania pliku ARFF
def load_arff_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        dataset = arff.load(file)
        data = dataset['data']  # Pobierz dane
        return data


# Funkcja do konwersji danych na DataFrame
def convert_to_dataframe(arff_data):
    # Tworzymy DataFrame z listy danych
    df = pd.DataFrame(arff_data, columns=['document_name', 'document_content'])
    return df


# Funkcja do generowania reprezentacji dokumentu (binary, bow, tf, tf-idf)
def generate_representations(df, output_folder):
    # Stwórz folder na wyniki, jeśli nie istnieje
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Przechodzenie po każdej unikalnej nazwie dokumentu
    for doc_name in df['document_name'].unique():
        # Wyodrębnienie dokumentów o tej samej nazwie
        docs = df[df['document_name'] == doc_name]['document_content'].tolist()

        # Reprezentacja "bag of words" i binarna
        vectorizer_bow = CountVectorizer(binary=False)
        vectorizer_binary = CountVectorizer(binary=True)

        # Reprezentacja TF-IDF
        vectorizer_tfidf = TfidfVectorizer()

        # Bag of Words (BoW)
        X_bow = vectorizer_bow.fit_transform(docs)
        bow_file_path = os.path.join(output_folder, f"{doc_name}_bow.npz")
        save_npz(bow_file_path, X_bow)

        # Reprezentacja binarna
        X_binary = vectorizer_binary.fit_transform(docs)
        binary_file_path = os.path.join(output_folder, f"{doc_name}_binary.npz")
        save_npz(binary_file_path, X_binary)

        # Reprezentacja TF-IDF
        X_tfidf = vectorizer_tfidf.fit_transform(docs)
        tfidf_file_path = os.path.join(output_folder, f"{doc_name}_tfidf.npz")
        save_npz(tfidf_file_path, X_tfidf)

        # Zapis słów użytych w wektorach
        feature_names = vectorizer_bow.get_feature_names_out()
        features_file_path = os.path.join(output_folder, f"{doc_name}_features.txt")
        with open(features_file_path, 'w', encoding='utf-8') as f:
            f.write("\n".join(feature_names))

        print(f"Zapisano pliki dla dokumentu: {doc_name}")


# Główna funkcja
def main():
    # Ścieżka do pliku ARFF
    input_arff_file = "Departments.arff"
    output_folder = "test"

    # Wczytaj plik ARFF
    arff_data = load_arff_file(input_arff_file)

    # Konwertuj dane do DataFrame
    df = convert_to_dataframe(arff_data)

    # Wygeneruj różne reprezentacje dokumentów
    generate_representations(df, output_folder)


# Uruchomienie programu
if __name__ == "__main__":
    main()
