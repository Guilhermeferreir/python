from kubernetes import client, config
from datetime import datetime, timedelta, timezone
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Configuração da API do Kubernetes
config.load_kube_config()  # Carrega a configuração do arquivo kubeconfig padrão

# Configuração do cliente Slack
slack_token = ''
slack_channel = '#'  # Substitua pelo nome do canal do Slack onde deseja enviar a mensagem

slack_client = WebClient(token=slack_token)

# Função para calcular o MTBF
def calculate_mtbf():
    v1 = client.CoreV1Api()
    pods = v1.list_pod_for_all_namespaces(watch=False)
    restarts = 0
    uptime_total = timedelta(0)
    now = datetime.now(timezone.utc)
    for pod in pods.items:
        if pod.status.container_statuses:  # Verifica se container_statuses não é None, garante que seu código não tentará acessar índices em None, evitando o erro "TypeError: 'NoneType' object is not subscriptable"
            restarts += pod.status.container_statuses[0].restart_count
            # Convertendo o tempo de início do pod para um objeto datetime
            start_time = pod.status.start_time.replace(tzinfo=timezone.utc)
            uptime_total += (now - start_time)
    if restarts > 0:
        mtbf_seconds = uptime_total.total_seconds() / restarts
        mtbf_hours = mtbf_seconds / 3600
        print(f"MTBF: {mtbf_hours:.2f} horas")
        print(f"Uptime: {uptime_total.total_seconds()}")
        print(f"Restart: {restarts}")
        #send_to_slack(f"MTBF: {mtbf_hours:.2f} horas")
        send_to_slack("---------- MTBF Kubernetes -----------" "\n"
       f"Uptime: {uptime_total.total_seconds()}" "\n"
       f"Restart: {restarts}" "\n"
       f"MTBF: {mtbf_hours:.2f} horas"
       )
    else:
        print("Não foi possível calcular o MTBF, nenhum reinício detectado.")
        send_to_slack("Não foi possível calcular o MTBF, nenhum reinício detectado.")

# Função para enviar mensagem para o Slack
def send_to_slack(message):
    try:
        slack_client.chat_postMessage(channel=slack_channel, text=message)
        print("Mensagem enviada para o Slack com sucesso.")
    except SlackApiError as e:
        print(f"Erro ao enviar mensagem para o Slack: {e.response['error']}")

# Chamada da Função
calculate_mtbf()
