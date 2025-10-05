
import sqlite3

def create_database():
    conn = sqlite3.connect('portaria.db')
    cursor = conn.cursor()

    # Tabela usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            senha TEXT NOT NULL,
            ip TEXT NOT NULL,
            libinserir TEXT NOT NULL,
            libalterar TEXT NOT NULL,
            libexcluir TEXT NOT NULL,
            libid TEXT NOT NULL,
            libdestino TEXT NOT NULL,
            libtipo TEXT NOT NULL,
            libempresa TEXT NOT NULL,
            libnome TEXT NOT NULL,
            librg TEXT NOT NULL,
            libveiculo TEXT NOT NULL,
            libplaca TEXT NOT NULL,
            libcr TEXT NOT NULL,
            libn_nota TEXT NOT NULL,
            libobs TEXT NOT NULL,
            libdata_entrada TEXT NOT NULL,
            libdata_saida TEXT NOT NULL,
            libperiodo TEXT NOT NULL,
            libperiodoalterado TEXT NOT NULL,
            libusuario TEXT NOT NULL,
            libusuarioalterado TEXT NOT NULL,
            libconsulta TEXT NOT NULL,
            libhora_entrada TEXT NOT NULL,
            libhora_saida TEXT NOT NULL
        )
    ''')

    # Inserindo dados de exemplo para usuários (do portaria.sql)
    cursor.execute("INSERT INTO usuarios (id, username, senha, ip, libinserir, libalterar, libexcluir, libid, libdestino, libtipo, libempresa, libnome, librg, libveiculo, libplaca, libcr, libn_nota, libobs, libdata_entrada, libdata_saida, libperiodo, libperiodoalterado, libusuario, libusuarioalterado, libconsulta, libhora_entrada, libhora_saida) VALUES (1,'EDER','12345','livre','sim','sim','sim','','','','','','','','','','','','','','','','','','','','')")
    cursor.execute("INSERT INTO usuarios (id, username, senha, ip, libinserir, libalterar, libexcluir, libid, libdestino, libtipo, libempresa, libnome, librg, libveiculo, libplaca, libcr, libn_nota, libobs, libdata_entrada, libdata_saida, libperiodo, libperiodoalterado, libusuario, libusuarioalterado, libconsulta, libhora_entrada, libhora_saida) VALUES (2,'VAGNER','vagner','livre','sim','sim','nao','','','','','','','','','','','','','','','','','','','','')")
    cursor.execute("INSERT INTO usuarios (id, username, senha, ip, libinserir, libalterar, libexcluir, libid, libdestino, libtipo, libempresa, libnome, librg, libveiculo, libplaca, libcr, libn_nota, libobs, libdata_entrada, libdata_saida, libperiodo, libperiodoalterado, libusuario, libusuarioalterado, libconsulta, libhora_entrada, libhora_saida) VALUES (3,'LIANE','230771','livre','sim','sim','nao','','','','','','','','','','','','','','','','','','','','')")

    # Tabela controle
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS controle (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            destino TEXT NOT NULL,
            tipo TEXT NOT NULL,
            empresa TEXT NOT NULL,
            nome TEXT NOT NULL,
            rg TEXT NOT NULL,
            veiculo TEXT NOT NULL,
            placa TEXT NOT NULL,
            cr TEXT NOT NULL,
            data_entrada TEXT NOT NULL,
            data_saida TEXT NOT NULL,
            hora_entrada TEXT NOT NULL,
            hora_saida TEXT NOT NULL,
            n_nota TEXT NOT NULL,
            obs TEXT NOT NULL,
            periodo TEXT NOT NULL,
            periodoalterado TEXT NOT NULL,
            usuario TEXT NOT NULL,
            usuarioalterado TEXT NOT NULL,
            data_alterada TEXT NOT NULL
        )
    ''')

    # As tabelas '2012' e '2013' parecem ser arquivos históricos e podem ser criadas dinamicamente ou ter uma abordagem diferente.
    # Por enquanto, vamos focar na tabela 'controle' principal.

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Banco de dados 'portaria.db' e tabelas criadas com sucesso.")

