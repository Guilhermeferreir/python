import xlsxwriter
from kubernetes import client, config
from datetime import datetime, timedelta, timezone

config.load_kube_config(

workbook = xlsxwriter.Workbook('mtbf_planilha.xlsx')
worksheet = workbook.add_worksheet("Minha Planilha")

worksheet.write('A1', 'Uptime')
worksheet.write('B1', 'restarts')
worksheet.write('C1', 'MTBF')


def calculate_mtbf():
    v1 = client.CoreV1Api()
    # Recuperar lista de pods em todos os namespaces
    pods = v1.list_pod_for_all_namespaces(watch=False)
    restarts = 0
    uptime_total = timedelta(0)
    now = datetime.now(timezone.utc)
    for pod in pods.items:
        restarts += pod.status.container_statuses[0].restart_count

        # Convertendo o tempo de início do pod para um objeto datetime
        start_time = pod.status.start_time.replace(tzinfo=timezone.utc)
        uptime_total += (now - start_time)
    if restarts > 0:
        mtbf_seconds = uptime_total.total_seconds() / restarts
        worksheet.write('A2', f"{mtbf_seconds}")
        worksheet.write('B2', f"${restarts}")
        mtbf_hours = mtbf_seconds / 3600
        worksheet.write('C2', f"${mtbf_hours}")
        #print(f"Uptime: {uptime_total()}")
        #print(f"Restart: {restarts}")
        #print(f"MTBF: {mtbf_hours:.2f} horas")
    else:
        print("Não foi possível calcular o MTBF, nenhum reinício detectado.")

calculate_mtbf()
workbook.close()

