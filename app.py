from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import os
from datetime import datetime
import bcrypt
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "portaria_secret_key_2024_change_in_production")

DATABASE = "portaria.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        os.system("python3 setup_database_bcrypt.py")

def check_password_bcrypt(password, hashed):
    """Verifica senha usando bcrypt"""
    return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))

def hash_password_bcrypt(password):
    """Gera hash bcrypt para a senha"""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def is_logged_in():
    return "username" in session

def is_admin():
    """Verifica se o usuário é administrador"""
    if not is_logged_in():
        return False
    return session.get("is_admin", False)

def admin_required(f):
    """Decorator para rotas que requerem admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin():
            flash("Acesso negado! Apenas administradores podem acessar esta área.", "error")
            return redirect(url_for("dashboard"))
        return f(*args, **kwargs)
    return decorated_function

def login_required(f):
    """Decorator para rotas que requerem login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("index"))
        return f(*args, **kwargs)
    return decorated_function

def check_permission(permission):
    if not is_logged_in():
        return False
    
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM usuarios WHERE username = ?", 
        (session["username"],)
    ).fetchone()
    conn.close()
    
    if user:
        return user[permission] == "sim"
    return False

@app.route("/")
def index():
    if is_logged_in():
        return redirect(url_for("dashboard"))
    
    conn = get_db_connection()
    usuarios = conn.execute("SELECT DISTINCT username FROM usuarios ORDER BY username").fetchall()
    conn.close()
    
    return render_template("index.html", usuarios=usuarios)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    senha = request.form["senha"]
    ip_rede = request.environ.get("REMOTE_ADDR", "127.0.0.1")
    
    conn = get_db_connection()
    user = conn.execute(
        "SELECT * FROM usuarios WHERE username = ?", 
        (username,)
    ).fetchone()
    conn.close()
    
    if not user:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for("index"))
    
    # Verificar senha (suporta bcrypt e texto plano)
    senha_valida = False
    if user["senha"].startswith("$2b$"):  # Hash bcrypt
        senha_valida = check_password_bcrypt(senha, user["senha"])
    else:  # Senha em texto plano (legado)
        senha_valida = (user["senha"] == senha)
    
    if not senha_valida:
        flash("A senha está incorreta!", "error")
        return redirect(url_for("index"))
    
    # Verificar IP
    if user["ip"] != "livre" and user["ip"] != ip_rede:
        flash("O IP está incorreto!", "error")
        return redirect(url_for("index"))
    
    # Login bem-sucedido
    session["username"] = username
    session["senha"] = senha
    session["ip"] = ip_rede if user["ip"] == "livre" else user["ip"]
    session["is_admin"] = (user["is_admin"] == 1) if "is_admin" in user.keys() else 0
    
    return redirect(url_for("dashboard"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))

@app.route("/dashboard")
@login_required
def dashboard():
    conn = get_db_connection()
    
    hoje = datetime.now().strftime("%Y-%m-%d")
    registros_hoje = conn.execute(
        "SELECT COUNT(*) as count FROM controle WHERE data_entrada = ?", 
        (hoje,)
    ).fetchone()["count"]
    
    veiculos_dentro = conn.execute(
        "SELECT COUNT(*) as count FROM controle WHERE data_saida = \"\" OR data_saida IS NULL"
    ).fetchone()["count"]
    
    ultimos_registros = conn.execute(
        """SELECT * FROM controle 
           ORDER BY id DESC 
           LIMIT 10"""
    ).fetchall()
    
    conn.close()
    
    return render_template("dashboard.html", 
                         registros_hoje=registros_hoje,
                         veiculos_dentro=veiculos_dentro,
                         ultimos_registros=ultimos_registros)

# ==================== ROTAS DE ADMIN ====================

@app.route("/admin")
@login_required
@admin_required
def admin_panel():
    """Painel principal de administração"""
    conn = get_db_connection()
    usuarios = conn.execute("SELECT * FROM usuarios ORDER BY username").fetchall()
    conn.close()
    
    return render_template("admin_panel.html", usuarios=usuarios)

@app.route("/admin/usuario/novo")
@login_required
@admin_required
def admin_novo_usuario():
    """Formulário para criar novo usuário"""
    return render_template("admin_usuario_form.html", usuario=None)

