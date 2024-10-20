import os
import subprocess

def linguagens_instaladas():
    linguagens = {}

    # Verifica se Python está instalado e obtém a versão
    if subprocess.call(["which", "python3"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["python3", "--version"]).decode().strip()
        linguagens["Python"] = {"extensao": ".py", "versao": version}
    
    # Verifica se Java está instalado e obtém a versão
    if subprocess.call(["which", "java"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["java", "-version"], stderr=subprocess.STDOUT).decode().strip()
        linguagens["Java"] = {"extensao": ".java", "versao": version}
    
    # Verifica se C está instalado (gcc) e obtém a versão
    if subprocess.call(["which", "gcc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["gcc", "--version"]).decode().strip()
        linguagens["C"] = {"extensao": ".c", "versao": version}
    
    # Verifica se C++ está instalado (g++) e obtém a versão
    if subprocess.call(["which", "g++"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["g++", "--version"]).decode().strip()
        linguagens["C++"] = {"extensao": ".cpp", "versao": version}
    
    # Verifica se Ruby está instalado e obtém a versão
    if subprocess.call(["which", "ruby"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["ruby", "--version"]).decode().strip()
        linguagens["Ruby"] = {"extensao": ".rb", "versao": version}
    
    # Verifica se Perl está instalado e obtém a versão
    if subprocess.call(["which", "perl"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["perl", "--version"]).decode().strip()
        linguagens["Perl"] = {"extensao": ".pl", "versao": version}
    
    # Verifica se Rust está instalado e obtém a versão
    if subprocess.call(["which", "rustc"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["rustc", "--version"]).decode().strip()
        linguagens["Rust"] = {"extensao": ".rs", "versao": version}
    
    # Verifica se Bash está instalado e obtém a versão
    if subprocess.call(["which", "bash"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["bash", "--version"]).decode().strip()
        linguagens["Bash"] = {"extensao": ".sh", "versao": version}
    
    # Verifica se Node.js está instalado (JavaScript) e obtém a versão
    if subprocess.call(["which", "node"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
        version = subprocess.check_output(["node", "--version"]).decode().strip()
        linguagens["JavaScript"] = {"extensao": ".js", "versao": version}

    return linguagens

def listar_diretorios(diretorio, extensoes, excluidos=[]):
    contagem = {extensao: {} for extensao in extensoes}
    for root, dirs, files in os.walk(diretorio):
        # Excluir diretórios indesejados
        dirs[:] = [d for d in dirs if d not in excluidos]
        
        for file in files:
            _, ext = os.path.splitext(file)
            if ext in extensoes:
                if root not in contagem[ext]:
                    contagem[ext][root] = 0
                contagem[ext][root] += 1
    return contagem

if __name__ == "__main__":
    linguagens = linguagens_instaladas()
    extensoes = {linguagem: info["extensao"] for linguagem, info in linguagens.items()}

    print("Linguagens instaladas e versões:")
    for linguagem, info in linguagens.items():
        print(f"{linguagem}: {info['versao']} ({info['extensao']})")

    # Define o diretório a ser pesquisado, como seu diretório home
    diretorio = os.path.expanduser("~")
    excluidos = ['node_modules', '.git', 'venv']  # Exemplo de diretórios a serem excluídos
    contagem = listar_diretorios(diretorio, [info["extensao"] for info in linguagens.values()], excluidos)

    print("\nDiretórios com arquivos encontrados:")
    for ext, dirs in contagem.items():
        if dirs:
            print(f"\nArquivos com extensão {ext}:")
            for dir_path, count in dirs.items():
                print(f"{dir_path}: {count} arquivo(s)")

