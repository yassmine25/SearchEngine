import pandas as pd
from modules.Document import Document, WikipediaDocument, NewsDocument
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