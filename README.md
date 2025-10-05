# Sistema de Controle de Portaria Modernizado

Este projeto apresenta uma versão modernizada de um sistema de controle de portaria, originalmente desenvolvido em PHP/MySQL, para uma arquitetura baseada em Python com o framework Flask e banco de dados SQLite.

## Tecnologias Utilizadas

*   **Backend:** Python 3.x, Flask
*   **Banco de Dados:** SQLite3
*   **Frontend:** HTML5, CSS3 (com Bootstrap), JavaScript

## Estrutura de Arquivos

A estrutura de diretórios do projeto é organizada da seguinte forma:

```
. (diretório raiz do projeto)
├── app.py                      # Aplicação Flask principal
├── create_db.py                # Script para criar e popular o banco de dados SQLite
├── portaria.db                 # Arquivo do banco de dados SQLite (gerado após execução de create_db.py)
├── README.md                   # Este arquivo de documentação
├── templates/                  # Contém os arquivos HTML (templates Jinja2)
│   ├── base.html               # Template base para todas as páginas
│   ├── index.html              # Página de login
│   ├── dashboard.html          # Dashboard principal
│   ├── novo_registro.html      # Formulário para adicionar novo registro
│   ├── consultar.html          # Página para consultar e gerenciar registros
│   └── editar_registro.html    # Formulário para editar um registro existente
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

Navegue até o diretório raiz do projeto no terminal e instale as bibliotecas Python necessárias:

```bash
pip install Flask Flask-Session
```

### 3. Inicialização do Banco de Dados

O banco de dados SQLite (`portaria.db`) será criado e populado com um usuário padrão ao executar o script `create_db.py`. Certifique-se de que o arquivo `portaria.db` não exista antes de executar este passo, ou exclua-o para garantir uma inicialização limpa.

```bash
python3 create_db.py
```

Você deverá ver a mensagem "Banco de dados 'portaria.db' e tabelas criadas com sucesso." no terminal.

### 4. Execução da Aplicação Flask

Após a criação do banco de dados, você pode iniciar a aplicação Flask:

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

## Usuários Padrão para Teste

Para testar a aplicação, utilize os seguintes usuários e senhas:

*   **Usuário:** `EDER`
    *   **Senha:** `12345`
    *   **Permissões:** Acesso completo (incluindo consulta).

*   **Usuário:** `LIANE`
    *   **Senha:** `12345`
    *   **Permissões:** Acesso completo (incluindo consulta).

## Observações Importantes

*   **Segurança:** Este projeto é uma modernização de um sistema legado e, como tal, algumas práticas de segurança (como hashing de senhas) não foram implementadas para manter a equivalência com o sistema original. Para um ambiente de produção, é **altamente recomendável** implementar hashing de senhas e outras medidas de segurança.
*   **Permissões de Usuário:** O sistema possui um controle básico de permissões (`libconsulta`), que pode ser expandido para gerenciar o acesso a outras funcionalidades.

---
