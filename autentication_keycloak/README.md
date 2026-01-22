# Autenticação Keycloak

## 🔐 Descrição

**Autenticação Keycloak** é uma aplicação Flask que implementa autenticação e autorização usando **Keycloak**, um servidor de identidade e gerenciamento de acesso de código aberto. O projeto utiliza o protocolo **OpenID Connect (OIDC)** para autenticar usuários.

## 🎯 Funcionalidades

- **Login com Keycloak**: Autenticação centralizada via OpenID Connect
- **Logout**: Finalização segura de sessão
- **Obtenção de Informações do Usuário**: Recuperação de dados do perfil (username, email, ID único)
- **Token de Acesso**: Geração e manipulação de tokens JWT
- **Proteção de Rotas**: Controle de acesso com `@oidc.require_login`

## 📋 Requisitos

- Python 3.7+
- Flask 1.0+
- Flask-OIDC
- Keycloak Server (instalado e configurado)

### Instalação de Dependências

```bash
pip install flask flask-oidc
```

## 🔧 Configuração

### 1. Instalar Keycloak

Use o script fornecido:

```bash
bash package_install.sh
```

Ou siga a [documentação oficial do Keycloak](https://www.keycloak.org/guides).

### 2. Configurar Arquivo keycloak.json

Este arquivo contém as credenciais do cliente Keycloak:

```json
{
  "realm": "seu-realm",
  "auth-server-url": "http://seu-keycloak-server:8080/auth",
  "ssl-required": "external",
  "resource": "seu-client-id",
  "credentials": {
    "secret": "sua-secret"
  },
  "public-client": false
}
```

**Obter valores:**
1. Acesse o Keycloak Admin Console
2. Navegue até seu Realm
3. Vá para Clients e crie/selecione um cliente
4. Copie as credenciais

### 3. Configurar app.py

Edite as configurações no arquivo:

```python
app.config.update(
    SECRET_KEY='sua-chave-secreta-segura',  # Gere uma chave forte
    OIDC_CLIENT_SECRETS='keycloak.json',     # Caminho do arquivo JSON
    OIDC_INTROSPECTION_AUTH_METHOD='client_secret_post',
    OIDC_TOKEN_TYPE_HINT='access_token',
    OIDC_SCOPES=['openid', 'email', 'profile'],
    OIDC_OPENID_REALM='seu-realm-keycloak'   # Seu realm
)
```

## 🚀 Como Usar

### 1. Iniciar a Aplicação

```bash
python app.py
```

Por padrão, a aplicação roda em `http://localhost:5000`

### 2. Acessar Rotas

| Rota | Descrição |
|------|-----------|
| `/` | Página inicial (verifica se usuário está logado) |
| `/login` | Faz login com Keycloak e exibe token e username |
| `/logout` | Faz logout e redireciona |

### 3. Testar Autenticação

1. Acesse `http://localhost:5000/`
   - Se não autenticado: mostra "Not logged in"
   - Se autenticado: mostra "Welcome [username]"

2. Clique para fazer login via `/login`
   - Será redirecionado para Keycloak
   - Após autenticar, verá seu token e username

3. Acesse `/logout` para finalizar

## 📝 Estrutura do Código

### Inicialização
```python
from flask import Flask, g
from flask_oidc import OpenIDConnect

app = Flask(__name__)
app.config.update(...)  # Configurações OIDC
oidc = OpenIDConnect(app)
```

### Rota Index (/)
```python
@app.route('/')
def index():
    if oidc.user_loggedin:
        info = oidc.user_getinfo(["preferred_username", "email", "sub"])
        return 'Welcome %s' % info.get("preferred_username")
    else:
        return '<h1>Not logged in</h1>'
```

### Rota Protegida (/login)
```python
@app.route('/login')
@oidc.require_login  # Decorator que força login
def login():
    token = oidc.get_access_token()
    info = oidc.user_getinfo(["preferred_username", "email", "sub"])
    username = info.get("preferred_username")
    return "Token: " + token + "<br/><br/>  Username: " + username
```

### Rota Logout (/logout)
```python
@app.route('/logout')
def logout():
    oidc.logout()
    return '<h2>Hi, you have been logged out! <a href="/">Return</a></h2>'
```

## 🐳 Docker

Uma imagem Docker está incluída para facilitar a implantação:

```bash
docker build -t auth-keycloak .
docker run -p 5000:5000 auth-keycloak
```

## 🔐 Informações de Usuário Disponíveis

O Keycloak fornece as seguintes informações (via OIDC scopes):

| Campo | Descricao | Scope |
|-------|-----------|-------|
| `preferred_username` | Nome de usuário | openid |
| `email` | Email | email |
| `sub` | ID único do usuário | openid |
| `name` | Nome completo | profile |
| `given_name` | Primeiro nome | profile |
| `family_name` | Sobrenome | profile |
| `email_verified` | Email verificado | email |

Para obter mais campos, adicione scopes em `OIDC_SCOPES`.

## 🛠️ Troubleshooting

### Erro: "OIDC client not configured"
- Verifique se `keycloak.json` existe e tem permissões de leitura
- Confirme o caminho em `OIDC_CLIENT_SECRETS`

### Erro: "Connection refused"
- Confirme que o Keycloak está rodando
- Verifique a URL do servidor em `keycloak.json`

### Erro: "Invalid redirect_uri"
- Adicione `http://localhost:5000/oidc/callback` nas configurações do cliente no Keycloak
- Em Keycloak Admin Console → Clients → Seu Cliente → Valid Redirect URIs

### Erro: "Token expired"
- Implemente refresh token para renovar automaticamente
- Consulte documentação do Flask-OIDC

## 📚 Documentação Oficial

- [Keycloak Documentation](https://www.keycloak.org/documentation)
- [OpenID Connect](https://openid.net/connect/)
- [Flask-OIDC](https://github.com/puittenbroek/flask-oidc)

## 🔒 Segurança

- ✅ Use HTTPS em produção (não HTTP)
- ✅ Mantenha `SECRET_KEY` segura e única
- ✅ Nunca cometa `keycloak.json` no repositório
- ✅ Use variáveis de ambiente para credenciais sensíveis
- ✅ Implemente CSRF protection

## 💡 Próximas Melhorias

- [ ] Implementar refresh token
- [ ] Adicionar autorização baseada em roles
- [ ] Implementar middleware de autenticação reutilizável
- [ ] Adicionar testes automatizados
- [ ] Configurar HTTPS
