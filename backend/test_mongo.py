from pymongo import MongoClient

# Conectar ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["test_db"]

# Testar conexão listando coleções
print("Conectado ao MongoDB:", db.list_collection_names())
