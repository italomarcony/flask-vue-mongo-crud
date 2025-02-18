from dataclasses import dataclass
from typing import List
from pymongo import MongoClient
import time
import json

# Definindo as dataclasses
@dataclass
class UserPreferences:
    timezone: str
    
    # Método para converter UserPreferences em um dicionário
    def to_dict(self):
        return {
            "timezone": self.timezone
        }

@dataclass
class User:
    username: str
    password: str
    roles: List[str]
    preferences: UserPreferences
    created_ts: float
    active: bool = True

    # Método para converter User em um dicionário
    def to_dict(self):
        return {
            "username": self.username,
            "password": self.password,
            "roles": self.roles,
            "preferences": self.preferences.to_dict(),  # Convertendo preferences para dict
            "created_ts": self.created_ts,
            "active": self.active
        }

# Função para carregar o JSON e inserir no MongoDB
def load_data_to_mongo():
    # Carregando o arquivo JSON
    with open('udata.json', 'r') as file:
        data = json.load(file)

    # Acessando a lista de usuários
    users_data = data.get("users", [])

    # Conectando ao MongoDB
    client = MongoClient('mongodb://localhost:27017/')
    db = client['your_database']
    collection = db['users']

    # Contagem de documentos antes da inserção
    initial_count = collection.count_documents({})
    print(f"Contagem inicial de documentos: {initial_count}")
    
    for user_data in users_data:
        user = parse_user_data(user_data)
        if user is None:
            continue  # Pular o usuário se ocorrer erro de parsing
        
        # Inserir no MongoDB (como um dicionário)
        collection.insert_one(user.to_dict())
        print(f"Usuário {user.username} inserido com sucesso.")

    # Contagem de documentos após a inserção
    final_count = collection.count_documents({})
    print(f"Contagem final de documentos: {final_count}")
    print(f"Documentos inseridos: {final_count - initial_count}")

# Função para converter os dados do JSON para o formato da dataclass
def parse_user_data(user_data):
    # Verificando se os dados necessários estão presentes
    if not isinstance(user_data, dict):
        print(f"Erro: Esperado dicionário, mas encontrado: {type(user_data)}")
        print(user_data)  # Imprimir o conteúdo do user_data
        return None

    roles = []
    
    # Mapeamento dos campos 'is_user_*' para 'roles'
    if user_data.get("is_user_admin"):
        roles.append("admin")
    if user_data.get("is_user_manager"):
        roles.append("manager")
    if user_data.get("is_user_tester"):
        roles.append("tester")

    preferences = UserPreferences(timezone=user_data.get("user_timezone", "UTC"))
    
    # Criando o objeto User
    user = User(
        username=user_data["user"],
        password=user_data["password"],
        roles=roles,
        preferences=preferences,
        created_ts=time.mktime(time.strptime(user_data["created_at"], "%Y-%m-%dT%H:%M:%SZ")),  # Convertendo para timestamp
        active=user_data.get("is_user_active", True),
    )

    return user

# Rodando a função para carregar os dados
load_data_to_mongo()
