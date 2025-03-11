from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
import json

app = Flask(__name__)
CORS(app)

def load_products():
    try:
        with open('data/products.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {"watches": []}
    except json.JSONDecodeError:
        return {"watches": []}

@app.route('/api/products', methods=['GET'])
def get_products():
    products_data = load_products()
    return jsonify(products_data)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    products_data = load_products()
    product = next((item for item in products_data['watches'] if item['id'] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404

@app.route('/static/images/<path:filename>')
def serve_image(filename):
    return send_from_directory(os.path.join(app.root_path, 'static/images'), filename)

if __name__ == '__main__':
    app.run(debug=True, port=5000)