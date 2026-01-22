# App Cadastro Django

## 📋 Descrição

**App Cadastro Django** é uma aplicação web construída com o framework Django para gerenciamento de cadastro de usuários. A aplicação fornece uma interface para visualizar e gerenciar dados de usuários através de uma administração intuitiva.

## 🎯 Funcionalidades

- **Cadastro de Usuários**: Adicionar, editar e remover usuários
- **Visualização de Usuários**: Listar todos os usuários cadastrados
- **Página Inicial**: Dashboard de boas-vindas
- **Admin Django**: Interface administrativa completa
- **Banco de Dados SQLite**: Persistência de dados local

## 📁 Estrutura do Projeto

```
app_cadastro_django/
├── app_cadastro/              # Projeto Django principal
│   ├── app/                   # Aplicação principal
│   │   ├── models.py          # Modelo de dados (Usuario)
│   │   ├── views.py           # Lógica de visualização
│   │   ├── admin.py           # Configuração do admin
│   │   ├── migrations/        # Migrações do banco de dados
│   │   └── templates/
│   │       └── users/
│   │           ├── home.html  # Página inicial
│   │           └── usuarios.html # Listagem de usuários
│   ├── app_cadastro/          # Configurações do projeto
│   │   ├── settings.py        # Configurações do Django
│   │   ├── urls.py            # Rotas principais
│   │   ├── wsgi.py            # WSGI para produção
│   │   └── asgi.py            # ASGI para async
│   ├── manage.py              # Utilitário de gerenciamento
│   └── db.sqlite3             # Banco de dados (gerado)
```

## 📋 Requisitos

- Python 3.8+
- Django 3.2+
- SQLite (incluído no Python)

## 🚀 Como Usar

### 1. Configuração Inicial

```bash
cd app_cadastro_django/app_cadastro
```

### 2. Instalar Dependências

```bash
pip install django
```

### 3. Aplicar Migrações

```bash
python manage.py migrate
```

### 4. Criar Superusuário (Admin)

```bash
python manage.py createsuperuser
# Siga as instruções para criar um usuário admin
```

### 5. Iniciar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://localhost:8000`

### 6. Acessar o Admin

Navegue para `http://localhost:8000/admin` e faça login com suas credenciais.

## 🗄️ Modelo de Dados

### Usuario

```python
class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nome = models.TextField(max_length=255)
    idade = models.IntegerField()
```

**Campos:**
- `id_usuario`: Identificador único (chave primária)
- `nome`: Nome do usuário (até 255 caracteres)
- `idade`: Idade do usuário (número inteiro)

## 🔗 Rotas Disponíveis

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial (home) |
| `/usuarios` | Listagem de todos os usuários |
| `/admin` | Painel administrativo |

## 📝 Templates HTML

### home.html
Página inicial da aplicação com boas-vindas e navegação.

### usuarios.html
Exibe uma tabela com todos os usuários cadastrados no banco de dados.

## 🛠️ Gerenciamento

### Criar um novo usuário pelo manage.py

```bash
python manage.py shell
>>> from app.models import Usuario
>>> usuario = Usuario.objects.create(nome="João Silva", idade=30)
>>> usuario.save()
```

### Listar todos os usuários

```bash
python manage.py shell
>>> from app.models import Usuario
>>> Usuario.objects.all()
```

### Deletar um usuário

```bash
python manage.py shell
>>> from app.models import Usuario
>>> usuario = Usuario.objects.get(id_usuario=1)
>>> usuario.delete()
```

## 📊 Migrações

As migrações já incluem:
- `0001_initial.py`: Criação inicial da tabela Usuario
- `0002_rename_usuarios_usuario.py`: Renomeação de tabela/campo

Para criar novas migrações após modificar models.py:

```bash
python manage.py makemigrations
python manage.py migrate
```

## 🔐 Configurações de Produção

Para implantar em produção, edite `app_cadastro/settings.py`:

```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']
SECRET_KEY = 'sua-chave-secreta-segura'
```

Use um banco de dados como PostgreSQL em vez de SQLite:

```bash
pip install psycopg2-binary
```

## 📚 Recursos Adicionais

- [Documentação Django](https://docs.djangoproject.com/)
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/models/)
- [Django Admin](https://docs.djangoproject.com/en/stable/ref/contrib/admin/)

## 💡 Próximas Melhorias

- [ ] Adicionar autenticação de usuários
- [ ] Implementar formulários de criação/edição
- [ ] Adicionar testes unitários
- [ ] Implementar paginação na listagem
- [ ] Adicionar validações de dados
