from modules.Document import WikipediaDocument, NewsDocument
from modules.Corpus import Corpus
from modules.apis import WikipediaAPI
from modules.apis import NewsAPI
from modules.SearchEngine import SearchEngine
from tqdm import tqdm
import sys
sys.stdout.reconfigure(encoding='utf-8')

# Initialiser les APIs
wiki = WikipediaAPI(user_agent='MyResearchApp/1.0 (contact: yasminemaddouri25@gmail.com)')
news_api = NewsAPI(api_key="69762aec07a640c6bc0ac63e60313737")

# Récupérer les articles
wiki_articles = wiki.get_articles("Intelligence artificielle", max_articles=200)
news_articles = news_api.get_articles("coronavirus", max_articles=100)

# Créer un corpus
corpus = Corpus("AI Articles")


# Ajouter les articles Wikipedia
for idx, article in enumerate(wiki_articles):
    corpus.add_document(WikipediaDocument(
        doc_id=article['id'],
        title=article['title'],
        text=article['text'],
        author=article['author'],
        date=article['date'],
        url=article['url'],
        source=article['source'],
        section_name=f"Section {idx + 1}"  # Nom de section fictif
    ))

# Ajouter les articles NewsAPI
for article in news_articles:
    corpus.add_document(NewsDocument(
        doc_id=article['id'],
        title=article['title'],
        text=article['text'],
        author=article['author'],
        date=article['date'],
        url=article['url'],
        source=article['source'],
        source_name="NewsAPI"  # Nom de la source
    ))

# Convertir les documents en DataFrame
df = corpus.to_dataframe()

# Afficher le DataFrame
print(df)

# Sauvegarder le DataFrame dans un fichier CSV
corpus.save_to_csv("data/corpus.csv")

# Charger le corpus pour vérification
new_corpus = Corpus("Loaded Corpus")
new_corpus.load_from_csv("data/corpus.csv")
print(f"Nombre de documents chargés : {len(new_corpus.documents)}")

#taille du corpus
print(f"Taille du corpus : {corpus.size()} documents")

# Calculer le nombre de mots et de phrases dans le premier document
for doc in corpus.documents:
    print(f"Document {doc.doc_id}: {doc.word_count()} mots, {doc.sentence_count()} phrases")

# Filtrer les documents courts
corpus.filter_short_documents()
print(f"Corpus après filtrage : {corpus.size()} documents")

# Concaténer les textes de tous les documents
all_texts = corpus.concatenate_texts()
print(f"Nombre total de mots dans le corpus : {len(all_texts.split())}") 

# Nettoyer le texte
corpus.nettoyer_texte()

frequencies = corpus.calculer_frequences()
print("Fréquences des mots dans le corpus :")
print(dict(list(frequencies.items())[:20]))  # Afficher les 20 mots les plus fréquents


# Construire le vocabulaire
vocabulaire = corpus.construire_vocabulaire()
print("Taille du vocabulaire :", len(vocabulaire))

# Recherche par mot-clé
results = corpus.search("intelligence")
print(results)


# Construire et afficher la matrice TF-IDF
tfidf_matrix = corpus.construire_matrice_TFIDF()
print("Matrice TF-IDF : ")
print(tfidf_matrix.head())

# recherche avec contexte
df_concorde = corpus.concorde("coronavirus", context_size=50)
print("\nConcordances pour le mot 'corona' :")
print(df_concorde.head())


# Moteur de recherche
search_engine = SearchEngine(corpus)

print("\n=== Moteur de recherche interactif sur le corpus ===\n")
while True:
    query = input("Entrez un mot-clé ou une phrase à rechercher (ou 'exit' pour quitter) : ").strip()
    
    if query.lower() == "exit":
        print("Fin de la session de recherche.")
        break

    print("\nLancement de la recherche...\n")
    
    # Recherche 
    query_results = search_engine.search(query, top_n=10, min_score=0.1)

    if query_results.empty:
        print(f"Aucun document trouvé pour la requête : '{query}'.\n")
    else:
        print(f"\nRésultats pour la requête : '{query}'")
        print(query_results[['id', 'title', 'score']].to_string(index=False))
    print("\n-----------------------------\n")

print("Programme terminé.")
