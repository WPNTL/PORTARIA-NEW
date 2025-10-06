#!/usr/bin/env python3
"""
Script para verificar o estado atual do banco de dados com bcrypt
"""

import sqlite3
import os
import bcrypt

def check_password_bcrypt(password, hashed):
    """Verifica senha usando bcrypt"""
    try:
        return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))
    except:
        return False

def check_database_status():
    """Verifica o estado atual do banco de dados e usuários"""
    
    print("🔍 Verificando estado do banco de dados...")
    
    # Verificar se o arquivo do banco existe
    if not os.path.exists('portaria.db'):
        print("❌ Arquivo 'portaria.db' não encontrado!")
        print("   Execute: python3 setup_database_bcrypt.py")
        return False
    
    try:
        conn = sqlite3.connect('portaria.db')
        cursor = conn.cursor()
        
        # Verificar tabelas existentes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tabelas = [row[0] for row in cursor.fetchall()]
        
        print(f"📊 Tabelas encontradas: {', '.join(tabelas)}")
        
        if 'usuarios' not in tabelas:
            print("❌ Tabela 'usuarios' não encontrada!")
            return False
        
        # Listar todos os usuários
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        
        # Obter nomes das colunas
        cursor.execute("PRAGMA table_info(usuarios)")
        colunas = [col[1] for col in cursor.fetchall()]
        
        print(f"\n👥 Usuários encontrados ({len(usuarios)}):")
        print("-" * 80)
        
        for usuario in usuarios:
            dados = dict(zip(colunas, usuario))
            
            print(f"ID: {dados.get('id', 'N/A')}")
            print(f"Username: {dados.get('username', 'N/A')}")
            print(f"Senha: {dados.get('senha', 'N/A')[:20]}...")
            print(f"IP: {dados.get('ip', 'N/A')}")
            print(f"É Admin: {'Sim' if dados.get('is_admin') == 1 else 'Não'}")
            print(f"Pode Inserir: {dados.get('libinserir', 'N/A')}")
            print(f"Pode Alterar: {dados.get('libalterar', 'N/A')}")
            print(f"Pode Excluir: {dados.get('libexcluir', 'N/A')}")
            print(f"Pode Consultar: {dados.get('libconsulta', 'N/A')}")
            
            # Testar senhas comuns
            senha_atual = dados.get('senha', '')
            username = dados.get('username', '')
            
            senhas_teste = ['12345', 'admin123', 'vagner', '230771', username.lower() if username else '']
            
            print("Teste de senhas:")
            for senha_teste in senhas_teste:
                if not senha_teste:
                    continue
                    
                senha_valida = False
                if senha_atual.startswith('$2b$'):  # Hash bcrypt
                    senha_valida = check_password_bcrypt(senha_teste, senha_atual)
                else:  # Senha em texto plano
                    senha_valida = (senha_atual == senha_teste)
                
                status = "✅" if senha_valida else "❌"
                print(f"  {status} '{senha_teste}'")
            
            print("-" * 80)
        
        # Verificar registros de controle
        if 'controle' in tabelas:
            cursor.execute("SELECT COUNT(*) FROM controle")
            total_registros = cursor.fetchone()[0]
            print(f"\n📋 Registros de controle: {total_registros}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar banco de dados: {str(e)}")
        return False

if __name__ == "__main__":
    check_database_status()
