# Restart Cronjob

## 🔄 Descrição

**Restart Cronjob** é uma aplicação Python que automaticamente monitora e controla a execução de **Kubernetes Cronjobs**. O script verifica continuamente a execução de um cronjob específico, recupera logs e implementa lógica de reinicialização automática quando necessário.

## 🎯 Funcionalidades

- **Monitoramento de Cronjobs**: Observa cronjobs em execução em um namespace
- **Detecção de Jobs Ativos**: Identifica quando um job foi disparado
- **Recuperação de Logs**: Obtém os últimos logs do pod em execução
- **Reinicialização Automática**: Reinicia automaticamente em caso de falha (configurável)
- **Integração Kubernetes**: Usa a API nativa do Kubernetes
- **Monitoramento Contínuo**: Loop infinito verificando status

## 📁 Estrutura do Projeto

```
restart_cronjob/
└── restart_cronjob.py     # Script principal
```

## 📋 Requisitos

- Python 3.7+
- Kubernetes Client Python (`kubernetes`)
- Acesso a um cluster Kubernetes
- Credenciais do Google Cloud (opcional, para GKE)
- Arquivo `kubeconfig` configurado

### Instalação de Dependências

```bash
pip install kubernetes
```

## 🚀 Como Usar

### 1. Configurar Variáveis de Ambiente

```bash
# Google Cloud credentials (opcional)
export GOOGLE_APPLICATION_CREDENTIALS="/caminho/para/credentials.json"

# Contexto do Kubernetes
export KUBECONFIG_CONTEXT="seu-contexto"

# Ou configurar no script
```

### 2. Editar Configurações no Script

Abra `restart_cronjob.py` e configure:

```python
namespace = "seu-namespace"           # Namespace do cronjob
nome_do_cronjob = "seu-cronjob-name"  # Nome do cronjob
```

### 3. Executar o Script

```bash
python restart_cronjob.py
```

O script executará em loop infinito, verificando o status do cronjob a cada intervalo.

### 4. Parar o Script

```bash
Ctrl + C
```

## 📝 Estrutura do Código

### Inicialização

```python
import time
import subprocess
import os
import kubernetes

def main():
    # Obter contexto Kubernetes
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    context = os.environ.get("KUBECONFIG_CONTEXT")
    
    # Criar cliente do Kubernetes
    client = kubernetes.client.CoreV1Api(
        configuration=kubernetes.client.Configuration.from_config_file(credentials)
    )
```

### Listar Pods

```python
# Listar todos os pods
pods = client.list_pods(context=context)

for pod in pods.items:
    print(pod.metadata.name)
```

### Obter Job Ativo

```python
# Comando para obter nome do job ativo
command = (
    "kubectl get cronjobs.batch -n " + namespace +
    " " + nome_do_cronjob +
    " -o jsonpath='{.status.active[*].name}'"
)
result = subprocess.run(command, shell=True, capture_output=True, text=True)
job_name = result.stdout.strip()

if job_name:
    print(f"Job ativo encontrado: {job_name}")
```

### Obter Pod do Job

```python
# Obter pod associado ao job
command = (
    "kubectl get pods -n " + namespace +
    " --selector=job-name=" + job_name +
    " -o jsonpath='{.items[-1:].metadata.name}'"
)
result = subprocess.run(command, shell=True, capture_output=True, text=True)
pod_name = result.stdout.strip()

if pod_name:
    print(f"Pod encontrado: {pod_name}")
```

### Recuperar Logs

```python
# Obter últimas linhas de log
command = "kubectl logs -n " + namespace + " --tail 1 " + pod_name
result = subprocess.run(command, shell=True, capture_output=True, text=True)
log_output = result.stdout

print(f"Logs: {log_output}")
```

## 🔄 Fluxo de Operação

```
1. Script inicia em loop infinito
   ↓
2. Verifica cronjob: kubectl get cronjobs
   ↓
3. Encontrou job ativo?
   ├─ SIM: Vai para passo 4
   └─ NÃO: Aguarda e volta ao passo 2
   ↓
4. Obtém nome do pod: kubectl get pods
   ↓
5. Recupera logs: kubectl logs
   ↓
6. Analisa logs (verificar sucesso/erro)
   ↓
7. Se erro detectado: Reinicia o job
   ↓
8. Aguarda próxima execução
   ↓
9. Volta ao passo 2
```

## 🛠️ Configuração Avançada

### Customizar Intervalo de Verificação

```python
import time

# Verificar a cada 30 segundos
while True:
    # ... lógica de verificação
    time.sleep(30)  # Aguardar 30 segundos
```

### Adicionar Reinicialização Automática

```python
def restart_job(namespace, job_name):
    command = f"kubectl delete job -n {namespace} {job_name}"
    subprocess.run(command, shell=True)
    
    # Aguardar a próxima execução do cronjob
    time.sleep(10)

# Chamar quando detectar erro
if error_detected:
    restart_job(namespace, job_name)
```

