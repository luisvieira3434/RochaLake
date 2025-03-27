from flask import Flask, jsonify
import json
import os

app = Flask(__name__)  # ESSENCIAL estar com esse nome

# Caminho correto
DATA_FILE = os.path.join(os.path.dirname(__file__), 'data.json')

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

@app.route('/')
def home():
    return jsonify({"message": "API rodando. Acesse /api/oportunidades"})

@app.route('/api/oportunidades', methods=['GET'])
def get_oportunidades():
    return jsonify(load_data())

@app.route('/api/oportunidades/<int:id>', methods=['GET'])
def get_oportunidade(id):
    dados = load_data()
    oportunidade = next((item for item in dados if item["id"] == id), None)
    if oportunidade:
        return jsonify(oportunidade)
    return jsonify({"error": "Oportunidade não encontrada"}), 404
