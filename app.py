from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)
PEDIDOS_DIR = "pedidos"
os.makedirs(PEDIDOS_DIR, exist_ok=True)

@app.route('/')
def home():
    return jsonify({"status": "Servidor da Ponte Lia ativo."})

@app.route('/receber', methods=['POST'])
def receber():
    dados = request.get_json()
    if not dados:
        return jsonify({"erro": "JSON inválido"}), 400
    pedido_id = dados.get("id", "pedido_sem_id")
    caminho = os.path.join(PEDIDOS_DIR, f"{pedido_id}.json")
    with open(caminho, "w") as f:
        json.dump(dados, f)
    return jsonify({"status": "Pedido recebido com sucesso."})

@app.route('/pingar', methods=['GET'])
def pingar():
    pedidos = os.listdir(PEDIDOS_DIR)
    return jsonify({"pedidos": pedidos})

@app.route('/pedidos/<ficheiro>', methods=['GET'])
def ficheiro_individual(ficheiro):
    caminho = os.path.join(PEDIDOS_DIR, ficheiro)
    if not os.path.exists(caminho):
        return jsonify({"erro": "Ficheiro não encontrado"}), 404
    with open(caminho, "r") as f:
        conteudo = f.read()
    return conteudo

@app.route('/pedidos/<ficheiro>', methods=['PUT'])
def receber_ficheiro(ficheiro):
    caminho = os.path.join(PEDIDOS_DIR, ficheiro)
    os.makedirs(PEDIDOS_DIR, exist_ok=True)
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(request.data.decode("utf-8"))
    return jsonify({"mensagem": "Ficheiro recebido com sucesso!"}), 200

@app.route("/remover/<nome>", methods=["DELETE"])
def remover_pedido(nome):
    caminho = os.path.join(PEDIDOS_DIR, nome)
    if os.path.exists(caminho):
        os.remove(caminho)
        return jsonify({"mensagem": f"{nome} apagado com sucesso."}), 200
    else:
        return jsonify({"erro": "Ficheiro não encontrado."}), 404
