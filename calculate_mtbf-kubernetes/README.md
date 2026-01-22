# Calculate MTBF - Kubernetes

## 📊 Descrição

**Calculate MTBF Kubernetes** é uma aplicação Python que calcula o **MTBF (Mean Time Between Failures)** de pods em um cluster Kubernetes. O MTBF é uma métrica fundamental para medir a confiabilidade e disponibilidade dos serviços, representando o tempo médio entre falhas.

## 🎯 Funcionalidades

- **Coleta de Dados de Pods**: Recupera informações de todos os pods no cluster Kubernetes
- **Cálculo de MTBF**: Calcula o tempo médio entre reinicializações
- **Geração de Relatório**: Exporta os resultados em planilha Excel
- **Análise de Uptime**: Calcula o tempo total de funcionamento dos pods
- **Contagem de Reinicializações**: Registra o número de restarts dos containers

## 📁 Estrutura do Projeto

```
calculate_mtbf-kubernetes/
├── generate_xlsxWriter/
│   ├── app.py                 # Script principal
│   └── mtbf_planilha.xlsx     # Arquivo Excel gerado
└── send_slack/
    └── app.py                 # (Futuro) Envio de notificações
```

## 📋 Requisitos

- Python 3.7+
- Kubernetes Client Python (`kubernetes`)
- XlsxWriter
- Acesso a um cluster Kubernetes
- Configuração de `kubeconfig` correta

### Instalação de Dependências

```bash
pip install kubernetes xlsxwriter
```

## 🚀 Como Usar

### 1. Configurar Acesso ao Kubernetes

Certifique-se de que sua configuração kubeconfig está pronta:

```bash
# Verificar contexto
kubectl config current-context

# Listar contextos disponíveis
kubectl config get-contexts

# Definir contexto
kubectl config use-context seu-contexto
```

### 2. Executar o Script

```bash
cd calculate_mtbf-kubernetes/generate_xlsxWriter
python app.py
```

### 3. Arquivo Gerado

Um arquivo `mtbf_planilha.xlsx` será criado com as seguintes colunas:

| Coluna | Descrição |
|--------|-----------|
| **Uptime** | Tempo total de funcionamento em segundos |
| **restarts** | Número total de reinicializações |
| **MTBF** | Tempo médio entre falhas em horas |

## 📝 Estrutura do Código

### Inicialização

```python
import xlsxwriter
from kubernetes import client, config
from datetime import datetime, timedelta, timezone

# Carregar configuração do kubeconfig
config.load_kube_config()

# Criar workbook
workbook = xlsxwriter.Workbook('mtbf_planilha.xlsx')
worksheet = workbook.add_worksheet("Minha Planilha")
```

### Cabeçalhos da Planilha

```python
worksheet.write('A1', 'Uptime')
worksheet.write('B1', 'restarts')
worksheet.write('C1', 'MTBF')
```

### Função de Cálculo: `calculate_mtbf()`

```python
def calculate_mtbf():
    v1 = client.CoreV1Api()
    
    # Recuperar lista de pods em TODOS os namespaces
    pods = v1.list_pod_for_all_namespaces(watch=False)
    
    restarts = 0
    uptime_total = timedelta(0)
    now = datetime.now(timezone.utc)
    
    # Iterar sobre cada pod
    for pod in pods.items:
        # Contar reinicializações do primeiro container
        restarts += pod.status.container_statuses[0].restart_count
        
        # Calcular uptime
        start_time = pod.status.start_time.replace(tzinfo=timezone.utc)
        uptime_total += (now - start_time)
    
    # Calcular MTBF
    if restarts > 0:
        mtbf_seconds = uptime_total.total_seconds() / restarts
        mtbf_hours = mtbf_seconds / 3600
        
        # Escrever na planilha
        worksheet.write('A2', f"{mtbf_seconds}")
        worksheet.write('B2', f"${restarts}")
        worksheet.write('C2', f"${mtbf_hours}")
    else:
        print("Não foi possível calcular o MTBF, nenhum reinício detectado.")

calculate_mtbf()
workbook.close()
```

## 📊 Interpretação dos Resultados

### MTBF Alto = Bom ✅
- Indica que o serviço está estável
- Poucos reinicializações
- Exemplo: MTBF = 500 horas significa que em média há uma falha a cada 500 horas

### MTBF Baixo = Problema ⚠️
- Indica que o serviço está instável
- Muitos reinicializações
- Exemplo: MTBF = 2 horas significa que há uma falha a cada 2 horas

### Fórmula

$$\text{MTBF} = \frac{\text{Tempo Total de Funcionamento}}{\text{Número de Reinicializações}}$$

## 🔍 Exemplos de Cálculo

**Cenário 1: Serviço Estável**
- Uptime Total: 7200 segundos (2 horas)
- Reinicializações: 1
- MTBF: 7200 / 1 = 7200 segundos = 2 horas

**Cenário 2: Serviço Instável**
- Uptime Total: 36000 segundos (10 horas)
- Reinicializações: 10
- MTBF: 36000 / 10 = 3600 segundos = 1 hora

## 🛠️ Configurações Avançadas

### Analisar Namespace Específico

Modifique o script para analisar apenas um namespace:

```python
def calculate_mtbf(namespace='default'):
    v1 = client.CoreV1Api()
    
    # Recuperar pods de um namespace específico
    pods = v1.list_namespaced_pod(namespace)
    
    # ... resto do código
```

### Analisar Múltiplos Containers

Se um pod tem múltiplos containers:

```python
# Contar todos os restarts
for container_status in pod.status.container_statuses:
    restarts += container_status.restart_count
```

### Filtrar por Labels

```python
# Recuperar pods com label específico
pods = v1.list_pod_for_all_namespaces(label_selector="app=meuapp")
```

## 🐛 Troubleshooting

### Erro: "Unable to read config file"
```bash
# Verificar se kubeconfig existe
cat $HOME/.kube/config

# Ou especificar explicitamente
export KUBECONFIG=/caminho/para/kubeconfig
```

### Erro: "No container statuses"
- Alguns pods podem estar em estado inicial
- Adicione verificação:
```python
if pod.status.container_statuses:
    restarts += pod.status.container_statuses[0].restart_count
```

### Erro: "Connection refused"
- Verifique se o cluster está acessível
- Teste com: `kubectl get nodes`

## 📈 Monitoramento Contínuo

Para executar periodicamente:

### Com cron (Linux/Mac)

```bash
# Executar a cada hora
0 * * * * cd /caminho/para/projeto && python calculate_mtbf-kubernetes/generate_xlsxWriter/app.py
```

### Com script wrapper

```bash
#!/bin/bash
while true; do
    python app.py
    sleep 3600  # Aguardar 1 hora
done
```

## 📚 Documentação Oficial

- [Kubernetes Python Client](https://github.com/kubernetes-client/python)
- [XlsxWriter Documentation](https://xlsxwriter.readthedocs.io/)
- [Kubernetes API Reference](https://kubernetes.io/docs/concepts/overview/kubernetes-api/)

## 🔐 Segurança

- ✅ Use RBAC para limitar permissões
- ✅ Não comita kubeconfig no repositório
- ✅ Use service accounts com permissões mínimas
- ✅ Armazene credenciais em secrets

## 💡 Próximas Melhorias

- [ ] Integração com Slack (usar send_slack/)
- [ ] Dashboard web para visualizar métricas
- [ ] Histórico de MTBF ao longo do tempo
- [ ] Alertas automáticos quando MTBF cai
- [ ] Análise por namespace
- [ ] Análise por pod individual
