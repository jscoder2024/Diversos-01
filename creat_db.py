# Tabela para armazenar os usuarios que terão acesso ao gerenciador
CREATE TABLE users (
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100),
	email VARCHAR(100),
	password TEXT,
	data_criacao TIMESTAMP DEFAULT CURRRENT_TIMESTAMP
);


# Tabela para armazear as senhas dos aplicativos

CRETE TABLE senhas (
	id SERIAL PRIMARY KEY,
	apps VARCHAR(100),
	users VARCHAR(100),
	email VARCHAR(100),
	password TEXT,
	obs TEXT,
	data_xcriacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