@app.route("/admin/usuario/criar", methods=["POST"])
@login_required
@admin_required
def admin_criar_usuario():
    """Criar novo usuário"""
    username = request.form.get("username", "").strip().upper()
    senha = request.form.get("senha", "")
    ip = request.form.get("ip", "livre")
    is_admin_flag = 1 if request.form.get("is_admin") == "sim" else 0
    
    # Permissões
    libinserir = request.form.get("libinserir", "nao")
    libalterar = request.form.get("libalterar", "nao")
    libexcluir = request.form.get("libexcluir", "nao")
    libconsulta = request.form.get("libconsulta", "nao")
    
    if not username or not senha:
        flash("Username e senha são obrigatórios!", "error")
        return redirect(url_for("admin_novo_usuario"))
    
    # Hash da senha usando bcrypt
    senha_hash = hash_password_bcrypt(senha)
    
    try:
        conn = get_db_connection()
        
        # Verificar se usuário já existe
        existing = conn.execute("SELECT id FROM usuarios WHERE username = ?", (username,)).fetchone()
        if existing:
            flash("Usuário já existe!", "error")
            conn.close()
            return redirect(url_for("admin_novo_usuario"))
        
        conn.execute("""
            INSERT INTO usuarios (
                username, senha, ip, is_admin,
                libinserir, libalterar, libexcluir, libconsulta,
                libid, libdestino, libtipo, libempresa, libnome, librg,
                libveiculo, libplaca, libcr, libn_nota, libobs,
                libdata_entrada, libdata_saida, libperiodo, libperiodoalterado,
                libusuario, libusuarioalterado, libhora_entrada, libhora_saida
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            username, senha_hash, ip, is_admin_flag,
            libinserir, libalterar, libexcluir, libconsulta,
            "", "", "", "", "", "", "", "", "", "", "",
            "", "", "", "", "", "", "", ""
        ))
        conn.commit()
        conn.close()
        
        flash(f"Usuário {username} criado com sucesso!", "success")
        return redirect(url_for("admin_panel"))
        
    except Exception as e:
        flash(f"Erro ao criar usuário: {str(e)}", "error")
        return redirect(url_for("admin_novo_usuario"))

@app.route("/admin/usuario/<int:user_id>/editar")
@login_required
@admin_required
def admin_editar_usuario(user_id):
    """Formulário para editar usuário"""
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    if not usuario:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for("admin_panel"))
    
    return render_template("admin_usuario_form.html", usuario=usuario)

@app.route("/admin/usuario/<int:user_id>/atualizar", methods=["POST"])
@login_required
@admin_required
def admin_atualizar_usuario(user_id):
    """Atualizar dados do usuário"""
    username = request.form.get("username", "").strip().upper()
    ip = request.form.get("ip", "livre")
    is_admin_flag = 1 if request.form.get("is_admin") == "sim" else 0
    
    # Permissões
    libinserir = request.form.get("libinserir", "nao")
    libalterar = request.form.get("libalterar", "nao")
    libexcluir = request.form.get("libexcluir", "nao")
    libconsulta = request.form.get("libconsulta", "nao")
    
    if not username:
        flash("Username é obrigatório!", "error")
        return redirect(url_for("admin_editar_usuario", user_id=user_id))
    
    try:
        conn = get_db_connection()
        conn.execute("""
            UPDATE usuarios SET
                username = ?, ip = ?, is_admin = ?,
                libinserir = ?, libalterar = ?, libexcluir = ?, libconsulta = ?
            WHERE id = ?
        """, (username, ip, is_admin_flag, libinserir, libalterar, libexcluir, libconsulta, user_id))
        conn.commit()
        conn.close()
        
        flash(f"Usuário {username} atualizado com sucesso!", "success")
        return redirect(url_for("admin_panel"))
        
    except Exception as e:
        flash(f"Erro ao atualizar usuário: {str(e)}", "error")
        return redirect(url_for("admin_editar_usuario", user_id=user_id))

@app.route("/admin/usuario/<int:user_id>/alterar-senha")
@login_required
@admin_required
def admin_alterar_senha_form(user_id):
    """Formulário para alterar senha"""
    conn = get_db_connection()
    usuario = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    
    if not usuario:
        flash("Usuário não encontrado!", "error")
        return redirect(url_for("admin_panel"))
    
    return render_template("admin_alterar_senha.html", usuario=usuario)

@app.route("/admin/usuario/<int:user_id>/alterar-senha", methods=["POST"])
@login_required
@admin_required
def admin_alterar_senha(user_id):
    """Alterar senha do usuário"""
    nova_senha = request.form.get("nova_senha", "")
    confirmar_senha = request.form.get("confirmar_senha", "")
    
    if not nova_senha or not confirmar_senha:
        flash("Ambos os campos são obrigatórios!", "error")
        return redirect(url_for("admin_alterar_senha_form", user_id=user_id))
    
    if nova_senha != confirmar_senha:
        flash("As senhas não coincidem!", "error")
        return redirect(url_for("admin_alterar_senha_form", user_id=user_id))
    
    # Hash da senha usando bcrypt
    senha_hash = hash_password_bcrypt(nova_senha)
    
    try:
        conn = get_db_connection()
        conn.execute("UPDATE usuarios SET senha = ? WHERE id = ?", (senha_hash, user_id))
        conn.commit()
        
        usuario = conn.execute("SELECT username FROM usuarios WHERE id = ?", (user_id,)).fetchone()
        conn.close()
        
        flash(f"Senha do usuário {usuario["username"]} alterada com sucesso!", "success")
        return redirect(url_for("admin_panel"))
        
    except Exception as e:
        flash(f"Erro ao alterar senha: {str(e)}", "error")
        return redirect(url_for("admin_alterar_senha_form", user_id=user_id))

@app.route("/admin/usuario/<int:user_id>/excluir", methods=["POST"])
@login_required
@admin_required
def admin_excluir_usuario(user_id):
    """Excluir usuário"""
    # Não permitir que o admin exclua a si mesmo
    conn = get_db_connection()
    usuario = conn.execute("SELECT username FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    
    if usuario and usuario["username"] == session["username"]:
        flash("Você não pode excluir seu próprio usuário!", "error")
        conn.close()
        return redirect(url_for("admin_panel"))
    
    try:
        conn.execute("DELETE FROM usuarios WHERE id = ?", (user_id,))
        conn.commit()
        conn.close()
        
        flash(f"Usuário {usuario["username"]} excluído com sucesso!", "success")
        
    except Exception as e:
        flash(f"Erro ao excluir usuário: {str(e)}", "error")
    
    return redirect(url_for("admin_panel"))

# ==================== ROTAS EXISTENTES ====================

@app.route("/novo_registro")
@login_required
def novo_registro():
    if not check_permission("libinserir"):
        flash("Você não tem permissão para inserir registros!", "error")
        return redirect(url_for("dashboard"))
    
    return render_template("novo_registro.html")

@app.route("/salvar_registro", methods=["POST"])
@login_required
def salvar_registro():
    if not check_permission("libinserir"):
        flash("Você não tem permissão para inserir registros!", "error")
        return redirect(url_for("dashboard"))
    
    destino = request.form.get("destino", "")
    tipo = request.form.get("tipo", "")
    empresa = request.form.get("empresa", "")
    nome = request.form.get("nome", "")
    rg = request.form.get("rg", "")
    veiculo = request.form.get("veiculo", "")
    placa = request.form.get("placa", "")
    cr = request.form.get("cr", "")
    data_entrada = request.form.get("data_entrada", "")
    hora_entrada = request.form.get("hora_entrada", "")
    n_nota = request.form.get("n_nota", "")
    obs = request.form.get("obs", "")
    
    periodo = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuario = session["username"]
    
    try:
        conn = get_db_connection()
        conn.execute("""
            INSERT INTO controle (
                destino, tipo, empresa, nome, rg, veiculo, placa, cr,
                data_entrada, data_saida, hora_entrada, hora_saida,
                n_nota, obs, periodo, periodoalterado, usuario, usuarioalterado, data_alterada
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            destino, tipo, empresa, nome, rg, veiculo, placa, cr,
            data_entrada, "", hora_entrada, "",
            n_nota, obs, periodo, "", usuario, "", ""
        ))
        conn.commit()
        conn.close()
        
        flash("Registro salvo com sucesso!", "success")
        return redirect(url_for("dashboard"))
        
    except Exception as e:
        flash(f"Erro ao salvar registro: {str(e)}", "error")
        return redirect(url_for("novo_registro"))

