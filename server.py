from flask import Flask, request, render_template, jsonify
import pandas as pd

app = Flask(__name__)


@app.route('/select_week', methods=['GET', 'POST'])
def select_week():
    if request.method == 'POST':
        # Récupérer la semaine depuis le formulaire
        week = request.form.get('week', type=int)
        return grocery_list_json(week)
    # Afficher le formulaire HTML
    return render_template('select_week.html')

def grocery_list_json(week):
    # Charger les fichiers Excel
    inventory = pd.read_excel('C:\\github_repo\\automated_grocery_list\\grocery\\inventaire.xlsx')
    recettes = pd.read_excel('C:\\github_repo\\automated_grocery_list\\grocery\\recettes.xlsx')

    # Filtrer les recettes pour la semaine sélectionnée
    recette_week_selected = recettes[recettes['Semaine'] == week]

    if recette_week_selected.empty:
        return jsonify({"message": f"Aucune recette trouvée pour la semaine {week}"}), 404

    # Extraire et dédupliquer les ingrédients
    all_ingredients = []
    for ingredients in recette_week_selected['Ingrédients'].dropna():
        splitted_ingredients = [item.strip() for item in ingredients.split(", ")]
        for ingredient in splitted_ingredients:
            if ingredient not in all_ingredients:
                all_ingredients.append(ingredient)
                
    # Vérifier l'inventaire et ajouter les articles non en stock et wanted/recurring
    shopping_list = []
    for ingredient in all_ingredients:
        # Vérifier si l'article est dans l'inventaire
        item_row = inventory[inventory['Item'] == ingredient]
        
        if not item_row.empty:
            # Si l'article n'est pas en stock et est voulu (Wanted) ou récurrent (Recurring), on l'ajoute
            in_stock = item_row['In stock'].values[0]
            wanted = item_row['Wanted'].values[0]
            recurring = item_row['Recurring'].values[0]
            
            if in_stock == "No" and (wanted == "Yes" or recurring == "Yes"):
                shopping_list.append(ingredient)

    # Add recurring items to the shopping list if not already included
    for index, row in inventory.iterrows():
        if row['Recurring'] == "Yes" and row['In stock'] == "No":
            item = row['Item']
            if item not in shopping_list:
                shopping_list.append(item)



    # Générer une page HTML avec les ingrédients
    return jsonify({"Liste": shopping_list})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)