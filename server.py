from flask import Flask, request, render_template, redirect
import pandas as pd
import json

def get_data():
    # Charger les données depuis un fichier Excel
    file_path = 'grocery//grocery.xlsx'

    inventory = pd.read_excel(file_path, sheet_name='inventory')
    recipes = pd.read_excel(file_path, sheet_name='recipes')

    return inventory, recipes

app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/select_week')

@app.route('/select_week', methods=['GET'])
def select_week():
    return render_template('select_week.html')

@app.route('/ingredients', methods=['GET'])
def bring_list():
    week = request.args.get('week', type=int)
    if not week:
        return redirect('/select_week')  # Redirection si la semaine n'est pas définie

    shopping_list = generate_shopping_list(week)

    # Générer JSON-LD
    json_ld = {
        "@context": "https://schema.org",
        "@type": "Recipe",
        "name": f"Liste d'épicerie pour la semaine {week}",
        "author": {
            "@type": "Person",
            "name": "Xavier Painchaud"
        },
        "description": "Une application pour générer automatiquement une liste d'épicerie hebdomadaire.",
        "image": "https://static.vecteezy.com/ti/vecteur-libre/p2/2056660-panier-et-une-liste-de-produits-vectoriel.jpg",
        "recipeIngredient": shopping_list
    }

    return render_template('index.html', shopping_list=shopping_list, week=week, json_ld=json.dumps(json_ld))

def generate_shopping_list(week):
    try:
        inventory, recipes = get_data()

        # Filtrer les recettes pour la semaine sélectionnée
        selected_recipes = recipes[recipes['Semaine'] == week]

        if selected_recipes.empty:
            return None    

        # Extract and deduplicate ingredients
        all_ingredients = set()
        for ingredients in selected_recipes['Ingrédients'].dropna():
            for ingredient in ingredients.split(", "):
                all_ingredients.add(ingredient.strip())

        # Check inventory and add items to the shopping list
        shopping_list = []
        for ingredient in all_ingredients:
            item_row = inventory[inventory['Item'] == ingredient]
            if not item_row.empty:
                in_stock = item_row['In stock'].values[0]
                if in_stock == "No":
                    shopping_list.append(ingredient)

        # Add recurring items to the shopping list
        for _, row in inventory.iterrows():
            if row['Recurring'] == "Yes" and row['In stock'] == "No":
                item = row['Item']
                if item not in shopping_list:
                    shopping_list.append(item)

        return shopping_list

    except Exception as e:
        return {"message": f"Erreur dans la génération de la liste d'épicerie: {str(e)}"}, 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
