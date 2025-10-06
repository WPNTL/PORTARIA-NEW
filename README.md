# Sistema de Controle de Portaria Modernizado

Este projeto apresenta uma versão modernizada de um sistema de controle de portaria, originalmente desenvolvido em PHP/MySQL, para uma arquitetura baseada em Python com o framework Flask e banco de dados SQLite.

## Tecnologias Utilizadas

*   **Backend:** Python 3.x, Flask
*   **Banco de Dados:** SQLite3
*   **Hashing de Senhas:** bcrypt
*   **Frontend:** HTML5, CSS3 (com Bootstrap), JavaScript

## Estrutura de Arquivos

A estrutura de diretórios do projeto é organizada da seguinte forma:

```
. (diretório raiz do projeto)
├── app.py               # Aplicação Flask principal (versão com bcrypt)
├── setup_database_bcrypt.py    # Script consolidado para criar/configurar o banco de dados com bcrypt
├── check_database_bcrypt.py    # Script para verificar o estado do banco de dados com bcrypt
├── portaria.db                 # Arquivo do banco de dados SQLite (gerado após execução de setup_database_bcrypt.py)
├── README.md                   # Este arquivo de documentação
├── templates/                  # Contém os arquivos HTML (templates Jinja2)
│   ├── base.html               # Template base para todas as páginas
│   ├── index.html              # Página de login
│   ├── dashboard.html          # Dashboard principal
│   ├── novo_registro.html      # Formulário para adicionar novo registro
│   ├── consultar.html          # Página para consultar e gerenciar registros
│   ├── editar_registro.html    # Formulário para editar um registro existente
│   ├── admin_panel.html        # Painel de administração
│   ├── admin_usuario_form.html # Formulário para criar/editar usuários admin
│   └── admin_alterar_senha.html# Formulário para alterar senha de usuários admin
└── static/                     # Contém arquivos estáticos (CSS, JS, imagens)
    ├── css/
    │   └── style.css           # Estilos CSS personalizados
    └── js/
        └── main.js             # Scripts JavaScript personalizados
```

## Configuração e Execução

Siga os passos abaixo para configurar e executar a aplicação em seu ambiente local.

### 1. Pré-requisitos

Certifique-se de ter o Python 3.x e o `pip` (gerenciador de pacotes do Python) instalados em seu sistema.

### 2. Instalação das Dependências

Navegue até o diretório raiz do projeto no terminal e instale as bibliotecas Python necessárias. **É crucial instalar `bcrypt` para o hashing de senhas.**

```bash
pip install Flask Flask-Session bcrypt
```

### 3. Configuração do Banco de Dados (Com BCRYPT)

Para garantir que o banco de dados `portaria.db` seja criado corretamente com todas as tabelas e usuários padrão, **com o usuário ADMIN usando hashing bcrypt**, siga estes passos:

1.  **Pare a aplicação Flask** (se estiver rodando).
2.  **Exclua *qualquer* arquivo `portaria.db` existente** no diretório do projeto. No terminal, execute:
    ```bash
    del portaria.db  # No Windows
    # ou
    rm portaria.db   # No Linux/macOS
    ```
    **Verifique manualmente** se o arquivo `portaria.db` realmente não está mais lá após este comando.
3.  **Execute o script de configuração do banco de dados com bcrypt:**
    ```bash
    python3 setup_database_bcrypt.py
    ```
    Este script irá criar um novo `portaria.db` com a estrutura correta e inserir os usuários padrão, incluindo o `ADMIN` com a senha `admin123` hasheada com bcrypt. Você deverá ver mensagens de sucesso no terminal.

### 4. Verificação do Banco de Dados (Opcional, mas recomendado)

Para confirmar que o banco de dados e os usuários foram criados corretamente, você pode executar o script de verificação com suporte a bcrypt:

```bash
python3 check_database_bcrypt.py
```

### 5. Execução da Aplicação Flask (Com BCRYPT)

Após a configuração do banco de dados, você pode iniciar a aplicação Flask usando a versão `app_bcrypt.py`:

```bash
python3 app.py
```

O servidor Flask será iniciado e estará acessível em `http://127.0.0.1:5000` (ou outro endereço IP local, dependendo da sua configuração de rede).

## Funcionalidades

O sistema oferece as seguintes funcionalidades principais:

*   **Login de Usuário:** Autenticação baseada em usuários e senhas armazenados no SQLite.
*   **Dashboard:** Visão geral dos registros do dia e veículos "dentro" da portaria.
*   **Novo Registro:** Formulário para registrar a entrada de veículos, coletando informações como destino, tipo de veículo, motorista, placa, etc.
*   **Consultar Registros:** Página para buscar, filtrar e visualizar todos os registros de entrada/saída.
*   **Registrar Saída:** Opção para marcar a saída de um veículo, atualizando o status e a hora de saída no banco de dados.
*   **Editar Registro:** Permite modificar os detalhes de um registro existente.
*   **Excluir Registro:** Remove um registro do sistema.
*   **Painel de Administração:** (Acessível apenas para usuários `is_admin=1`) Gerenciamento de usuários, incluindo criação, edição, exclusão e alteração de senhas e permissões.

## Usuários Padrão para Teste

Para testar a aplicação, utilize os seguintes usuários e senhas:

*   **Usuário:** `ADMIN`
    *   **Senha:** `admin123`
    *   **Permissões:** Acesso completo e privilégios de administrador (senha hasheada com bcrypt).

*   **Usuário:** `EDER`
    *   **Senha:** `12345`
    *   **Permissões:** Acesso completo (incluindo consulta) (senha em texto plano).

*   **Usuário:** `LIANE`
    *   **Senha:** `230771`
    *   **Permissões:** Acesso completo (exceto exclusão) (senha em texto plano).

## Observações Importantes

*   **Segurança:** Para um ambiente de produção, é **altamente recomendável** que *todas* as senhas sejam hasheadas (não apenas a do ADMIN) e que o `app.secret_key` seja uma chave forte e secreta.
*   **Permissões de Usuário:** O sistema possui um controle básico de permissões (`libconsulta`, `libinserir`, etc.), que pode ser expandido para gerenciar o acesso a outras funcionalidades.

---
