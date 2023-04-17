import sqlite3 as db

class Usuario:
    def __init__( self , nome_completo , contato , cpf_acesso , tipo_usuario ):
        self.nome_completo = nome_completo
        self.contato = contato
        self.cpf_acesso = cpf_acesso
        self.tipo_usuario = tipo_usuario

class Veiculo:
    def __init__(self , cod_cliente , tipo_veiculo , cor_veiculo ):
        self.cod_cliente = cod_cliente
        self.tipo_veiculo = tipo_veiculo
        self.cor_veiculo = cor_veiculo

class Servico:
    "teste"

def my_conn():
    return db.connect("gom.db")

def novo_usuario(usuario):
    "O parametro usuario deve receber um objeto class, Se o retorno dessa func for False o usuario ja existe"

    if ver_usuario(usuario.cpf_acesso):
        return False

    conn = my_conn()
    cur = conn.cursor()
    
    SQL = f"""
    INSERT INTO usuario (nome_completo , contato , cpf_acesso , tipo_usuario)
    VALUES ( '{usuario.nome_completo}','{usuario.contato}','{usuario.cpf_acesso}','{usuario.tipo_usuario}' )
    """

    cur.execute(SQL)

    conn.commit()
    conn.close()

    return True

def cons_usuarios():
    conn = my_conn()
    cur = conn.cursor()

    SQL = f"""
    SELECT * FROM usuario
    """

    result = cur.execute(SQL).fetchall()

    conn.commit()
    conn.close()

    return result

def ver_usuario(cpf_usuario):
    "Verifica se usuario ja existe no sistema"
    conn = my_conn()
    cur = conn.cursor()

    SQL = f"""
    SELECT * FROM usuario WHERE cpf_acesso LIKE '{cpf_usuario}'
    """

    result = cur.execute(SQL).fetchall()

    conn.commit()
    conn.close()

    if len(result) > 0:
        return True
    else:
        return False

def ver_usuario_detalhes(cpf_usuario):
    "Retorna detalhes do usuario tupla"
    conn = my_conn()
    cur = conn.cursor()

    SQL = f"""
    SELECT * FROM usuario WHERE cpf_acesso LIKE '{cpf_usuario}'
    """

    result = cur.execute(SQL).fetchall()

    conn.commit()
    conn.close()

    return result

def novo_veiculo(id_cliente,veiculo):
    conn = my_conn()
    cur = conn.cursor()
    
    SQL = f"""
    INSERT INTO veiculo ( cod_cliente , tipo_veiculo , cor_veiculo )
    VALUES ( {id_cliente} ,'{veiculo.tipo_veiculo}','{veiculo.cor_veiculo}' )
    """

    cur.execute(SQL)



    conn.commit()
    conn.close()

def ver_veiculo_usu(id_cliente):
    "Retorna detalhes do veiculo tupla"
    conn = my_conn()
    cur = conn.cursor()

    SQL = f"""
    SELECT * FROM veiculo WHERE cod_cliente LIKE {id_cliente}
    """

    result = cur.execute(SQL).fetchall()

    conn.commit()
    conn.close()
 
    return result

if __name__=="__main__":
    conn = my_conn()
    cur = conn.cursor()

    # Criando tabela usuario
    SQL = "CREATE TABLE usuario ( id integer primary key , nome_completo , contato , cpf_acesso , tipo_usuario )"
    cur.execute(SQL)

    # Criando tabela veiculo
    SQL = "CREATE TABLE veiculo ( id integer primary key , cod_cliente , tipo_veiculo , cor_veiculo )"
    cur.execute(SQL)

    conn.commit()
    conn.close()