@app.route("/consultar")
@login_required
def consultar():
    if not check_permission("libconsulta"):
        flash("Você não tem permissão para consultar registros!", "error")
        return redirect(url_for("dashboard"))
    
    empresa = request.args.get("empresa", "")
    nome = request.args.get("nome", "")
    placa = request.args.get("placa", "")
    data_inicio = request.args.get("data_inicio", "")
    data_fim = request.args.get("data_fim", "")
    status = request.args.get("status", "")
    
    conn = get_db_connection()
    
    query = "SELECT * FROM controle WHERE 1=1"
    params = []
    
    if empresa:
        query += " AND empresa LIKE ?"
        params.append(f"%{empresa}%")
    
    if nome:
        query += " AND nome LIKE ?"
        params.append(f"%{nome}%")
    
    if placa:
        query += " AND placa LIKE ?"
        params.append(f"%{placa}%")
    
    if data_inicio:
        query += " AND data_entrada >= ?"
        params.append(data_inicio)
    
    if data_fim:
        query += " AND data_entrada <= ?"
        params.append(data_fim)
    
    if status == "dentro":
        query += " AND (data_saida = \"\" OR data_saida IS NULL)"
    elif status == "saiu":
        query += " AND data_saida != \"\" AND data_saida IS NOT NULL"
    
    query += " ORDER BY id DESC LIMIT 100"
    
    registros = conn.execute(query, params).fetchall()
    conn.close()
    
    return render_template("consultar.html", 
                         registros=registros,
                         empresa=empresa,
                         nome=nome,
                         placa=placa,
                         data_inicio=data_inicio,
                         data_fim=data_fim,
                         status=status)

