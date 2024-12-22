from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route('/grocery_list.json')
def serve_json():
    return jsonify({
        "items": [
            {"name": "Milk", "specification": "1L"},
            {"name": "Bread", "specification": "Baguette"},
            {"name": "Apples", "specification": "6 pieces"}
        ]
    })

@app.route('/inventory.json')
def inventory():
    df = pd.read_excel('C:\grocery_inventory\inventaire.xlsx')
    return df

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)