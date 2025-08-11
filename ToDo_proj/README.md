# ToDo Django 📝

Aplicação web completa de gerenciamento de tarefas desenvolvida em Django com sistema avançado de autenticação, gerenciamento de usuários e dashboard administrativo.

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
   - Dashboard Admin: http://127.0.0.1:8000/user/admin-dashboard/
   - Admin Django: http://127.0.0.1:8000/admin

---

## 📋 Funcionalidades

### Sistema de Autenticação
- ✅ Cadastro de usuários com validação completa
- ✅ Login/Logout seguro
- ✅ Sistema de sessões
- ✅ Validação de formulários avançada

### Gerenciamento de Usuários
- ✅ **Modelo de usuário customizado** com campos adicionais:
  - CPF, telefone, data de nascimento, gênero
  - Tipos de usuário (Admin, User, Observer)
  - Sistema de endereços completo com CEP
- ✅ **Dashboard administrativo** com interface moderna
- ✅ **Gerenciamento completo de usuários** (ativar/desativar, editar, excluir)
- ✅ **Estatísticas visuais** com gráficos de gênero e idade
- ✅ **Sistema de permissões** baseado em tipos de usuário

### Gerenciamento de Tarefas
- ✅ **Sistema de status avançado**: Pendente, Em Andamento, Concluído
- ✅ Criar, editar e excluir tarefas
- ✅ Interface AJAX para atualizações dinâmicas
- ✅ **Filtros por status** e paginação
- ✅ **Estatísticas de tarefas** por usuário
- ✅ Tarefas organizadas por usuário

### Interface e UX
- ✅ **Design responsivo** e moderno
- ✅ **AG-Grid** para tabelas interativas
- ✅ **Chart.js** para gráficos estatísticos
- ✅ **Modais avançados** para detalhes e edição
- ✅ **Feedback visual** para todas as ações
- ✅ **Interface AJAX** para experiência fluida

### APIs REST
- ✅ **API completa de usuários** (CRUD)
- ✅ **APIs de estatísticas** (gênero, idade, tarefas)
- ✅ **Endpoints de ativação/desativação** de usuários
- ✅ **API de detalhes completos** de usuários
- ✅ **APIs de gerenciamento de tarefas**

---

## 📁 Estrutura do Projeto

```
ToDo_proj/
├── ToDo_app/              # App principal de tarefas
│   ├── models.py          # Modelo Task com status avançado
│   ├── views.py           # Views de tarefas e APIs
│   ├── urls.py            # URLs do app de tarefas
│   ├── choices.py         # Choices para status e meses
│   └── templates/         # Templates de tarefas
│       ├── base.html      # Template base
│       ├── index.html     # Página inicial
│       └── tasks/         # Templates específicos de tarefas
├── ToDo_auth_app/         # App de autenticação
│   ├── forms.py           # Formulários de autenticação
│   ├── views.py           # Views de auth
│   ├── services.py        # Serviços de autenticação
│   └── templates/auth/    # Templates de autenticação
├── ToDo_user_app/         # App de gerenciamento de usuários
│   ├── models.py          # Modelos Usuario e Address
│   ├── views.py           # Views administrativas e APIs
│   ├── urls.py            # URLs do sistema administrativo
│   ├── choices.py         # Choices para usuários e endereços
│   └── templates/         # Templates administrativos
│       └── admin_dashboard.html  # Dashboard principal
├── ToDo_proj/             # Configurações do projeto
│   ├── settings.py        # Configurações Django
│   ├── urls.py           # URLs principais
│   └── wsgi.py           # Configuração WSGI
├── static/                # Arquivos estáticos
│   ├── css/              # Estilos CSS
│   │   ├── base.css      # Estilos base
│   │   ├── auth.css      # Estilos de autenticação
│   │   ├── dashboard.css # Estilos do dashboard de tarefas
│   │   ├── index.css     # Estilos da página inicial
│   │   └── admin-dashboard.css # Estilos do dashboard admin
│   └── js/               # Scripts JavaScript
│       ├── base.js       # Scripts base
│       ├── dashboard.js  # Scripts do dashboard de tarefas
│       └── admin-dashboard.js # Scripts do dashboard admin
├── requirements.txt       # Dependências Python
├── manage.py             # Utilitário Django
├── setup_projeto.bat    # Script de configuração automática
├── README.md             # Este arquivo
└── INICIO_RAPIDO.md      # Guia de início rápido
```

---

## 👥 Tipos de Usuário

### Admin (A)
- ✅ Acesso completo ao dashboard administrativo
- ✅ Gerenciamento de todos os usuários
- ✅ Visualização de estatísticas globais
- ✅ Ativação/desativação de usuários

### Observer (O)
- ✅ Acesso ao dashboard administrativo
- ✅ Visualização de dados e estatísticas
- ✅ Sem permissões de edição

### User (U)
- ✅ Acesso ao dashboard de tarefas
- ✅ Gerenciamento das próprias tarefas
- ✅ Perfil pessoal

---

## 🔧 Tecnologias Utilizadas

### Backend
- **Django 5.2.4** - Framework web principal
- **SQLite** - Banco de dados (desenvolvimento)
- **email-validator 2.2.0** - Validação de emails

### Frontend
- **HTML5, CSS3, JavaScript** - Tecnologias base
- **AG-Grid** - Tabelas interativas avançadas
- **Chart.js** - Gráficos e visualizações
- **Font Awesome** - Ícones
- **CSS Grid/Flexbox** - Layout responsivo

### Funcionalidades Avançadas
- **AJAX** - Atualizações dinâmicas
- **REST APIs** - Comunicação frontend/backend
- **Modais** - Interface de usuário moderna
- **Paginação** - Otimização de performance
- **Filtros dinâmicos** - Experiência de usuário aprimorada

---

## 🎯 Principais Endpoints

### Autenticação
- `/auth/login/` - Login de usuários
- `/auth/register/` - Cadastro de usuários
- `/auth/logout/` - Logout

### Tarefas
- `/tasks/` - Dashboard de tarefas
- `/tasks/create/` - Criar tarefa
- `/tasks/update/<id>/` - Atualizar tarefa
- `/tasks/delete/<id>/` - Excluir tarefa
- `/tasks/complete/<id>/` - Marcar como concluída

### Administração
- `/user/admin-dashboard/` - Dashboard administrativo
- `/user/api/users/` - API de usuários
- `/user/api/gender-stats/` - Estatísticas de gênero
- `/user/api/age-stats/` - Estatísticas de idade
- `/user/api/user/details/<id>/` - Detalhes do usuário
- `/user/api/user/activate/<id>/` - Ativar usuário
- `/user/api/user/deactivate/<id>/` - Desativar usuário

---