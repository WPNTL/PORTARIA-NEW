from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'portaria_secret_key_2024'

# Configuração do banco de dados
DATABASE = 'portaria.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        os.system('python3 create_db.py')

# Função para verificar se o usuário está logado
def is_logged_in():
    return 'username' in session

# Função para verificar permissões do usuário
def check_permission(permission):
    if not is_logged_in():
        return False
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM usuarios WHERE username = ?', 
        (session['username'],)
    ).fetchone()
    conn.close()
    
    if user:
        return user[permission] == 'sim'
    return False

@app.route('/')
def index():
    if is_logged_in():
        return redirect(url_for('dashboard'))
    
    # Buscar usuários para o dropdown
    conn = get_db_connection()
    usuarios = conn.execute('SELECT DISTINCT username FROM usuarios ORDER BY username').fetchall()
    conn.close()
    
    return render_template('index.html', usuarios=usuarios)

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    senha = request.form['senha']
    ip_rede = request.environ.get('REMOTE_ADDR', '127.0.0.1')
    
    conn = get_db_connection()
    user = conn.execute(
        'SELECT * FROM usuarios WHERE username = ?', 
        (username,)
    ).fetchone()
    conn.close()
    
    if not user:
        flash('Usuário não encontrado!', 'error')
        return redirect(url_for('index'))
    
    if user['senha'] != senha:
        flash('A senha está incorreta!', 'error')
        return redirect(url_for('index'))
    
    # Verificar IP (se não for 'livre', deve coincidir com o IP do usuário)
    if user['ip'] != 'livre' and user['ip'] != ip_rede:
        flash('O IP está incorreto!', 'error')
        return redirect(url_for('index'))
    
    # Login bem-sucedido
    session['username'] = username
    session['senha'] = senha
    session['ip'] = ip_rede if user['ip'] == 'livre' else user['ip']
    
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if not is_logged_in():
        return redirect(url_for('index'))
    
    # Buscar estatísticas básicas
    conn = get_db_connection()
    
    # Contar registros do dia atual
    hoje = datetime.now().strftime('%Y-%m-%d')
    registros_hoje = conn.execute(
        'SELECT COUNT(*) as count FROM controle WHERE data_entrada = ?', 
        (hoje,)
    ).fetchone()['count']
    
    # Contar veículos ainda na empresa (sem data de saída)
    veiculos_dentro = conn.execute(
        'SELECT COUNT(*) as count FROM controle WHERE data_saida = "" OR data_saida IS NULL'
    ).fetchone()['count']
    
    # Últimos registros
    ultimos_registros = conn.execute(
        '''SELECT * FROM controle 
           ORDER BY id DESC 
           LIMIT 10'''
    ).fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                         registros_hoje=registros_hoje,
                         veiculos_dentro=veiculos_dentro,
                         ultimos_registros=ultimos_registros)

@app.route('/novo_registro')
def novo_registro():
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libinserir'):
        flash('Você não tem permissão para inserir registros!', 'error')
        return redirect(url_for('dashboard'))
    
    return render_template('novo_registro.html')

@app.route('/salvar_registro', methods=['POST'])
def salvar_registro():
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libinserir'):
        flash('Você não tem permissão para inserir registros!', 'error')
        return redirect(url_for('dashboard'))
    
    # Obter dados do formulário
    destino = request.form.get('destino', '')
    tipo = request.form.get('tipo', '')
    empresa = request.form.get('empresa', '')
    nome = request.form.get('nome', '')
    rg = request.form.get('rg', '')
    veiculo = request.form.get('veiculo', '')
    placa = request.form.get('placa', '')
    cr = request.form.get('cr', '')
    data_entrada = request.form.get('data_entrada', '')
    hora_entrada = request.form.get('hora_entrada', '')
    n_nota = request.form.get('n_nota', '')
    obs = request.form.get('obs', '')
    
    # Dados de controle
    periodo = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    usuario = session['username']
    
    try:
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO controle (
                destino, tipo, empresa, nome, rg, veiculo, placa, cr,
                data_entrada, data_saida, hora_entrada, hora_saida,
                n_nota, obs, periodo, periodoalterado, usuario, usuarioalterado, data_alterada
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            destino, tipo, empresa, nome, rg, veiculo, placa, cr,
            data_entrada, '', hora_entrada, '',
            n_nota, obs, periodo, '', usuario, '', ''
        ))
        conn.commit()
        conn.close()
        
        flash('Registro salvo com sucesso!', 'success')
        return redirect(url_for('dashboard'))
        
    except Exception as e:
        flash(f'Erro ao salvar registro: {str(e)}', 'error')
        return redirect(url_for('novo_registro'))

