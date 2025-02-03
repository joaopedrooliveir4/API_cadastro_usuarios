#  API de Gerenciamento de Usuários

## Descrição

Esta API permite o cadastro, atualização de senha e remoção de usuários. O banco de dados utilizado é o MongoDB, e a API foi desenvolvida utilizando Flask.

## Tecnologias Utilizadas

- Python
- Flask
- MongoDB
- bcrypt

## Endpoints

### 1. Registro de Usuário

**Rota:** `POST /users/register`

**Corpo da Requisição (JSON):**

```json
{
    "nome": "Nome do Usuário",
    "email": "usuario@email.com",
    "senha": "senha123"
}
```

**Respostas:**

- `201 Created` - Usuário registrado com sucesso.
- `400 Bad Request` - Erro na validação dos dados.
- `500 Internal Server Error` - Erro ao conectar ao banco.

### 2. Atualização de Senha

**Rota:** `PUT /users/update-password`

**Corpo da Requisição (JSON):**

```json
{
    "email": "usuario@email.com",
    "nova_senha": "novasenha123"
}
```

**Respostas:**

- `200 OK` - Senha atualizada com sucesso.
- `404 Not Found` - E-mail não encontrado.
- `500 Internal Server Error` - Erro ao atualizar a senha.

### 3. Exclusão de usuário

**Rota:** `DELETE /users/delete`

**Corpo da Requisição (JSON):**

```json
{
    "email": "usuario@email.com"
}
```

**Respostas:**

- `200 OK` - Usuário deletado com sucesso.
- `404 Not Found` - E-mail não encontrado.
- `500 Internal Server Error` - Erro ao excluir conta.

## Como Executar

1. Instale as dependências:
   ```bash
   pip install flask pymongo bcrypt
   ```
2. Execute o servidor:
   ```bash
   python app.py
   ```
3. A API estará disponível em `http://127.0.0.1:5000/`.

## Observações

- Utilize um ambiente virtual para organizar as dependências.
- Certifique-se de configurar corretamente a conexão com o MongoDB.

## Autor

Desenvolvido por João Pedro Oliveira.
