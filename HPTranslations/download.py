import requests
import os
import time
import json

# --- CONFIGURAÇÃO ---

# Nome do arquivo contendo os IDs (um por linha)
IDS_FILE = "ids_guias.txt" # Assumindo que o arquivo está na mesma pasta do script

# Lista para armazenar os IDs lidos do arquivo
guide_ids = []
try:
    with open(IDS_FILE, "r", encoding="utf-8") as f:
        guide_ids = [line.strip() for line in f if line.strip()]
except FileNotFoundError:
    print(f"Erro: Arquivo de IDs '{IDS_FILE}' não encontrado.")
    exit()

if not guide_ids:
    print(f"Aviso: O arquivo '{IDS_FILE}' está vazio ou não contém IDs válidos.")
    exit()

# Substitua pelo caminho da pasta na sua partição do Windows montada no Ubuntu
# CERTIFIQUE-SE QUE ESTE CAMINHO ESTÁ CORRETO NO SEU AMBIENTE UBUNTU!
OUTPUT_DIR = "/media/seu_usuario/NomeDaSuaParticaoWindows/Usuarios/SeuUsuarioWindows/Documentos/TraducoesIFixit"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# URL base da API da iFixit para guias (VERIFIQUE A DOCUMENTAÇÃO OFICIAL)
API_BASE_URL = "https://www.ifixit.com/api/2.0/guides/"

# NÃO PRECISA DE HEADERS/CREDENCIAS AQUI SE A API FOR PÚBLICA PARA ESTE ENDPOINT


# --- LÓGICA DE DOWNLOAD ---
print(f"Iniciando download de {len(guide_ids)} guias listados em '{IDS_FILE}' para '{OUTPUT_DIR}'...")

for guide_id in guide_ids:
    api_url = f"{API_BASE_URL}{guide_id}"
    output_filename = os.path.join(OUTPUT_DIR, f"guide_{guide_id}.json")

    if os.path.exists(output_filename):
        print(f"Guia {guide_id} já existe. Pulando.")
        continue

    try:
        print(f"Baixando guia {guide_id}...")
        # Faz a requisição GET. REMOVIDO headers=HEADERS
        response = requests.get(api_url)

        response.raise_for_status()

        guide_data = response.json()

        with open(output_filename, "w", encoding="utf-8") as f:
            json.dump(guide_data, f, indent=4, ensure_ascii=False)

        print(f"Guia {guide_id} baixado e salvo com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao baixar guia {guide_id}: {e}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON para guia {guide_id}. Resposta inválida.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar guia {guide_id}: {e}")

    time.sleep(0.5) # Mantém a pausa para evitar rate limits

print("Processo de download concluído.")