from flask import Flask, request, jsonify
import re
import bcrypt
from pymongo import MongoClient
from bson import ObjectId

print("Testando conexão...")

def connect():
    try:
        client = MongoClient(
            "mongodb+srv://jp3066984:JPWzGwwdjExEUcdC@cadastros.5u5nn.mongodb.net/?retryWrites=true&w=majority&appName=cadastros&tls=true"
        )
        db = client['cadastros']
        colecao = db["users"]

        # Testando conexão
        print("Conexão com MongoDB estabelecida com sucesso.")
        return db  # Retorna a conexão
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None  # Retorna None em caso de erro na conexão

# Função para converter ObjectId em string
def str_id(id):
    return str(id)

app = Flask(__name__)

@app.route("/users/register", methods=["POST"])
def register_users():
    # Enviando dados via JSON
    data = request.get_json()
    nome = data.get("nome")
    email = data.get("email")
    senha = data.get("senha")

    # Validação dos campos obrigatórios
    if not nome:
        return jsonify({"error": "O campo nome é obrigatório"}), 400
    if not email:
        return jsonify({"error": "O campo email é obrigatório"}), 400
    if not senha:
        return jsonify({"error": "O campo senha é obrigatório"}), 400
    if len(senha) < 6:
        return jsonify({"error": "A senha deve ter pelo menos 6 caracteres"}), 400

    # Expressão regular para validar e-mails
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(email_regex, email):
        return jsonify({"error": "O email fornecido é inválido"}), 400

    # Conectar ao banco de dados
    db = connect()  # Usando a função connect() diretamente
    if db is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    users_collection = db["users"]

    # Verificar se o email já existe no banco de dados
    if users_collection.find_one({"email": email}):
        return jsonify({"error": "O email fornecido já está registrado"}), 400

    # Gerar um hash seguro para a senha
    hashed_senha = bcrypt.hashpw(senha.encode("utf-8"), bcrypt.gensalt())

    # Criar objeto do usuário para retorno
    usuario = {
        "nome": nome,
        "email": email,
        "senha": hashed_senha.decode("utf-8")  # Armazena a senha como string
    }

    # Inserir o novo usuário no banco de dados
    result = users_collection.insert_one(usuario)

    # Verificando se a inserção foi bem-sucedida
    if result.inserted_id:
        print(f"Usuário inserido com o id: {result.inserted_id}")
    else:
        return jsonify({"error": "Erro ao inserir o usuário no banco de dados"}), 500

    # Excluindo a senha da resposta antes de retornar
    usuario.pop("senha")
    usuario["_id"] = str_id(result.inserted_id)  # Convertendo ObjectId para string

    return jsonify({
        "message": "Usuário registrado com sucesso!",
        "user": usuario  # Retorna os dados do usuário (sem a senha)
    }), 201

@app.route("/users", methods=["GET"])
def get_users():
    try:
        # Conectar ao banco de dados
        db = connect()  # Usando a função connect() diretamente
        if db is None:
            return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500
        
        users_collection = db["users"]

        # Buscar todos os usuários no banco, incluindo o id
        users = list(users_collection.find({}, {"_id": 1, "email": 1}))  # Retorna id e e-mail

        # Convertendo ObjectId para string para a resposta
        for user in users:
            user["_id"] = str_id(user["_id"])

        return jsonify({"users": users}), 200

    except Exception as e:
        return jsonify({"error": f"Erro ao buscar usuários: {str(e)}"}), 500
    
@app.route("/users/update_password", methods=["PUT"])
def update_password():
    data = request.get_json()
    email = data.get("email")
    nova_senha = data.get("senha")

    if not email:
        return jsonify({"error": "O campo e-mail é obrigatório"}), 400
    
    if not nova_senha:
        return jsonify({"error": "O campo senha é obrigatório"}), 400
    
    if len(nova_senha) < 6:
        return jsonify({"error": "A senha deve ter pelo menos 6 caracteres"}), 400

    db = connect()
    
    if db is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    users_collection = db["users"]
    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "E-mail não encontrado"}), 404

    hashed_senha = bcrypt.hashpw(nova_senha.encode("utf-8"), bcrypt.gensalt())

    result = users_collection.update_one(
        {"email": email},
        {"$set": {"senha": hashed_senha.decode("utf-8")}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Não foi possível atualizar a senha"}), 400

    return jsonify({"message": "Senha atualizada com sucesso!"}), 200

@app.route("/users/delete", methods=["DELETE"])
def delete_user():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "O campo e-mail é obrigatório"}), 400

    db = connect()

    if db is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    users_collection = db["users"]
    user = users_collection.find_one({"email": email})

    if not user:
        return jsonify({"error": "E-mail não encontrado"}), 404

    result = users_collection.delete_one({"email": email})

    if result.deleted_count == 0:
        return jsonify({"error": "Não foi possível apagar a conta"}), 500

    return jsonify({"message": "Usuário deletado com sucesso!"}), 200


if __name__ == "__main__":
    connect()  # Testa a conexão quando iniciar o app
    app.run(debug=True)  # Inicia o servidor Flask