### Adicionar Notificações

```python
import smtplib
from email.mime.text import MIMEText

def enviar_alerta(assunto, mensagem):
    sender = "seu-email@gmail.com"
    recipients = ["admin@example.com"]
    
    msg = MIMEText(mensagem)
    msg["Subject"] = assunto
    msg["From"] = sender
    msg["To"] = ", ".join(recipients)
    
    with smtplib.SMTP("smtp.gmail.com", 587) as server:
        server.starttls()
        server.login(sender, "sua-senha")
        server.sendmail(sender, recipients, msg.as_string())

# Chamar quando detectar erro
if error_detected:
    enviar_alerta("Cronjob Falhou", f"O cronjob {nome_do_cronjob} falhou")
```

## 📊 Exemplo Completo

```python
import time
import subprocess
import os

namespace = "default"
nome_do_cronjob = "meu-cronjob"

while True:
    try:
        # Verificar jobs ativos
        command = (
            f"kubectl get cronjobs.batch -n {namespace} {nome_do_cronjob} "
            f"-o jsonpath='{{.status.active[*].name}}'"
        )
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        job_name = result.stdout.strip()
        
        if job_name:
            print(f"[{time.strftime('%H:%M:%S')}] Job ativo: {job_name}")
            
            # Obter pod
            command = (
                f"kubectl get pods -n {namespace} "
                f"--selector=job-name={job_name} "
                f"-o jsonpath='{{.items[-1:].metadata.name}}'"
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            pod_name = result.stdout.strip()
            
            if pod_name:
                # Obter logs
                command = f"kubectl logs -n {namespace} --tail 1 {pod_name}"
                result = subprocess.run(command, shell=True, capture_output=True, text=True)
                print(f"[{time.strftime('%H:%M:%S')}] Logs: {result.stdout}")
        else:
            print(f"[{time.strftime('%H:%M:%S')}] Nenhum job ativo no momento")
        
        # Verificar a cada 60 segundos
        time.sleep(60)
        
    except Exception as e:
        print(f"[{time.strftime('%H:%M:%S')}] Erro: {e}")
        time.sleep(60)
```

## 📋 Comando kubectl Utilizados

| Comando | Descrição |
|---------|-----------|
| `kubectl get cronjobs.batch` | Lista cronjobs |
| `kubectl get pods` | Lista pods |
| `kubectl logs` | Mostra logs do pod |
| `kubectl delete job` | Deleta um job (para reiniciar) |
| `kubectl describe pod` | Mostra detalhes do pod |

## 🔐 Configuração de Segurança

### Via kubeconfig

```bash
export KUBECONFIG=/caminho/para/kubeconfig
python restart_cronjob.py
```

### Via Service Account (em cluster)

```python
from kubernetes import client, config

# Carregar configuração dentro do cluster
config.load_incluster_config()
```

### RBAC Permissions Necessárias

```yaml
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: cronjob-monitor
rules:
- apiGroups: ["batch"]
  resources: ["cronjobs"]
  verbs: ["get", "list", "watch"]
- apiGroups: ["batch"]
  resources: ["jobs"]
  verbs: ["get", "list", "delete"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list"]
- apiGroups: [""]
  resources: ["pods/log"]
  verbs: ["get"]
```

## 🐛 Troubleshooting

### Erro: "kubeconfig not found"
```bash
# Verificar arquivo kubeconfig
cat $HOME/.kube/config

# Ou definir explicitamente
export KUBECONFIG=/caminho/para/kubeconfig
```

### Erro: "Connection refused"
```bash
# Verificar contexto do kubectl
kubectl config current-context

# Testar conexão
kubectl get pods
```

### Erro: "Permission denied"
```bash
# Verificar permissões RBAC
kubectl auth can-i get cronjobs --as=system:serviceaccount:default:default

# Criar binding RBAC apropriado
```

### Script não detecta jobs
```bash
# Verificar se cronjob existe
kubectl get cronjobs -n seu-namespace

# Verificar se algum job foi executado
kubectl get jobs -n seu-namespace

# Verificar status do cronjob
kubectl describe cronjob seu-cronjob -n seu-namespace
```

## 📚 Documentação Oficial

- [Kubernetes Cronjobs](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/)
- [Kubernetes Python Client](https://github.com/kubernetes-client/python)
- [kubectl Reference](https://kubernetes.io/docs/reference/kubectl/)

## 💡 Próximas Melhorias

- [ ] Adicionar parsing mais robusto de logs
- [ ] Implementar sistema de alertas (Slack, Email)
- [ ] Adicionar histórico de execuções
- [ ] Dashboard de monitoramento
- [ ] Suporte a múltiplos cronjobs
- [ ] Configuração via arquivo YAML
- [ ] Retry automático com backoff exponencial
- [ ] Testes automatizados
