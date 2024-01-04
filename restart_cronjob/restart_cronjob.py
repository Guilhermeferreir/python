import time
import subprocess
import os
import kubernetes


def main():
    # Obter o contexto Kubernetes
    credentials = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    context = os.environ.get("KUBECONFIG_CONTEXT")
    # Criar um cliente do Kubernetes
    client = kubernetes.client.CoreV1Api(
        configuration=kubernetes.client.Configuration.from_config_file(credentials)
    )
    # Listar os pods
    pods = client.list_pods(context=context)

    # Imprimir os pods
    for pod in pods.items:
        print(pod.metadata.name)

    while True:
        # Substitua 'nome_do_cronjob' pelo nome do seu cronjob
        command = (
            "kubectl get cronjobs.batch -n "
            + namespace
            + "  "
            + nome_do_cronjob
            + " -o jsonpath='{.status.active[*].name}'"
        )
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        job_name = result.stdout.strip()

        if job_name:
            # Obtenha o nome do pod para o job ativo
            command = (
                "kubectl get pods -n "
                + namespace
                + " --selector=job-name="
                + job_name
                + " -o jsonpath='{.items[-1:].metadata.name}'"
            )
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            pod_name = result.stdout.strip()

            if pod_name:
                print(pod_name)
                command = "kubectl logs -n " + namespace + " --tail 1 " + pod_name
                result = subprocess.run(
                    command, shell=True, capture_output=True, text=True
                )
                new_last_line = result.stdout
                # print(new_last_line)
                # print(last_line)
                if not first_run:
                    if new_last_line == last_line:
                        print("A última linha é a mesma que a anterior.")
                        print("matando pod: " + pod_name)
                        command = "kubectl delete po -n " + namespace, pod_name
                        result = subprocess.run(
                            command, shell=True, capture_output=True, text=True
                        )
                    else:
                        print("A última linha mudou.")

                last_line = new_last_line
                first_run = False

            else:
                print("Nenhum pod encontrado para o job.")
        else:
            print("Nenhum job ativo encontrado para o cronjob.")
        # Aguarde 5 minutos
        time.sleep(300)


if __name__ == "__main__":
    last_line = None
    first_run = True
    nome_do_cronjob = ""
    namespace = ""
    main()