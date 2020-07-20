DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS proprietario;

CREATE TABLE usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_usuario TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
);

CREATE TABLE proprietario (
    cod_proprietario INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    RG TEXT NOT NULL,
    CPF_CNPJ TEXT NOT NULL,
    razao_social TEXT,
    estado_de_moradia TEXT NOT NULL,
    cidade_de_moradia TEXT NOT NULL,
    endereco_de_moradia TEXT NOT NULL,
    numero_de_moradia TEXT NOT NULL,
    complemento_endereco TEXT,
    telefone TEXT NOT NULL,
    celular TEXT NOT NULL,
    email TEXT NOT NULL,
    liberar_acesso BOL,
    id_autor INTEGER NOT NULL,
    data_cadastro TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_autor) REFERENCES user (id)
);