import tkinter as tk
from tkinter import messagebox
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import sqlite3

# Função para configurar o banco de dados SQLite
def setup_database():
    conn = sqlite3.connect('produtos.db')  # Conectar ao banco de dados (ou criar se não existir)
    cursor = conn.cursor()
    
    # Criar tabela se não existir
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        subtitulo TEXT,
        codigo_barras TEXT UNIQUE,  -- Definindo código de barras como único
        preco_original TEXT,
        preco_promocional TEXT
    )
    ''')
    conn.commit()
    conn.close()

# Função para verificar se o código de barras já existe
def codigo_barras_existe(codigo_barras):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT COUNT(*) FROM produtos WHERE codigo_barras = ?', (codigo_barras,))
    existe = cursor.fetchone()[0] > 0  # Retorna True se existir
    
    conn.close()
    return existe

# Função para inserir os dados no banco de dados
def inserir_dados(titulo, subtitulo, codigo_barras, preco_original, preco_promocional):
    conn = sqlite3.connect('produtos.db')
    cursor = conn.cursor()
    
    # Tentar inserir os dados, se o código de barras não existir
    try:
        cursor.execute('''
        INSERT INTO produtos (titulo, subtitulo, codigo_barras, preco_original, preco_promocional)
        VALUES (?, ?, ?, ?, ?)
        ''', (titulo, subtitulo, codigo_barras, preco_original, preco_promocional))
        
        conn.commit()
    except sqlite3.IntegrityError:
        messagebox.showinfo("Info", "Produto já existe no banco de dados.")
    finally:
        conn.close()

# Função para extrair os dados do produto
def extrair_dados_produto():
    url = url_entry.get()
    if not url:
        messagebox.showerror("Erro", "Por favor, insira uma URL")
        return

    # Inicializar o driver do Selenium
    driver = webdriver.Chrome()  # Substitua pelo caminho do seu WebDriver

    try:
        driver.get(url)
        print(f"Acessando URL: {url}")
        
        # Esperar que o título do produto seja carregado
        produto_titulo = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".div-info-title"))
        ).text
        
        produto_subtitulo = driver.find_element(By.CSS_SELECTOR, ".div-info-subtitle").text
        codigo_barras = driver.find_element(By.CSS_SELECTOR, ".div-info-bar-code").text.split(": ")[1]

        # Tentar encontrar o preço original (sem oferta)
        try:
            preco_original = driver.find_element(By.CSS_SELECTOR, ".info-price-original del").text
            # Remover o símbolo da moeda se necessário
            preco_original = preco_original.replace('R$', '').strip()  
        except:
            preco_original = "Preço original não encontrado"

        # Tentar encontrar o preço promocional
        try:
            preco_promocional = driver.find_element(By.CSS_SELECTOR, ".price-product-modal span[style*='font-size: 24px']").text
            # Remover o símbolo da moeda se necessário
            preco_promocional = preco_promocional.replace('R$', '').strip()
        except:
            preco_promocional = "00,00"  # Valor padrão caso não haja promoção

        # Formatar os preços de volta com o símbolo da moeda
        preco_original = f"R$ {preco_original}" if preco_original != "Preço original não encontrado" else preco_original
        preco_promocional = f"R$ {preco_promocional}" if preco_promocional != "00,00" else "R$ 00,00"
        
        # Exibir os dados na interface gráfica
        resultado_label.config(
            text=f"Produto: {produto_titulo}\n"
                 f"Subtítulo: {produto_subtitulo}\n"
                 f"Código de Barras: {codigo_barras}\n"
                 f"Preço Original: {preco_original}\n"
                 f"Preço Promocional: {preco_promocional}"
        )
        
        # Verificar se o código de barras já existe
        if codigo_barras_existe(codigo_barras):
            messagebox.showinfo("Info", "Produto já existe no banco de dados.")
        else:
            # Persistir dados no banco de dados
            inserir_dados(produto_titulo, produto_subtitulo, codigo_barras, preco_original, preco_promocional)
            messagebox.showinfo("Sucesso", "Dados do produto salvos com sucesso!")
        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao extrair os dados do produto: {e}")
    
    finally:
        driver.quit()

# Criação da interface gráfica usando Tkinter
app = tk.Tk()
app.title("Busca de Preços de Produtos")
app.geometry("600x500")  # Tamanho da janela
app.resizable(False, False)  # Desabilitar redimensionamento da janela
app.configure(bg="#f5f5f5")  # Cor de fundo

# Estilos de fontes
titulo_fonte = ("Arial", 16, "bold")
label_fonte = ("Arial", 12)
resultado_fonte = ("Arial", 10)

# Configuração do banco de dados
setup_database()

# Frame para o título
titulo_frame = tk.Frame(app, bg="#f5f5f5")
titulo_frame.pack(pady=20)

titulo_label = tk.Label(titulo_frame, text="Buscar Preço de Produto", font=titulo_fonte, fg="#333", bg="#f5f5f5")
titulo_label.pack()

# Frame para a URL
url_frame = tk.Frame(app, bg="#f5f5f5")
url_frame.pack(pady=10)

url_label = tk.Label(url_frame, text="URL do Produto:", font=label_fonte, bg="#f5f5f5")
url_label.grid(row=0, column=0, padx=5, pady=5)
url_entry = tk.Entry(url_frame, width=50, font=label_fonte)
url_entry.grid(row=0, column=1, padx=5, pady=5)

# Botão para buscar os dados
botao_frame = tk.Frame(app, bg="#f5f5f5")
botao_frame.pack(pady=20)

buscar_button = tk.Button(botao_frame, text="Buscar Dados", font=label_fonte, bg="#4CAF50", fg="white", width=15, command=extrair_dados_produto)
buscar_button.pack(pady=5)

# Label para exibir o resultado
resultado_frame = tk.Frame(app, bg="#f5f5f5", bd=1, relief=tk.SUNKEN)
resultado_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

resultado_label = tk.Label(resultado_frame, text="", justify="left", font=resultado_fonte, bg="#f5f5f5", fg="#333")
resultado_label.pack(pady=10, padx=10)

# Iniciar a aplicação Tkinter
app.mainloop()

