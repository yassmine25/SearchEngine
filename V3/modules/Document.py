# Ce module contient la classe Document qui est une classe abstraite pour représenter un document textuel.
class Document:
    def __init__(self, doc_id,title, text,author, date, url,source):
        self.doc_id = doc_id
        self.title = title
        self.text = text
        self.author = author
        self.date = date
        self.url = url
        self.source = source
   # Méthode pour afficher les informations du document
    def __str__(self):
        return f"Document[{self.doc_id}] - Title: {self.title}, Source: {self.source} "
    # Méthode pour compter le nombre de mots dans le texte
    def word_count(self):
        return len(self.text.split())  # compter le nombre des mots qui sont séparés par des espaces
  # Méthode pour compter le nombre de phrases dans le texte
    def sentence_count(self):
        return len(self.text.split('.'))  # compter le nombre des phrases qui sont séparées par des points


# Héritage de Document pour Wikipedia
class WikipediaDocument(Document):
    def __init__(self, doc_id, title, text, author, date, url, source, section_name):
        super().__init__(doc_id, title, text, author, date, url, source)
        self.section_name = section_name  # Attribut spécifique aux articles Wikipedia
# Méthode pour afficher les informations du document Wikipedia
    def __str__(self):
        return f"WikipediaDocument[{self.doc_id}] - Title: {self.title}, Section: {self.section_name}, Source: {self.source}"


# Héritage de Document pour News
class NewsDocument(Document):
    def __init__(self, doc_id, title, text, author, date, url, source, source_name):
        super().__init__(doc_id, title, text, author, date, url, source)
        self.source_name = source_name  # Nom de la source du news ("CNN", "Le Monde")
# Méthode pour afficher les informations du document News
    def __str__(self):
        return f"NewsDocument[{self.doc_id}] - Title: {self.title}, Source Name: {self.source_name}, Source: {self.source}"
