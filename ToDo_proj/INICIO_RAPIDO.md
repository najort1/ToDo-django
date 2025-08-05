# 🚀 Início Rápido - ToDo Django

## Para usuários que querem apenas executar o projeto:

### Opção 1: Configuração Automática (Recomendado)
1. Certifique-se de ter o Python 3.8+ instalado
2. Execute o arquivo: `setup_projeto.bat`
3. Siga as instruções na tela
4. Pronto! 🎉

### Opção 2: Configuração Manual Rápida
```bash
# 1. Criar ambiente virtual
python -m venv venv

# 2. Ativar ambiente virtual
venv\Scripts\activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar migrações
python manage.py migrate

# 5. Iniciar servidor
python manage.py runserver
```

## Acessar a aplicação:
- **Aplicação principal:** http://127.0.0.1:8000
- **Painel admin:** http://127.0.0.1:8000/admin (requer superusuário)

## Criar superusuário (opcional):
```bash
python manage.py createsuperuser
```

## Parar o servidor:
Pressione `Ctrl + C` no terminal

---

**Dica:** Para mais detalhes, consulte o arquivo `README.md` completo.