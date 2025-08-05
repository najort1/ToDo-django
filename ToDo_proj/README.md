# ToDo Django 📝

Aplicação web de lista de tarefas desenvolvida em Django com sistema completo de autenticação e interface moderna.

## 🚀 Configuração Rápida (Recomendado)

### Configuração Automática
Para configurar o projeto automaticamente, simplesmente execute:

```bash
setup_projeto.bat
```

Este script irá:
- ✅ Verificar se o Python está instalado
- ✅ Criar e ativar um ambiente virtual
- ✅ Instalar todas as dependências
- ✅ Executar as migrações do banco de dados
- ✅ Oferecer criação de superusuário
- ✅ Iniciar o servidor (opcional)

**Requisitos:** Python 3.8+ instalado no sistema

---

## ⚙️ Configuração Manual

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a passo

1. **Clone o repositório**
   ```bash
   git clone https://github.com/najort1/ToDo-django.git
   cd ToDo_proj
   ```

2. **Crie um ambiente virtual**
   ```bash
   python -m venv venv
   ```

3. **Ative o ambiente virtual**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Instale as dependências**
   ```bash
   pip install -r requirements.txt
   ```

5. **Execute as migrações**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crie um superusuário (opcional)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor**
   ```bash
   python manage.py runserver
   ```

8. **Acesse a aplicação**
   - Aplicação: http://127.0.0.1:8000
   - Admin: http://127.0.0.1:8000/admin

---

## 📋 Funcionalidades

### Autenticação
- ✅ Cadastro de usuários
- ✅ Login/Logout
- ✅ Validação de formulários
- ✅ Sessões seguras

### Gerenciamento de Tarefas
- ✅ Criar, editar e excluir tarefas
- ✅ Marcar tarefas como concluídas
- ✅ Interface AJAX para atualizações dinâmicas
- ✅ Filtros e estatísticas
- ✅ Tarefas organizadas por usuário

### Interface
- ✅ Design responsivo
- ✅ Interface moderna e intuitiva
- ✅ Feedback visual para ações do usuário

---

## 📁 Estrutura do Projeto

```
ToDo_proj/
├── ToDo_app/              # App principal de tarefas
│   ├── models.py          # Modelos de dados
│   ├── views.py           # Lógica de visualização
│   ├── urls.py            # URLs do app
│   └── templates/         # Templates HTML
├── ToDo_auth_app/         # App de autenticação
│   ├── forms.py           # Formulários de auth
│   ├── views.py           # Views de auth
│   └── templates/         # Templates de auth
├── static/                # Arquivos estáticos
│   ├── css/               # Estilos CSS
│   └── js/                # Scripts JavaScript
├── requirements.txt       # Dependências Python
├── manage.py             # Utilitário Django
└── setup_projeto.bat    # Script de configuração automática
```

---

## 🔧 Tecnologias Utilizadas

- **Backend:** Django 5.2.4
- **Banco de Dados:** SQLite (desenvolvimento)
- **Frontend:** HTML5, CSS3, JavaScript
- **Validação:** email-validator
- **Estilo:** CSS customizado com design responsivo

---