import sqlite3 as db
import os

class Usuario:
    def __init__( self , nome_completo , contato , cpf_acesso , tipo_usuario ):
        self.nome_completo = nome_completo
        self.contato = contato
        self.cpf_acesso = cpf_acesso
        self.tipo_usuario = tipo_usuario

class Veiculo:
    def __init__(self , tipo_veiculo , cor_veiculo , placa_veiculo ):
        self.tipo_veiculo = tipo_veiculo
        self.cor_veiculo = cor_veiculo
        self.placa_veiculo = placa_veiculo

class Servico:
    id_cliente = None
    nome_cliente = None
    placa_veiculo = None
    servico_realizado = None
    obs_servico = None

def novo_servico(servico):

    SQL = f"""
    INSERT INTO servico (id_cliente, nome_cliente , placa_veiculo , servico_realizado , obs_servico )
    VALUES ({servico.id_cliente},'{servico.nome_cliente}','{servico.placa_veiculo}','{servico.servico_realizado}','{servico.obs_servico}')
    """

    conn = my_conn()
    cur = conn.cursor()

    cur.execute(SQL)

    conn.commit()
    conn.close()

    return True

def del_servico(id_servico):
    conn = my_conn()
    cur = conn.cursor()

    SQL = f"DELETE FROM servico WHETE id={id_servico}"

    try: 
        cur.execute(SQL)
        conn.commit()
        conn.close()
        return True

    except:
        conn.close()
        return False

def con_servico(id_cliente):

    SQL = f"SELECT * FROM servico WHERE id_cliente={id_cliente}"

    conn = my_conn()
    cur = conn.cursor()

    try: 
        result = cur.execute(SQL).fetchall()
        conn.commit()
        conn.close()
        return result

    except:
        conn.close()
        return []

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

    return list(result)

def novo_veiculo(id_cliente,veiculo):
    conn = my_conn()
    cur = conn.cursor()
    
    SQL = f"""
    INSERT INTO veiculo ( cod_cliente , tipo_veiculo , cor_veiculo , placa_veiculo)
    VALUES ( {id_cliente} ,'{veiculo.tipo_veiculo}','{veiculo.cor_veiculo}' , '{veiculo.placa_veiculo}' )
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

if __name__ == "__main__" :

    if os.path.isfile('gom.db'):
        os.remove('gom.db')

    conn = my_conn()
    cur = conn.cursor()

    # Criando tabela usuario
    SQL = "CREATE TABLE usuario ( id integer primary key , nome_completo text , contato text , cpf_acesso text , tipo_usuario text)"
    cur.execute(SQL)

    # Criando tabela veiculo
    SQL = "CREATE TABLE veiculo ( id integer primary key , cod_cliente integer , tipo_veiculo text , cor_veiculo text , placa_veiculo text )"
    cur.execute(SQL)

    # Criando tabela veiculo
    SQL = "CREATE TABLE servico ( id integer primary key ,id_cliente integer, nome_cliente text , placa_veiculo text , servico_realizado text , obs_servico text )"
    cur.execute(SQL)

    usaurio_1 = Usuario("ROBERTO GOMES","85989613249","1","FUN")
    usaurio_2 = Usuario("JOSE DA SILVA","85988888888","12345678910","CLI")

    usuarios = [usaurio_1,usaurio_2]

    for user in usuarios:
        novo_usuario(user)

    conn.commit()
    conn.close()