@app.route('/consultar')
def consultar():
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libconsulta'):
        flash('Você não tem permissão para consultar registros!', 'error')
        return redirect(url_for('dashboard'))
    
    # Parâmetros de busca
    empresa = request.args.get('empresa', '')
    nome = request.args.get('nome', '')
    placa = request.args.get('placa', '')
    data_inicio = request.args.get('data_inicio', '')
    data_fim = request.args.get('data_fim', '')
    status = request.args.get('status', '')
    
    conn = get_db_connection()
    
    # Construir query dinâmica
    query = 'SELECT * FROM controle WHERE 1=1'
    params = []
    
    if empresa:
        query += ' AND empresa LIKE ?'
        params.append(f'%{empresa}%')
    
    if nome:
        query += ' AND nome LIKE ?'
        params.append(f'%{nome}%')
    
    if placa:
        query += ' AND placa LIKE ?'
        params.append(f'%{placa}%')
    
    if data_inicio:
        query += ' AND data_entrada >= ?'
        params.append(data_inicio)
    
    if data_fim:
        query += ' AND data_entrada <= ?'
        params.append(data_fim)
    
    if status == 'dentro':
        query += ' AND (data_saida = "" OR data_saida IS NULL)'
    elif status == 'saiu':
        query += ' AND data_saida != "" AND data_saida IS NOT NULL'
    
    query += ' ORDER BY id DESC LIMIT 100'
    
    registros = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template('consultar.html', 
                         registros=registros,
                         empresa=empresa,
                         nome=nome,
                         placa=placa,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         status=status)

@app.route('/editar_registro/<int:id>')
def editar_registro(id):
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libalterar'):
        flash('Você não tem permissão para alterar registros!', 'error')
        return redirect(url_for('consultar'))
    
    conn = get_db_connection()
    registro = conn.execute('SELECT * FROM controle WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if not registro:
        flash('Registro não encontrado!', 'error')
        return redirect(url_for('consultar'))
    
    return render_template('editar_registro.html', registro=registro)

@app.route('/atualizar_registro/<int:id>', methods=['POST'])
def atualizar_registro(id):
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libalterar'):
        flash('Você não tem permissão para alterar registros!', 'error')
        return redirect(url_for('consultar'))
    
    # Obter dados do formulário
    destino = request.form.get('destino', '')
    tipo = request.form.get('tipo', '')
    empresa = request.form.get('empresa', '')
    nome = request.form.get('nome', '')
    rg = request.form.get('rg', '')
    veiculo = request.form.get('veiculo', '')
    placa = request.form.get('placa', '')
    cr = request.form.get('cr', '')
    data_entrada = request.form.get('data_entrada', '')
    data_saida = request.form.get('data_saida', '')
    hora_entrada = request.form.get('hora_entrada', '')
    hora_saida = request.form.get('hora_saida', '')
    n_nota = request.form.get('n_nota', '')
    obs = request.form.get('obs', '')
    
    # Dados de controle
    periodoalterado = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    usuarioalterado = session['username']
    data_alterada = datetime.now().strftime('%Y-%m-%d')
    
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE controle SET
                destino = ?, tipo = ?, empresa = ?, nome = ?, rg = ?, veiculo = ?, placa = ?, cr = ?,
                data_entrada = ?, data_saida = ?, hora_entrada = ?, hora_saida = ?,
                n_nota = ?, obs = ?, periodoalterado = ?, usuarioalterado = ?, data_alterada = ?
            WHERE id = ?
        ''', (
            destino, tipo, empresa, nome, rg, veiculo, placa, cr,
            data_entrada, data_saida, hora_entrada, hora_saida,
            n_nota, obs, periodoalterado, usuarioalterado, data_alterada, id
        ))
        conn.commit()
        conn.close()
        
        flash('Registro atualizado com sucesso!', 'success')
        return redirect(url_for('consultar'))
        
    except Exception as e:
        flash(f'Erro ao atualizar registro: {str(e)}', 'error')
        return redirect(url_for('editar_registro', id=id))

@app.route('/excluir_registro/<int:id>', methods=['POST'])
def excluir_registro(id):
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libexcluir'):
        flash('Você não tem permissão para excluir registros!', 'error')
        return redirect(url_for('consultar'))
    
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM controle WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        
        flash('Registro excluído com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao excluir registro: {str(e)}', 'error')
    
    return redirect(url_for('consultar'))

@app.route('/registrar_saida/<int:id>', methods=['POST'])
def registrar_saida(id):
    if not is_logged_in():
        return redirect(url_for('index'))
    
    if not check_permission('libalterar'):
        flash('Você não tem permissão para alterar registros!', 'error')
        return redirect(url_for('consultar'))
    
    data_saida = datetime.now().strftime('%Y-%m-%d')
    hora_saida = datetime.now().strftime('%H:%M')
    periodoalterado = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    usuarioalterado = session['username']
    data_alterada = datetime.now().strftime('%Y-%m-%d')
    
    try:
        conn = get_db_connection()
        conn.execute('''
            UPDATE controle SET
                data_saida = ?, hora_saida = ?, periodoalterado = ?, usuarioalterado = ?, data_alterada = ?
            WHERE id = ?
        ''', (data_saida, hora_saida, periodoalterado, usuarioalterado, data_alterada, id))
        conn.commit()
        conn.close()
        
        flash('Saída registrada com sucesso!', 'success')
        
    except Exception as e:
        flash(f'Erro ao registrar saída: {str(e)}', 'error')
    
    return redirect(url_for('consultar'))

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)

