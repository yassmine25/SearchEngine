import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Classe pour représenter un moteur de recherche
class SearchEngine:
    def __init__(self, corpus):
        self.corpus = corpus
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = self.vectorizer.fit_transform([doc.text for doc in corpus.documents])
# Rechercher des documents dans le corpus
    def search(self, query, top_n=5, min_score=0.2):
        # Transformer la requête avec le même vectorizer
        query_vector = self.vectorizer.transform([query])
        
        # Calculer la similarité cosinus
        similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        
        # Trier les scores
        scores = list(enumerate(similarities))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        
        # Filtrer les résultats en fonction du score minimum
        filtered_scores = [(idx,score) for idx, score in sorted_scores if score >= min_score]

        filtered_scores = filtered_scores[:top_n]
        # Construire les résultats
        results = [{
            "id": self.corpus.documents[idx].doc_id,
            "title": self.corpus.documents[idx].title,
            "text": self.corpus.documents[idx].text,
            "source": self.corpus.documents[idx].source,
            "score": score
        } for idx, score in filtered_scores]
        
        return pd.DataFrame(results)