@app.route("/editar_registro/<int:id>")
@login_required
def editar_registro(id):
    if not check_permission("libalterar"):
        flash("Você não tem permissão para alterar registros!", "error")
        return redirect(url_for("consultar"))
    
    conn = get_db_connection()
    registro = conn.execute("SELECT * FROM controle WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if not registro:
        flash("Registro não encontrado!", "error")
        return redirect(url_for("consultar"))
    
    return render_template("editar_registro.html", registro=registro)

@app.route("/atualizar_registro/<int:id>", methods=["POST"])
@login_required
def atualizar_registro(id):
    if not check_permission("libalterar"):
        flash("Você não tem permissão para alterar registros!", "error")
        return redirect(url_for("consultar"))
    
    destino = request.form.get("destino", "")
    tipo = request.form.get("tipo", "")
    empresa = request.form.get("empresa", "")
    nome = request.form.get("nome", "")
    rg = request.form.get("rg", "")
    veiculo = request.form.get("veiculo", "")
    placa = request.form.get("placa", "")
    cr = request.form.get("cr", "")
    data_entrada = request.form.get("data_entrada", "")
    data_saida = request.form.get("data_saida", "")
    hora_entrada = request.form.get("hora_entrada", "")
    hora_saida = request.form.get("hora_saida", "")
    n_nota = request.form.get("n_nota", "")
    obs = request.form.get("obs", "")
    
    periodoalterado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuarioalterado = session["username"]
    data_alterada = datetime.now().strftime("%Y-%m-%d")
    
    try:
        conn = get_db_connection()
        conn.execute("""
            UPDATE controle SET
                destino = ?, tipo = ?, empresa = ?, nome = ?, rg = ?, veiculo = ?, placa = ?, cr = ?,
                data_entrada = ?, data_saida = ?, hora_entrada = ?, hora_saida = ?,
                n_nota = ?, obs = ?, periodoalterado = ?, usuarioalterado = ?, data_alterada = ?
            WHERE id = ?
        """, (
            destino, tipo, empresa, nome, rg, veiculo, placa, cr,
            data_entrada, data_saida, hora_entrada, hora_saida,
            n_nota, obs, periodoalterado, usuarioalterado, data_alterada, id
        ))
        conn.commit()
        conn.close()
        
        flash("Registro atualizado com sucesso!", "success")
        return redirect(url_for("consultar"))
        
    except Exception as e:
        flash(f"Erro ao atualizar registro: {str(e)}", "error")
        return redirect(url_for("editar_registro", id=id))

@app.route("/excluir_registro/<int:id>", methods=["POST"])
@login_required
def excluir_registro(id):
    if not check_permission("libexcluir"):
        flash("Você não tem permissão para excluir registros!", "error")
        return redirect(url_for("consultar"))
    
    try:
        conn = get_db_connection()
        conn.execute("DELETE FROM controle WHERE id = ?", (id,))
        conn.commit()
        conn.close()
        
        flash("Registro excluído com sucesso!", "success")
        
    except Exception as e:
        flash(f"Erro ao excluir registro: {str(e)}", "error")
    
    return redirect(url_for("consultar"))

@app.route("/registrar_saida/<int:id>", methods=["POST"])
@login_required
def registrar_saida(id):
    if not check_permission("libalterar"):
        flash("Você não tem permissão para alterar registros!", "error")
        return redirect(url_for("consultar"))
    
    data_saida = datetime.now().strftime("%Y-%m-%d")
    hora_saida = datetime.now().strftime("%H:%M")
    periodoalterado = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    usuarioalterado = session["username"]
    data_alterada = datetime.now().strftime("%Y-%m-%d")
    
    try:
        conn = get_db_connection()
        conn.execute("""
            UPDATE controle SET
                data_saida = ?, hora_saida = ?, periodoalterado = ?, usuarioalterado = ?, data_alterada = ?
            WHERE id = ?
        """, (data_saida, hora_saida, periodoalterado, usuarioalterado, data_alterada, id))
        conn.commit()
        conn.close()
        
        flash("Saída registrada com sucesso!", "success")
        
    except Exception as e:
        flash(f"Erro ao registrar saída: {str(e)}", "error")
    
    return redirect(url_for("consultar"))

if __name__ == "__main__":
    init_db()
    app.run(debug=False, host="0.0.0.0", port=5000)

