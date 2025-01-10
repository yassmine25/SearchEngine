import unittest
from modules.Document import WikipediaDocument, NewsDocument
from modules.Corpus import Corpus
from modules.SearchEngine import SearchEngine

# Tests pour les documents
class TestDocument(unittest.TestCase):
    def test_wikipedia_document_creation(self):
        doc = WikipediaDocument(
            doc_id="wiki_1",
            title="IA",
            text="L'intelligence artificielle est fascinante.",
            author="Alan Turing",
            date="2025-01-01",
            url="https://example.com/wiki/ia",
            source="Wikipedia",
            section_name="Introduction"
        )
        self.assertEqual(doc.doc_id, "wiki_1")
        self.assertEqual(doc.section_name, "Introduction")
# Test pour le document News
    def test_news_document_creation(self):
        doc = NewsDocument(
            doc_id="news_1",
            title="Pandémie",
            text="La pandémie a changé le monde.",
            author="Journaliste",
            date="2024-12-01",
            url="https://example.com/news/pandemie",
            source="NewsAPI",
            source_name="Le Monde"
        )
        self.assertEqual(doc.source_name, "Le Monde")
    

# Tests pour le corpus
class TestCorpus(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus("Test Corpus")
        self.doc1 = WikipediaDocument(
            doc_id="wiki_1", title="Test IA", text="Test sur l'intelligence artificielle.",
            author="Auteur 1", date="2023-01-01", url="https://example.com", source="Wikipedia", section_name="Tech"
        )
        self.doc2 = NewsDocument(
            doc_id="news_1", title="News Article", text="Actualités sur le monde de l'IA.",
            author="Auteur 2", date="2023-02-01", url="https://example-news.com", source="NewsAPI", source_name="Reuters"
        )
# Test pour ajouter un document au corpus
    def test_add_document(self):
        self.corpus.add_document(self.doc1)
        self.assertEqual(self.corpus.size(), 1)
# Test pour supprimer un document du corpus
    def test_concordance(self):
        self.corpus.add_document(self.doc1)
        concorde_result = self.corpus.concorde("intelligence", context_size=10)
        self.assertGreater(len(concorde_result), 0)
        self.assertIn("intelligence", concorde_result.iloc[0]["match"].lower())
# Test pour construire la matrice TF-IDF
    def test_tfidf_matrix_creation(self):
        self.corpus.add_document(self.doc1)
        tfidf_matrix = self.corpus.construire_matrice_TFIDF()
        self.assertEqual(tfidf_matrix.shape[0], 1)

# Tests pour le moteur de recherche
class TestSearchEngine(unittest.TestCase):
    def setUp(self):
        self.corpus = Corpus("Search Corpus")
        self.doc1 = WikipediaDocument(
            doc_id="wiki_1", title="Intelligence", text="L'intelligence artificielle change le monde.",
            author="Auteur IA", date="2024-01-01", url="https://example.com", source="Wikipedia", section_name="Tech"
        )
        self.corpus.add_document(self.doc1)
        self.search_engine = SearchEngine(self.corpus)
# Test pour la requête de recherche
    def test_search_query(self):
        results = self.search_engine.search("artificielle", top_n=1)
        self.assertEqual(len(results), 1)
        self.assertIn("artificielle", results.iloc[0]['text'].lower())
# Test pour une recherche vide
    def test_empty_search(self):
        results = self.search_engine.search("inexistant", top_n=1)
        self.assertEqual(len(results), 0)

if __name__ == "__main__":
    unittest.main()
