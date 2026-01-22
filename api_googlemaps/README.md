# API Google Maps

## 📍 Descrição

Este projeto é uma aplicação Python que utiliza a **API Google Maps** para obter informações de localização geográfica. O script permite recuperar dados de endereços como coordenadas de latitude e longitude, bem como o endereço formatado.

## 🎯 Funcionalidades

- **Geocodificação de Endereços**: Converte um endereço textual em coordenadas geográficas (latitude e longitude)
- **Formatação de Endereços**: Retorna o endereço em formato padronizado fornecido pelo Google
- **Tratamento de Erros**: Implementa verificação de resultados e tratamento de exceções

## 📋 Requisitos

- Python 3.7+
- Biblioteca `googlemaps`

### Instalação de Dependências

```bash
pip install googlemaps
```

## 🚀 Como Usar

### 1. Obter uma Chave de API do Google Maps

1. Acesse [Google Cloud Console](https://console.cloud.google.com/)
2. Crie um novo projeto
3. Ative a API "Maps SDK for Python"
4. Gere uma chave de API
5. Configure o faturamento (se necessário)

### 2. Configurar o Script

Abra o arquivo `app.py` e preencha os campos:

```python
if __name__ == "__main__":
    key_api = 'SUA_CHAVE_API_AQUI'  # Cole sua chave de API
    address = 'Endereço que deseja buscar'  # Digite o endereço
    get_details_Local(key_api, address)
```

### 3. Executar o Script

```bash
python app.py
```

## 📊 Saída Esperada

O script imprimirá:

```
name: Endereço Formatado
Latitude: -23.5505
Longitude: -46.6333
```

## 🔧 Estrutura do Código

### Função Principal: `get_details_Local(api_key, address)`

**Parâmetros:**
- `api_key` (str): Chave de autenticação da API Google Maps
- `address` (str): Endereço a ser geocodificado

**Retorno:** Imprime os dados de localização no console

**Processo:**
1. Inicializa cliente do Google Maps com a chave de API
2. Realiza geocodificação do endereço fornecido
3. Extrai latitude, longitude e endereço formatado
4. Imprime os resultados
5. Trata erros de requisição ou endereço não encontrado

## ⚠️ Tratamento de Erros

O script inclui tratamento para:
- Endereços não encontrados
- Erros de conexão com a API
- Respostas vazias da API

## 💡 Exemplos de Uso

### Buscar coordenadas de uma rua

```python
get_details_Local(api_key, "Av. Paulista, São Paulo, Brasil")
```

### Buscar coordenadas de um estabelecimento

```python
get_details_Local(api_key, "Estádio do Morumbi, São Paulo")
```

## 📚 Documentação Oficial

- [Google Maps API Documentation](https://developers.google.com/maps)
- [Python Client Library](https://github.com/googlemaps/google-maps-services-python)

## 🔐 Segurança

⚠️ **Importante**: Nunca cometa sua chave de API no repositório. Use variáveis de ambiente:

```python
import os
key_api = os.environ.get('GOOGLE_MAPS_API_KEY')
```

## 📝 Licença

Este projeto é fornecido como exemplo educacional.
