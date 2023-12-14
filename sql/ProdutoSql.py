SQL_CRIAR_TABELA = """
 CREATE TABLE IF NOT EXISTS produto (
 id    INTEGER      PRIMARY KEY AUTOINCREMENT,
 nome  TEXT         NOT NULL,
 valor NUMERIC(9,2) NOT NULL,
 desc  TEXT         NOT NULL
 )
"""
SQL_INSERIR = """
 INSERT INTO produto (nome, valor, desc)
 VALUES (?,?,?)
"""
SQL_ALTERAR = """
 UPDATE produto
 SET nome=?, valor=?, desc=?
 WHERE id=?
"""
SQL_EXCLUIR = """
 DELETE FROM produto
 WHERE id=?
"""
SQL_OBTER_TODOS = """
 SELECT id, nome, valor, desc
 FROM produto
 ORDER BY nome
"""
SQL_OBTER_POR_ID = """
 SELECT id, nome, valor, desc
 FROM produto
 WHERE id=?
"""