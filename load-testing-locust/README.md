# Load Testing - Locust

## 🚀 Descrição

**Load Testing Locust** é um projeto de teste de carga para validar a performance e estabilidade de uma API (especificamente uma API Unleash de feature flags). Utiliza **Locust**, uma ferramenta de teste de carga open-source que permite simular múltiplos usuários concorrentes acessando a aplicação.

## 🎯 Funcionalidades

- **Teste de Carga Distribuído**: Simula centenas de usuários simultâneos
- **Testes de API REST**: Requisições HTTP contra endpoints específicos
- **Obtenção de Features**: Busca lista de todas as feature flags
- **Busca Aleatória**: Seleciona features aleatoriamente para testes
- **Relatórios Detalhados**: Gera estatísticas de performance
- **Execução Headless**: Pode rodar sem interface gráfica

## 📁 Estrutura do Projeto

```
load-testing-locust/
├── locustfile.py              # Cenário de teste
├── documentation.md           # Documentação adicional
└── README.md                  # Este arquivo
```

## 📋 Requisitos

- Python 3.7+
- Locust 2.0+
- API Unleash acessível
- Kubectl (se rodar em container Kubernetes)

### Instalação de Dependências

```bash
pip install locust
```

## 🚀 Como Usar

### 1. Configurar a API

Edite `locustfile.py` e configure:

```python
API_KEY = "seu-token-aqui"  # Token da API Unleash
API_HEADER = {
    "Authorization": API_KEY
}

# Host da API
host = "http://seu-unleash-server:4242"
```

### 2. Executar Locust (Interface Gráfica)

```bash
locust -f locustfile.py
```

Acesse `http://localhost:8089` no navegador para iniciar o teste.

### 3. Executar Locust (Modo Headless)

```bash
# Comando básico (100 usuários, taxa de spawn 10 por segundo, 1 minuto)
locust -f locustfile.py --headless -u 100 -r 10 -t 1m

# Explicação dos parâmetros:
# -u 100    = 100 usuários simultâneos
# -r 10     = 10 novos usuários por segundo
# -t 1m     = Duração do teste (1 minuto)
```

### 4. Executar em Kubernetes (Container)

```bash
# Iniciar container interativo
kubectl run -i --tty --rm debug --image=alpine --restart=Never -- sh

# Dentro do container, instalar dependências
apk add python3 py3-pip gcc python3-dev musl-dev linux-headers
pip install locust

# Criar arquivo locustfile.py dentro do container
nano locustfile.py

# Executar o teste
locust -f locustfile.py --headless -u 100 -r 10
```

## 📝 Estrutura do Código

### Inicialização

```python
import random
from locust import HttpUser, TaskSet, task, between, constant

# Configurações
API_KEY = "*:development...."
API_HEADER = {
    "Authorization": API_KEY
}
```

### Classe TaskSet: `UserBehavior`

Define as ações que cada usuário simulado executará:

```python
class UserBehavior(TaskSet):
    GLOBAL_FEATURES = []  # Cache de features
    
    @task
    def get_all_flags(self):
        # Task 1: Buscar todas as features
        response = self.client.get("/api/client/features",
            headers=API_HEADER,
        )
        all_features_response = response.json()
        features = []
        for feature in all_features_response.get('features', []):
            features.append(feature["name"])
        self.GLOBAL_FEATURES = features

    @task
    def get_unique_flag(self):
        # Task 2: Buscar uma feature específica
        if len(self.GLOBAL_FEATURES) > 0:
            response = self.client.get(
                f"/api/client/features/{random.choice(self.GLOBAL_FEATURES)}",
                headers=API_HEADER
            )
```

### Classe HttpUser: `WebsiteUser`

Define o perfil de usuário:

```python
class WebsiteUser(HttpUser):
    tasks = [UserBehavior]           # Tarefas a executar
    wait_time = constant(1)          # Esperar 1 segundo entre requisições
    host = "http://unleash.unleash:4242"  # URL do servidor
```

## 📊 Parâmetros de Teste

### Usuários (-u)

```bash
locust -f locustfile.py -u 50  # 50 usuários
```

### Taxa de Spawn (-r)

```bash
locust -f locustfile.py -u 100 -r 5  # 5 usuários novos por segundo até 100
```

