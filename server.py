from flask import Flask
import pandas as pd

app = Flask(__name__)

@app.route('/inventory.json')
def inventory_json():
    pass
    '''
    # Read data from the Excel file
    data = pd.read_excel('C:\grocery\inventaire.xlsx')

    # Convert the data to JSON
    data_json = data.to_dict(orient='records')
    return data_json
    '''
@app.route('/grocery_list.json')
def grocery_list_json():
    inventory = pd.read_excel('C:\\github_repo\\automated_grocery_list\\grocery\\inventaire.xlsx')

    recettes = pd.read_excel('C:\\github_repo\\automated_grocery_list\\grocery\\recettes.xlsx')

    ingredients = recettes['Ingrédients']
    
    recettes_json = recettes.to_dict(orient='records')

    return recettes_json
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)