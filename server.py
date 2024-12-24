from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/select_week', methods=['GET', 'POST'])
def select_week():
    if request.method == 'POST':
        # Retrieve the selected week from the form
        week = request.form.get('week', type=int)
        
        if not week:
            return jsonify({"message": "Semaine non valide."}), 400
        
        shopping_list = generate_shopping_list(week)

        if not shopping_list:
            return jsonify({"message": f"Aucune recette trouvée pour la semaine {week}"}), 404

        # Render the list for Bring
        return render_template('bring_list.html', shopping_list=shopping_list)
    
    # Render the week selection form
    return render_template('select_week.html')

def generate_shopping_list(week):
    try:
        # Load Excel files
        inventory = pd.read_excel('C:\\github_repo\\automated_grocery_list\\grocery\\inventaire.xlsx')
        recipes = pd.read_excel('C:\\github_repo\\automated_grocery_list\\grocery\\recettes.xlsx')

        # Filter recipes for the selected week
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
