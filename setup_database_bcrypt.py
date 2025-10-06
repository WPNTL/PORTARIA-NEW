#!/usr/bin/env python3
"""
Script consolidado para configurar o banco de dados SQLite com bcrypt.
Força o uso de bcrypt para todas as senhas.
"""

import sqlite3
import os
import bcrypt

DATABASE = 'portaria.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password_bcrypt(password):
    """Gera hash bcrypt para a senha"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Tabela usuarios
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            ip TEXT NOT NULL,
            is_admin INTEGER DEFAULT 0,
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

    conn.commit()
    conn.close()
    print("✓ Tabelas criadas/verificadas com sucesso.")

def add_missing_columns():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Adicionar is_admin se não existir
    cursor.execute("PRAGMA table_info(usuarios)")
    columns = [column[1] for column in cursor.fetchall()]
    if 'is_admin' not in columns:
        print("🔄 Adicionando coluna 'is_admin' à tabela 'usuarios'...")
        cursor.execute("ALTER TABLE usuarios ADD COLUMN is_admin INTEGER DEFAULT 0")
        conn.commit()
        print("✓ Coluna 'is_admin' adicionada.")

    conn.close()

def insert_default_users():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Inserir usuário ADMIN
    cursor.execute("SELECT id FROM usuarios WHERE username = 'ADMIN'")
    if not cursor.fetchone():
        senha_admin_hash = hash_password_bcrypt('admin123')
        cursor.execute("""
            INSERT INTO usuarios (
                username, senha, ip, is_admin,
                libinserir, libalterar, libexcluir, libconsulta,
                libid, libdestino, libtipo, libempresa, libnome, librg,
                libveiculo, libplaca, libcr, libn_nota, libobs,
                libdata_entrada, libdata_saida, libperiodo, libperiodoalterado,
                libusuario, libusuarioalterado, libhora_entrada, libhora_saida
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'ADMIN', senha_admin_hash, 'livre', 1,
            'sim', 'sim', 'sim', 'sim',
            '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', ''
        ))
        print("✓ Usuário ADMIN criado (senha: admin123) - BCRYPT.")
    else:
        print("👤 Usuário ADMIN já existe.")

    # Inserir usuário EDER
    cursor.execute("SELECT id FROM usuarios WHERE username = 'EDER'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (
                username, senha, ip, is_admin,
                libinserir, libalterar, libexcluir, libconsulta,
                libid, libdestino, libtipo, libempresa, libnome, librg,
                libveiculo, libplaca, libcr, libn_nota, libobs,
                libdata_entrada, libdata_saida, libperiodo, libperiodoalterado,
                libusuario, libusuarioalterado, libhora_entrada, libhora_saida
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'EDER', '12345', 'livre', 0,
            'sim', 'sim', 'sim', 'sim',
            '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', ''
        ))
        print("✓ Usuário EDER criado (senha: 12345) - TEXTO PLANO.")
    else:
        print("👤 Usuário EDER já existe.")

    # Inserir usuário VAGNER
    cursor.execute("SELECT id FROM usuarios WHERE username = 'VAGNER'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (
                username, senha, ip, is_admin,
                libinserir, libalterar, libexcluir, libconsulta,
                libid, libdestino, libtipo, libempresa, libnome, librg,
                libveiculo, libplaca, libcr, libn_nota, libobs,
                libdata_entrada, libdata_saida, libperiodo, libperiodoalterado,
                libusuario, libusuarioalterado, libhora_entrada, libhora_saida
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'VAGNER', 'vagner', 'livre', 0,
            'sim', 'sim', 'nao', 'sim',
            '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', ''
        ))
        print("✓ Usuário VAGNER criado (senha: vagner) - TEXTO PLANO.")
    else:
        print("👤 Usuário VAGNER já existe.")

    # Inserir usuário LIANE
    cursor.execute("SELECT id FROM usuarios WHERE username = 'LIANE'")
    if not cursor.fetchone():
        cursor.execute("""
            INSERT INTO usuarios (
                username, senha, ip, is_admin,
                libinserir, libalterar, libexcluir, libconsulta,
                libid, libdestino, libtipo, libempresa, libnome, librg,
                libveiculo, libplaca, libcr, libn_nota, libobs,
                libdata_entrada, libdata_saida, libperiodo, libperiodoalterado,
                libusuario, libusuarioalterado, libhora_entrada, libhora_saida
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            'LIANE', '230771', 'livre', 0,
            'sim', 'sim', 'nao', 'sim',
            '', '', '', '', '', '', '', '', '', '', '',
            '', '', '', '', '', '', '', ''
        ))
        print("✓ Usuário LIANE criado (senha: 230771) - TEXTO PLANO.")
    else:
        print("👤 Usuário LIANE já existe.")

    conn.commit()
    conn.close()
    print("✓ Usuários padrão verificados/inseridos.")


if __name__ == '__main__':
    print("🔧 Iniciando configuração do banco de dados com BCRYPT...")
    
    # 1. Criar/Verificar tabelas
    create_tables()
    
    # 2. Adicionar colunas ausentes (como is_admin)
    add_missing_columns()
    
    # 3. Inserir usuários padrão
    insert_default_users()
    
    print("\n🎉 Configuração do banco de dados concluída!")
    print("\n📝 Credenciais dos usuários padrão:")
    print("   - ADMIN (senha: admin123) - Administrador - BCRYPT")
    print("   - EDER (senha: 12345) - TEXTO PLANO")
    print("   - VAGNER (senha: vagner) - TEXTO PLANO")
    print("   - LIANE (senha: 230771) - TEXTO PLANO")
    print("\n💡 Agora você pode iniciar a aplicação Flask e fazer login.")
