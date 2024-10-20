import string as st
import numpy as np

def gerar_senha(tamanho):
    """
    Gera uma senha aleatória composta por letras, números e caracteres especiais.

    Args:
        tamanho (int): O comprimento da senha a ser gerada.

    Returns:
        str: Uma senha aleatória gerada.
    """
    letras = st.ascii_letters
    numeros = st.digits
    especiais = st.punctuation

    algarismos = letras + numeros + especiais
    senha = np.random.choice(list(algarismos), tamanho)

    return ''.join(senha)

# Solicita ao usuário o tamanho da senha
quant_digit = int(input("\nInforme o tamanho da senha desejada: "))

# Gera e exibe a senha
senha_gerada = gerar_senha(quant_digit)
print('', senha_gerada)

print("")
