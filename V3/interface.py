import tkinter as tk
from tkinter import ttk, messagebox
from modules.SearchEngine import SearchEngine
from modules.Corpus import Corpus
import pandas as pd
from tkinter import filedialog

# Initialiser le corpus et le moteur de recherche
corpus = Corpus("AI Articles")
corpus.load_from_csv("data/corpus.csv")
search_engine = SearchEngine(corpus)

# fonction pour exécuter la recherche
def execute_search():
    query = search_entry.get().strip()  # Récupérer le texte entré par l'utilisateur et supprimer les espaces inutiles

    # Vérifier si le champ de recherche est vide
    if not query:
        messagebox.showwarning("Recherche vide", "Veuillez entrer un mot-clé pour effectuer une recherche.")
        return  # Stoppe l'exécution si la barre de recherche est vide

    num_articles = int(article_count_scale.get())  # Récupérer le nombre d'articles sélectionné
    results = search_engine.search(query, top_n=num_articles, min_score=0.1)  # Effectuer la recherche

    # Effacer les anciens résultats
    for row in result_tree.get_children():
        result_tree.delete(row)

    # Ajouter les nouveaux résultats
    for _, row in results.iterrows():
        score = row['score']  # Score TF-IDF du document
        result_tree.insert("", "end", values=(row['id'], row['title'], row['text'], row['source'], round(score, 4)))


# Créer une fonction pour exporter les résultats
def export_results():
    query = search_entry.get().strip()
    if not query:
        tk.messagebox.showwarning("Exportation", "Veuillez effectuer une recherche avant d'exporter.")
        return
    
    # Extraire les résultats actuels du tableau
    data = []
    for row_id in result_tree.get_children():
        values = result_tree.item(row_id)["values"]
        data.append({
            "ID": values[0],
            "Titre": values[1],
            "Extrait": values[2],
            "Source": values[3]
        })

    if not data:
        tk.messagebox.showinfo("Exportation", "Aucun résultat à exporter.")
        return

    df = pd.DataFrame(data)
    filepath = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if filepath:
        df.to_csv(filepath, index=False, encoding='utf-8')
        tk.messagebox.showinfo("Exportation", "Les résultats ont été exportés avec succès.")

# Créer la fenêtre principale
root = tk.Tk()
root.title("Moteur de Recherche")

# Ajouter une boîte de recherche
search_label = tk.Label(root, text="Entrez votre requête :")
search_label.pack(pady=5)

search_entry = tk.Entry(root, width=50)
search_entry.pack(pady=5)

# Ajouter un widget Scale pour choisir le nombre d'articles
article_count_label = tk.Label(root, text="Nombre d'articles à extraire :")
article_count_label.pack(pady=5)

article_count_scale = tk.Scale(root, from_=1, to=100, orient="horizontal", length=300)  # Défaut : 1 à 100 articles
article_count_scale.set(20)  # Valeur par défaut
article_count_scale.pack(pady=5)

search_button = tk.Button(root, text="Rechercher", command=execute_search)
search_button.pack(pady=10)

export_button = tk.Button(root, text="Exporter les résultats", command=export_results)
export_button.pack(pady=5)

# Ajouter une table pour afficher les résultats
columns = ("ID", "Titre", "Extrait", "Source", "Score")
result_tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    result_tree.heading(col, text=col)
    result_tree.column(col, width=150)
result_tree.pack(pady=10, fill="both", expand=True)
# Fonction pour afficher le texte complet de l'article
def show_full_text(event):
    selected_item = result_tree.selection()
    if selected_item:
        item = result_tree.item(selected_item[0])  # Obtenir la ligne sélectionnée
        doc_id = item["values"][0]  # Récupérer l'ID du document
        title = item["values"][1]  # Titre
        text = item["values"][2]  # Extrait complet du document
        source = item["values"][3]  # Source
        
        # Créer une nouvelle fenêtre
        full_text_window = tk.Toplevel(root)
        full_text_window.title(f"Article - {title}")
        full_text_window.geometry("600x400")

        # Ajouter un widget Text pour afficher le contenu complet
        text_widget = tk.Text(full_text_window, wrap="word")
        text_widget.insert("1.0", f"ID : {doc_id}\nTitre : {title}\nSource : {source}\n\n{text}")
        text_widget.configure(state="disabled")  # Rendre le texte non éditable
        text_widget.pack(expand=True, fill="both")

        # Ajouter une barre de défilement
        scrollbar = tk.Scrollbar(full_text_window, command=text_widget.yview)
        text_widget.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

# Associer la fonction à l'événement de sélection dans le Treeview
result_tree.bind("<<TreeviewSelect>>", show_full_text)

# Lancer la boucle principale de Tkinter
root.mainloop()
