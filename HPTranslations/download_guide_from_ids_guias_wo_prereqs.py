import requests
import os
import time
import json

# --- CONFIGURAÇÃO ---

# Nome do arquivo contendo os IDs (um por linha)
IDS_FILE = "ids_guias.txt"

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

OUTPUT_DIR = "/media/udobaingo/Antigo Drive/Trados/HPOriginGuides"
os.makedirs(OUTPUT_DIR, exist_ok=True)

API_BASE_URL = "https://www.ifixit.com/api/2.0/guides/"

def filtrar_dados_para_trados(guide_data): # Não precisamos mais do current_guide_id aqui
    textos_para_traducao = []

    def extrair_textos(data):
        if isinstance(data, dict):
            for chave, valor in data.items():
                
                # --- FILTRO PARA A CHAVE 'prerequisites' ---
                if chave == "prerequisites":
                    # Se encontrarmos a chave 'prerequisites', simplesmente ignoramos todo o seu conteúdo.
                    # Não chamamos extrair_textos para 'valor', pulando para a próxima chave.
                    continue 
                
                # Filtro para chaves que não queremos (ids, imagens, etc.)
                if chave not in ["id", "guid", "mini", "thumbnail", "140x105", "200x150", "standard", "440x330", "medium", "large", "huge", "original"] and isinstance(valor, str) and valor.strip():
                    textos_para_traducao.append(valor.strip())
                elif isinstance(valor, (dict, list)):
                    # Continua a recursão para outros dicionários ou listas
                    extrair_textos(valor) 
        elif isinstance(data, list):
            for item in data:
                extrair_textos(item)
    
    extrair_textos(guide_data)
    return "\n".join(textos_para_traducao)

# --- LÓGICA DE DOWNLOAD ---
print(f"Iniciando download de {len(guide_ids)} guias listados em '{IDS_FILE}' para '{OUTPUT_DIR}'...")

for guide_id in guide_ids:
    api_url = f"{API_BASE_URL}{guide_id}"
    
    output_filename_trados = os.path.join(OUTPUT_DIR, f"trados_guide_{guide_id}.txt")

    if os.path.exists(output_filename_trados):
        print(f"Guia {guide_id} (TXT) já existe. Pulando.")
        continue

    try:
        print(f"Baixando guia {guide_id}...")
        response = requests.get(api_url)
        response.raise_for_status()

        guide_data = response.json()
        # Não precisamos mais passar o guide_id para a função de filtro
        textos_filtrados = filtrar_dados_para_trados(guide_data) 

        with open(output_filename_trados, "w", encoding="utf-8") as f:
            f.write(textos_filtrados)

        print(f"Textos para tradução do guia {guide_id} salvos em '{output_filename_trados}' com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao baixar guia {guide_id}: {e}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON para guia {guide_id}. Resposta inválida.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar guia {guide_id}: {e}")

    time.sleep(0.5)

print("Processo de download concluído.")
