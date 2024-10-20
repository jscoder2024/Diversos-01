import psycopg2
from cryptography.fernet import Fernet
import os
import string
import random

# Função para conectar ao banco de dados PostgreSQL
def connect_db():
    return psycopg2.connect(
        dbname="admin",
        user="joshe",
        password="eu141521",
        host="localhost"
    )

# Função para gerar uma chave de criptografia
def generate_key():
    return Fernet.generate_key()

# Função para salvar a chave de criptografia em um arquivo
def save_key(key):
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

# Função para carregar a chave de criptografia de um arquivo
def load_key():
    return open("secret.key", "rb").read()

# Verificar se o arquivo de chave existe, se não, gerar uma nova chave
if not os.path.exists("secret.key"):
    key = generate_key()
    save_key(key)
else:
    key = load_key()

# Função para criptografar a senha
def encrypt_password(password):
    cipher_suite = Fernet(key)
    encrypted_bytes = cipher_suite.encrypt(password.encode())
    return encrypted_bytes.decode('utf-8')  # Converter bytes para string

# Função para descriptografar a senha
def decrypt_password(encrypted_password):
    cipher_suite = Fernet(key)
    try:
        print(f"Tentando descriptografar: {encrypted_password}")  # Exibe a senha criptografada
        return cipher_suite.decrypt(encrypted_password.encode('utf-8')).decode()  # Converter string de volta para bytes
    except Exception as e:
        print(f"Erro ao descriptografar a senha: {e}")
        return "[ERRO NA DESCRIPTOGRAFIA]"

# Função para inserir uma nova senha
def inserir_senha(app, users, email, password, obs):
    conn = connect_db()
    cursor = conn.cursor()
    encrypted_password = encrypt_password(password)

    cursor.execute("""
        INSERT INTO senhas (apps, users, email, password, obs)
        VALUES (%s, %s, %s, %s, %s)
    """, (app, users, email, encrypted_password, obs))

    conn.commit()
    cursor.close()
    conn.close()
    print("Senha adicionada com sucesso!")

# Função para listar as senhas (com descriptografia)
def listar_senhas():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id, apps, users, email, password, obs FROM senhas")
    rows = cursor.fetchall()

    for row in rows:
        senha_descriptografada = decrypt_password(row[4])
        print(f"ID: {row[0]}, App: {row[1]}, User: {row[2]}, Email: {row[3]}, Senha: {senha_descriptografada}, Observação: {row[5]}")

    cursor.close()
    conn.close()

# Função para editar uma senha existente
def editar_senha(id_senha, novo_password):
    conn = connect_db()
    cursor = conn.cursor()
    encrypted_password = encrypt_password(novo_password)

    cursor.execute("""
        UPDATE senhas
        SET password = %s
        WHERE id = %s
    """, (encrypted_password, id_senha))

    conn.commit()
    cursor.close()
    conn.close()
    print("Senha atualizada com sucesso!")

# Função para excluir uma senha
def excluir_senha(id_senha):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM senhas WHERE id = %s", (id_senha,))

    conn.commit()
    cursor.close()
    conn.close()
    print("Senha excluída com sucesso!")

# Função para gerar senhas seguras aleatoriamente
def gerar_senha(tamanho=16):
    caracteres = string.ascii_letters + string.digits + string.punctuation
    senha = ''.join(random.choice(caracteres) for i in range(tamanho))
    return senha

# Interface simples de menu via terminal
def menu():
    while True:
        print("\nGerenciador de Senhas")
        print("1. Inserir nova senha")
        print("2. Listar senhas")
        print("3. Editar senha")
        print("4. Excluir senha")
        print("5. Gerar senha segura")
        print("6. Sair")

        escolha = input("\nEscolha uma opção: ")

        if escolha == "1":
            app = input("App: ")
            users = input("Usuário: ")
            email = input("Email: ")
            password = input("Senha: ")
            obs = input("Observação: ")
            inserir_senha(app, users, email, password, obs)
        elif escolha == "2":
            listar_senhas()
        elif escolha == "3":
            id_senha = input("ID da senha a ser editada: ")
            novo_password = input("Nova senha: ")
            editar_senha(id_senha, novo_password)
        elif escolha == "4":
            id_senha = input("ID da senha a ser excluída: ")
            excluir_senha(id_senha)
        elif escolha == "5":
            tamanho = int(input("Tamanho da senha: "))
            print(f"Senha gerada: {gerar_senha(tamanho)}")
        elif escolha == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

# Executar o menu
if __name__ == "__main__":
    menu()

