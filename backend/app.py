from flask import Flask, jsonify, request
from flask_pymongo import PyMongo
from flask_cors import CORS
from bson import ObjectId

app = Flask(__name__)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Configuração do MongoDB
app.config["MONGO_URI"] = "mongodb://localhost:27017/your_database"
mongo = PyMongo(app)

@app.route('/')
def home():
    return "Flask is working!"

# Endpoint para obter os usuários
@app.route('/users', methods=['GET'])
def get_users():
    users_collection = mongo.db.users
    users = list(users_collection.find())
    # Remover o campo _id de cada usuário, se necessário
    for user in users:
        user['_id'] = str(user['_id'])  # Convertendo ObjectId para string
    return jsonify(users)

# Endpoint para adicionar um novo usuário
@app.route('/users', methods=['POST'])
def add_user():
    data = request.json
    users_collection = mongo.db.users

    # Verificar se o username já existe
    if users_collection.find_one({"username": data.get("username")}):
        return jsonify({"message": "Username already exists"}), 400

    result = users_collection.insert_one(data)
    return jsonify({"message": "User added", "id": str(result.inserted_id)}), 201

# Endpoint para buscar um usuário por username
@app.route('/users/<username>', methods=['GET'])
def get_user(username):
    users_collection = mongo.db.users
    user = users_collection.find_one({"username": username})
    
    if user:
        user['_id'] = str(user['_id'])  # Convertendo ObjectId para string
        return jsonify(user)
    else:
        return jsonify({"message": "User not found."}), 404

# Endpoint para atualizar um usuário
@app.route('/users/<username>', methods=['PUT'])
def update_user(username):
    data = request.json
    users_collection = mongo.db.users
    
    # Procurar pelo usuário no banco
    user = users_collection.find_one({"username": username})
    
    if user:
        # Atualizar os campos do usuário
        updated_user = {}
        if "password" in data:
            updated_user["password"] = data["password"]
        if "roles" in data:
            updated_user["roles"] = data["roles"]
        if "preferences" in data:
            updated_user["preferences"] = data["preferences"]
        if "active" in data:
            updated_user["active"] = data["active"]
        
        # Atualizar no MongoDB
        users_collection.update_one({"username": username}, {"$set": updated_user})
        
        return jsonify({"message": f"User {username} updated successfully."}), 200
    else:
        return jsonify({"message": "User not found."}), 404

# Endpoint para deletar um usuário
@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    users_collection = mongo.db.users
    
    # Procurar o usuário
    user = users_collection.find_one({"username": username})
    
    if user:
        # Deletar o usuário
        users_collection.delete_one({"username": username})
        return jsonify({"message": f"User {username} deleted successfully."}), 200
    else:
        return jsonify({"message": "User not found."}), 404

if __name__ == '__main__':
    app.run(debug=True)
