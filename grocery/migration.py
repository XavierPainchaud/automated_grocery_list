import pandas as pd
import sqlite3

# Charger les fichiers Excel
inventory = pd.read_excel('inventaire.xlsx')
recipes = pd.read_excel('recettes.xlsx')

# Créer une connexion SQLite
conn = sqlite3.connect('grocery.db')

# Sauvegarder les données dans SQLite
inventory.to_sql('inventory', conn, if_exists='replace', index=False)
recipes.to_sql('recipes', conn, if_exists='replace', index=False)

# Fermer la connexion
conn.close()