### Duração (-t)

```bash
locust -f locustfile.py -t 5m     # 5 minutos
locust -f locustfile.py -t 1h     # 1 hora
locust -f locustfile.py -t 30s    # 30 segundos
```

### Headless (--headless)

```bash
locust -f locustfile.py --headless  # Sem interface gráfica
```

## 📈 Interpretação de Resultados

Na interface web ou nos logs, você verá:

| Métrica | Significado |
|---------|------------|
| **Type** | Tipo de requisição (GET, POST, etc) |
| **Name** | Nome do endpoint |
| **# requests** | Total de requisições |
| **# fails** | Número de falhas |
| **Median** | Tempo mediano de resposta |
| **95%** | 95º percentil (95% das requisições respondem em menos tempo) |
| **99%** | 99º percentil |
| **Max** | Tempo máximo de resposta |
| **Min** | Tempo mínimo de resposta |
| **Avg** | Tempo médio de resposta |

## 🎯 Casos de Teste Comuns

### Teste de Smoke (Leve)
```bash
locust -f locustfile.py --headless -u 5 -r 1 -t 30s
```
- Valida que a API está respondendo
- Rápido e leve

### Teste de Carga (Moderado)
```bash
locust -f locustfile.py --headless -u 100 -r 10 -t 10m
```
- Simula carga típica
- Identifica gargalos

### Teste de Stress (Pesado)
```bash
locust -f locustfile.py --headless -u 500 -r 50 -t 30m
```
- Testa limite da aplicação
- Identifica quebras

### Teste de Resistência (Longa duração)
```bash
locust -f locustfile.py --headless -u 50 -r 5 -t 24h
```
- Verifica estabilidade
- Detecta memory leaks

## 🐳 Docker

Para rodar em um container:

```dockerfile
FROM python:3.9
RUN pip install locust
WORKDIR /app
COPY locustfile.py .
CMD ["locust", "-f", "locustfile.py", "--headless", "-u", "100", "-r", "10"]
```

Construir e executar:

```bash
docker build -t locust-test .
docker run locust-test
```

## 🔧 Configurações Avançadas

### Adicionar Wait Time Variável

```python
class WebsiteUser(HttpUser):
    wait_time = between(1, 3)  # Entre 1 e 3 segundos
```

### Adicionar Múltiplos Endpoints

```python
class UserBehavior(TaskSet):
    @task(2)  # Task com peso 2 (mais frequente)
    def task1(self):
        pass
    
    @task(1)  # Task com peso 1
    def task2(self):
        pass
```

### Adicionar Setup/Teardown

```python
class WebsiteUser(HttpUser):
    def on_start(self):
        # Executado quando usuário começa
        pass
    
    def on_stop(self):
        # Executado quando usuário termina
        pass
```

## 📋 Documentação Adicional

Consulte `documentation.md` para:
- Instruções de execução em Kubernetes
- Instalação de dependências em container
- Exemplos adicionais

## 🐛 Troubleshooting

### Erro: "Connection refused"
```bash
# Verificar se a API está acessível
curl http://seu-unleash-server:4242/health
```

### Erro: "Unauthorized"
```bash
# Verificar se o token está correto
# Consulte a documentação da API Unleash para gerar um novo token
```

### Erro: "Too many open files"
```bash
# Aumentar limite de file descriptors (Linux)
ulimit -n 10000
```

### Interface não aparece
```bash
# Certifique-se de que está acessando no navegador
# http://localhost:8089
# e não está usando --headless
```

## 📚 Documentação Oficial

- [Locust Documentation](https://docs.locust.io/)
- [Unleash Documentation](https://docs.getunleash.io/)
- [HTTP Protocol](https://developer.mozilla.org/en-US/docs/Web/HTTP)

## 💡 Próximas Melhorias

- [ ] Adicionar múltiplos cenários de teste
- [ ] Integrar com CI/CD
- [ ] Adicionar notificações em caso de falhas
- [ ] Dashboard de histórico
- [ ] Testes parametrizados
- [ ] Integração com Grafana/Prometheus

## 📝 Notas Importantes

⚠️ **Cuidado ao executar testes de carga em produção**
- Comunique com a equipe
- Execute em horários off-peak
- Comece com testes leves
- Aumente gradualmente a carga
