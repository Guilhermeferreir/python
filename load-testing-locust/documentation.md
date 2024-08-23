## Testes executados no unleash de stage

### Como executar

#### Inciar container de teste
Garanta que o kubectl esteja no contexto correto

```bash
kubectl run -i --tty --rm debug --image=alpine --restart=Never -- sh
```

#### Instalar dependencias dentro do container
```bash
apk add curl
apk add nano
apk add python3
apk add py-pip
apk add build-base
apk add gcc python3-dev musl-dev linux-headers
```

#### Iniciar o ambiente de teste
```bash
python3 -m venv venv
source venv/bin/activate
pip install locust
```

- Copie o código do arquivo locustfile.py para um arquivo locustfile.py dentro do container
- Garanta que o baseURL esteja correto (http://namespace.service)
```bash
touch locustfile.py
nano locustfile.py
```

- Execute o locust
```bash
locust -f locustfile.py --headless -u 100 -r 10
```