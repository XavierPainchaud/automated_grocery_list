# import json

# # Load your JSON file
# with open('recette.json', 'r') as file:
#     data = json.load(file)

# # Generate Bring! URL
# base_url = "bring://import-shopping-list?items="
# items = [f"{item['name']} ({item['specification']})" for item in data['items']]
# bring_url = base_url + ",".join(items)

# print(f"Use this link to import into Bring!: {bring_url}")
import pandas as pd


inventory = pd.read_excel('C:\\grocery\\inventaire.xlsx')

recettes = pd.read_excel('C:\\grocery\\recettes.xlsx')

ingredients = recettes['Ingrédients']

recettes_json = recettes.to_dict(orient='records')

print(recettes_json)