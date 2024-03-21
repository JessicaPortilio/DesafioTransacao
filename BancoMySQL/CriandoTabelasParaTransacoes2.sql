DROP DATABASE TRANSACOES_DESAFIO;
CREATE DATABASE TRANSACOES_DESAFIO;
USE TRANSACOES_DESAFIO
-- Criação da Tabela Usuarios
CREATE TABLE Usuarios (
    IDUSUARIO INT PRIMARY KEY AUTO_INCREMENT,
    NomeCompleto VARCHAR(255),
    CPFCNPJ VARCHAR(20) UNIQUE,
    Email VARCHAR(255) UNIQUE,
    Salt CHAR(64),
    HashedSenha CHAR(64),
    TipoUsuario VARCHAR(10)
);

-- Criação da Tabela Carteiras
CREATE TABLE Carteiras (
    ID_USUARIO INT PRIMARY KEY,
    Saldo DECIMAL(10, 2),
    CONSTRAINT FK_CARTEIRAS_USUARIOS FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(IDUSUARIO)
);

-- Criação da Tabela Lojistas
CREATE TABLE Lojistas (
    ID_USUARIO INT PRIMARY KEY,
    CONSTRAINT FK_LOJISTAS_USUARIOS FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(IDUSUARIO)
);

-- Criação da Tabela Transferencias
CREATE TABLE Transferencias (
    IDTRANSFERENCIA INT PRIMARY KEY AUTO_INCREMENT,
    ID_USUARIO_REMETENTE INT,
    ID_USUARIO_DESTINATARIO INT,
    Valor DECIMAL(10, 2),
    Status VARCHAR(50),
    Data TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT FK_TRANSFERENCIAS_REMETENTE FOREIGN KEY (ID_USUARIO_REMETENTE) REFERENCES Usuarios(IDUSUARIO),
    CONSTRAINT FK_TRANSFERENCIAS_DESTINATARIO FOREIGN KEY (ID_USUARIO_DESTINATARIO) REFERENCES Usuarios(IDUSUARIO) -- Ou Lojistas(ID), dependendo do destinatário
);

-- Criação da Tabela Notificacoes
CREATE TABLE Notificacoes (
    IDNOTIFICACOES INT PRIMARY KEY AUTO_INCREMENT,
    ID_USUARIO INT,
    Tipo VARCHAR(50),
    Status VARCHAR(50),
    CONSTRAINT FK_NOTIFICACOES_USUARIOS FOREIGN KEY (ID_USUARIO) REFERENCES Usuarios(IDUSUARIO) -- Ou Lojistas(ID), dependendo do destinatário da notificação
);

DROP PROCEDURE InserirUsuario;

DELIMITER //

CREATE PROCEDURE InserirUsuario(
    p_NomeCompleto VARCHAR(255),
    p_CPFCNPJ VARCHAR(20),
    p_Email VARCHAR(255),
    p_Senha VARCHAR(255),
    p_TipoUsuario VARCHAR(10)
)
BEGIN
    DECLARE v_Salt CHAR(64);
    DECLARE v_HashedSenha CHAR(64);

    -- Gera um salt aleatório
    SET v_Salt = SHA2(UUID(), 256);

    -- Gera a senha hash usando o salt
    SET v_HashedSenha = SHA2(CONCAT(p_Senha, v_Salt), 256);

    -- Inserção do usuário
    INSERT INTO Usuarios (NomeCompleto, CPFCNPJ, Email, Salt, HashedSenha, TipoUsuario)
    VALUES (p_NomeCompleto, p_CPFCNPJ, p_Email, v_Salt, v_HashedSenha, p_TipoUsuario);

END //

DELIMITER ;


-- Inserção do primeiro usuário como COMUM
CALL InserirUsuario('Fulano de Tal', '12345678901', 'fulano@email.com', 'senha123', 'COMUM');

INSERT INTO 
	Carteiras (ID_USUARIO, Saldo) 
		VALUES (1, 1000.0);

-- Inserção do segundo usuário como COMUM
CALL InserirUsuario('Ciclano da Silva', '98765432101', 'ciclano@email.com', 'outrasenha456', 'COMUM');

INSERT INTO 
	Carteiras (ID_USUARIO, Saldo) 
		VALUES (2, 800.0);
		
CALL InserirUsuario('Betrana de Tal', '54376543565', 'betrana@email.com', 'maisumasenha123', 'LOJISTA');

INSERT INTO 
	Carteiras (ID_USUARIO, Saldo) 
		VALUES (3, 1000.0);
		
 SELECT U.IDUSUARIO, U.NOMECOMPLETO, U.CPFCNPJ, U.EMAIL, C.SALDO 
 FROM USUARIOS U
 INNER JOIN CARTEIRAS C 
 ON U.IDUSUARIO = C.ID_USUARIO;
 
 SELECT 
