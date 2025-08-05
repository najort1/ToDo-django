@echo off
chcp 65001 >nul
echo ========================================
echo    CONFIGURAÇÃO AUTOMÁTICA DO PROJETO
echo         ToDo Django Application
echo ========================================
echo.

:: Verificar se Python está instalado
echo [1/7] Verificando instalação do Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não encontrado!
    echo Por favor, instale o Python 3.8+ em: https://python.org
    echo Certifique-se de marcar "Add Python to PATH" durante a instalação
    pause
    exit /b 1
)
echo ✅ Python encontrado!
python --version
echo.

:: Verificar se pip está disponível
echo [2/7] Verificando pip...
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: pip não encontrado!
    echo Reinstale o Python com pip incluído
    pause
    exit /b 1
)
echo ✅ pip disponível!
echo.

:: Criar ambiente virtual
echo [3/7] Criando ambiente virtual...
if exist "venv" (
    echo ⚠️  Ambiente virtual já existe. Removendo o antigo...
    rmdir /s /q venv
)
python -m venv venv
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao criar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual criado com sucesso!
echo.

:: Ativar ambiente virtual
echo [4/7] Ativando ambiente virtual...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao ativar ambiente virtual
    pause
    exit /b 1
)
echo ✅ Ambiente virtual ativado!
echo.

:: Atualizar pip
echo [5/7] Atualizando pip...
python -m pip install --upgrade pip
echo ✅ pip atualizado!
echo.

:: Instalar dependências
echo [6/7] Instalando dependências do projeto...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao instalar dependências
    pause
    exit /b 1
)
echo ✅ Dependências instaladas com sucesso!
echo.

:: Executar migrações
echo [7/7] Executando migrações do banco de dados...
python manage.py makemigrations
python manage.py migrate
if %errorlevel% neq 0 (
    echo ❌ ERRO: Falha ao executar migrações
    pause
    exit /b 1
)
echo ✅ Migrações executadas com sucesso!
echo.

:: Perguntar sobre criação de superusuário
echo ========================================
echo           CONFIGURAÇÃO OPCIONAL
echo ========================================
echo.
set /p criar_super="Deseja criar um superusuário para acessar o admin? (s/n): "
if /i "%criar_super%"=="s" (
    echo.
    echo Criando superusuário...
    echo DICA: Use um email válido e senha forte
    python manage.py createsuperuser
    echo.
)

:: Finalização
echo ========================================
echo        CONFIGURAÇÃO CONCLUÍDA! 🎉
echo ========================================
echo.
echo ✅ Projeto configurado com sucesso!
echo.
echo PRÓXIMOS PASSOS:
echo 1. Para iniciar o servidor: python manage.py runserver
echo 2. Acesse: http://127.0.0.1:8000
echo 3. Admin (se criou superusuário): http://127.0.0.1:8000/admin
echo.
echo COMANDOS ÚTEIS:
echo - Ativar ambiente virtual: venv\Scripts\activate
echo - Executar testes: python manage.py test
echo - Criar migrações: python manage.py makemigrations
echo - Aplicar migrações: python manage.py migrate
echo.

set /p iniciar="Deseja iniciar o servidor agora? (s/n): "
if /i "%iniciar%"=="s" (
    echo.
    echo Iniciando servidor de desenvolvimento...
    echo Pressione Ctrl+C para parar o servidor
    echo.
    python manage.py runserver
) else (
    echo.
    echo Para iniciar o servidor posteriormente, execute:
    echo   venv\Scripts\activate
    echo   python manage.py runserver
)

echo.
echo Pressione qualquer tecla para sair...
pause >nul