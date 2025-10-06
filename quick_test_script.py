#!/usr/bin/env python3
"""
Script de teste rápido para verificar configuração do sistema admin
"""

import sqlite3
import bcrypt

def test_database():
    print("=" * 60)
    print("TESTE DO SISTEMA ADMINISTRATIVO")
    print("=" * 60)
    
    try:
        conn = sqlite3.connect('portaria.db')
        cursor = conn.cursor()
        
        # Teste 1: Verificar tabela usuarios
        print("\n✓ TESTE 1: Verificando tabela 'usuarios'...")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuarios'")
        if cursor.fetchone():
            print("  ✓ Tabela 'usuarios' existe")
        else:
            print("  ✗ ERRO: Tabela 'usuarios' não existe!")
            return False
        
        # Teste 2: Verificar coluna is_admin
        print("\n✓ TESTE 2: Verificando coluna 'is_admin'...")
        cursor.execute("PRAGMA table_info(usuarios)")
        columns = [col[1] for col in cursor.fetchall()]
        if 'is_admin' in columns:
            print("  ✓ Coluna 'is_admin' existe")
        else:
            print("  ✗ ERRO: Coluna 'is_admin' não existe!")
            return False
        
        # Teste 3: Verificar usuário ADMIN
        print("\n✓ TESTE 3: Verificando usuário ADMIN...")
        cursor.execute("SELECT username, senha, is_admin FROM usuarios WHERE username = 'ADMIN'")
        admin = cursor.fetchone()
        
        if not admin:
            print("  ✗ ERRO: Usuário ADMIN não encontrado!")
            return False
        
        print(f"  ✓ Usuário ADMIN encontrado")
        print(f"  - Username: {admin[0]}")
        print(f"  - is_admin: {admin[2]}")
        
        # Teste 4: Verificar bcrypt
        print("\n✓ TESTE 4: Verificando hash bcrypt...")
        if admin[1].startswith('$2b$'):
            print("  ✓ Senha está usando bcrypt")
            
            # Testar senha
            senha_correta = bcrypt.checkpw('admin123'.encode('utf-8'), admin[1].encode('utf-8'))
            if senha_correta:
                print("  ✓ Senha 'admin123' está correta")
            else:
                print("  ✗ ERRO: Senha 'admin123' não funciona!")
        else:
            print("  ✗ AVISO: Senha não está usando bcrypt!")
            print(f"  - Senha atual: {admin[1]}")
        
        # Teste 5: Listar todos os usuários
        print("\n✓ TESTE 5: Listando todos os usuários...")
        cursor.execute("SELECT username, is_admin FROM usuarios")
        usuarios = cursor.fetchall()
        
        for user in usuarios:
            admin_status = "ADMIN" if user[1] == 1 else "Normal"
            print(f"  - {user[0]}: {admin_status}")
        
        conn.close()
        
        print("\n" + "=" * 60)
        print("✓ TODOS OS TESTES PASSARAM!")
        print("=" * 60)
        print("\nVocê pode agora:")
        print("1. Iniciar a aplicação: python3 app_bcrypt.py")
        print("2. Acessar: http://127.0.0.1:5000")
        print("3. Fazer login como ADMIN / admin123")
        print("4. Acessar: http://127.0.0.1:5000/admin")
        print("=" * 60)
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n✗ ERRO DE BANCO DE DADOS: {e}")
        print("\nSolução: Execute 'python3 setup_database_bcrypt.py'")
        return False
    except Exception as e:
        print(f"\n✗ ERRO: {e}")
        return False

if __name__ == "__main__":
    test_database()
