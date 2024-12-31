from flask import Flask, request, render_template, jsonify
import pandas as pd
import sqlite3

# Connexion à SQLite
def get_data():
    conn = sqlite3.connect('grocery.db')

    # Charger les données
    inventory = pd.read_sql_query("SELECT * FROM inventory", conn)
    recipes = pd.read_sql_query("SELECT * FROM recipes", conn)

    conn.close()
    return inventory, recipes

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def bring_list():
    if request.method == 'POST':
        week = request.form.get('week', type=int)

        if not week:
            return jsonify({"message": "Semaine non valide."}), 400

        shopping_list = generate_shopping_list(week)

        if not shopping_list:
            return render_template('index.html', shopping_list=[], week=week)

        return render_template('index.html', shopping_list=shopping_list, week=week)

    # Affiche uniquement le formulaire si aucune semaine n'est sélectionnée
    return render_template('index.html', shopping_list=None)


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
                wanted = item_row['Wanted'].values[0]
                recurring = item_row['Recurring'].values[0]
                if in_stock == "No" and (wanted == "Yes" or recurring == "Yes"):
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
