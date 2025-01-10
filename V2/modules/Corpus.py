import pandas as pd
from modules.Document import Document , WikipediaDocument, NewsDocument
import re
from sklearn.feature_extraction.text import TfidfVectorizer

class Corpus:
    def __init__(self, name):
        self.name = name
        self.documents = []

    def add_document(self, document):
        self.documents.append(document)

    def to_dataframe(self):
        data = []
        for doc in self.documents:
            base_data = {
                'id': doc.doc_id,
                'title': doc.title,
                'text': doc.text,
                'author': doc.author,
                'date': doc.date,
                'url': doc.url,
                'source': doc.source
            }
            if isinstance(doc, WikipediaDocument):
                base_data['section_name'] = doc.section_name  # Ajout pour Wikipedia
                base_data['source_name'] = None  # Pas pertinent pour Wikipedia
            elif isinstance(doc, NewsDocument):
                base_data['section_name'] = None  # Pas pertinent pour NewsAPI
                base_data['source_name'] = doc.source_name  # Ajout pour NewsAPI
            else:
                base_data['section_name'] = None
                base_data['source_name'] = None

            data.append(base_data)

        return pd.DataFrame(data)

    
    def save_to_csv(self, file_path):
       df = self.to_dataframe()
       df.to_csv(file_path, sep='\t', index=False)
    

    from modules.Document import Document, WikipediaDocument, NewsDocument

    def load_from_csv(self, file_path):
        df = pd.read_csv(file_path, sep='\t')
        for _, row in df.iterrows():
            if row['source'] == 'wikipedia':
                self.add_document(WikipediaDocument(
                    doc_id=row['id'], title=row['title'], text=row['text'],
                    author=row['author'], date=row['date'], url=row['url'],
                    source=row['source'], section_name="Unknown Section"
                ))
            elif row['source'] == 'newsapi':
                self.add_document(NewsDocument(
                    doc_id=row['id'], title=row['title'], text=row['text'],
                    author=row['author'], date=row['date'], url=row['url'],
                    source=row['source'], source_name="NewsAPI"
                ))
            else:
                self.add_document(Document(
                    doc_id=row['id'], title=row['title'], text=row['text'],
                    author=row['author'], date=row['date'], url=row['url'],
                    source=row['source']
                ))


    def size(self):
        return len(self.documents)

    def filter_short_documents(self, min_length=20):
        self.documents = [doc for doc in self.documents if len(doc.text) >= min_length]
    

    def concatenate_texts(self):
        return ' '.join([doc.text for doc in self.documents])
    
    def search(self, keyword):
        results = []
        for doc in self.documents:
            matches = re.finditer(keyword, doc.text, re.IGNORECASE)
            for match in matches:
                context = doc.text[max(0, match.start()-30):match.end()+30]
                results.append({
                    'doc_id': doc.doc_id,
                    'context': context
                })
        return results
    
    def concorde(self, keyword, context_size=30):
        
        results = []
        for doc in self.documents:
            matches = re.finditer(keyword, doc.text, re.IGNORECASE)
            for match in matches:
                left_context = doc.text[max(0, match.start()-context_size):match.start()]
                right_context = doc.text[match.end():match.end()+context_size]
                results.append({
                    'doc_id': doc.doc_id,
                    'left_context': left_context,
                    'match': match.group(),
                    'right_context': right_context
                })
        return pd.DataFrame(results)
    
    def nettoyer_texte(self):
        
        for doc in self.documents:
            doc.text = re.sub(r'[^\w\s]', '', doc.text.lower())  # Supprimer la ponctuation et mettre en minuscule

    def construire_vocabulaire(self):
        vocabulaire = set()
        for doc in self.documents:
            vocabulaire.update(doc.text.split())
        return sorted(vocabulaire)
    
    def calculer_frequences(self):
        from collections import Counter
        frequencies = Counter()
        for doc in self.documents:
            frequencies.update(doc.text.split())
        return frequencies
    
    def construire_matrice_TF(self):
        vocab = self.construire_vocabulaire()
        matrix = []
        for doc in self.documents:
            row = [doc.text.split().count(word) for word in vocab]
            matrix.append(row)
        return pd.DataFrame(matrix, columns=vocab, index=[doc.doc_id for doc in self.documents])


    def construire_matrice_TFIDF(self):
        texts = [doc.text for doc in self.documents]
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(texts)
        return pd.DataFrame(tfidf_matrix.toarray(), columns=vectorizer.get_feature_names_out(), index=[doc.doc_id for doc in self.documents])
