import requests
import os
import time
import json
import re

# --- CONFIGURAÇÃO ---

# Nome do arquivo contendo os IDs (um por linha)
IDS_FILE = "ids_guias.txt"

# Caminho completo para a pasta de saída dos arquivos TXT
# ATENÇÃO: SUBSTITUA '/media/udo-antonio-baingo/TOSHIBA EXT/MeusRecursosTrados/Trabalho_Final_HP/en-US/'
# PELA PARTE DO SEU CAMINHO QUE É COMUM A TODOS OS SEUS PROJETOS.
# O novo subdiretório 'Ultimos_Guias_HP' será criado dentro dele.
BASE_PROJECTS_DIR = "/media/udo-antonio-baingo/TOSHIBA EXT/MeusRecursosTrados/Trabalho_Final_HP/en-US/"
OUTPUT_DIR = os.path.join(BASE_PROJECTS_DIR, "Ultimos_Guias_HP") # NOVO DIRETÓRIO DE SAÍDA ATUALIZADO

# URL base da API da iFixit
API_BASE_URL = "https://www.ifixit.com/api/2.0/guides/"

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

# Garante que o diretório de saída exista
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- FUNÇÃO DE FILTRAGEM RECURSIVA ---

def extract_and_filter_text(data, extracted_texts):
    """
    Extrai strings de um dicionário/lista JSON recursivamente, aplicando filtros.
    Mantém o conteúdo 'raw' intacto, sem remover HTML ou Markdown.
    """
    if isinstance(data, dict):
        for key, value in data.items():
            # Regras de exclusão de chaves ou blocos completos
            if key == "prerequisites":
                # Ignora completamente o bloco de pré-requisitos
                continue
            if key in [
                "id", "guid", "mini", "thumbnail", "140x105", "200x150",
                "standard", "440x330", "medium", "large", "huge", "original",
                "rendered", # Para ignorar explicitamente as chaves _rendered
                "bullet", # Para ignorar os marcadores de bullet (black, red, image, etc.)
                "image", "media", "flags", "revision", "revisionid", "userid", "username",
                "modified", "can_edit", "documents", "tools", "parts",
                "workflow", "difficulty", "locale", "url", "type", "category",
                "topic", "summary", "keywords", "featured", "public",
                "published", "prereq_guides", "next_guide", "previous_guide",
                "compatibility", "device", "author", "solutions",
                "time_required", "documents", "related_guides",
                "solution_notes", "tools_raw", "parts_raw"
            ]:
                continue

            if isinstance(value, str):
                if value.strip():
                    if key.endswith('_rendered') or (key == 'summary' and 'prerequisites' in data.keys()):
                        continue
                    
                    extracted_texts.append(value.strip())
            elif isinstance(value, (dict, list)):
                extract_and_filter_text(value, extracted_texts)
    elif isinstance(data, list):
        for item in data:
    
            extract_and_filter_text(item, extracted_texts)

# --- LÓGICA DE DOWNLOAD E PROCESSAMENTO ---
print(f"Iniciando download de {len(guide_ids)} guias listados em '{IDS_FILE}' para '{OUTPUT_DIR}'...")

for guide_id in guide_ids:
    api_url = f"{API_BASE_URL}{guide_id}"
    
    output_filename_trados = os.path.join(OUTPUT_DIR, f"guide_{guide_id}.txt")

    if os.path.exists(output_filename_trados):
        print(f"Guia {guide_id} (TXT) já existe. Pulando.")
        continue

    try:
        print(f"Baixando guia {guide_id}...")
        response = requests.get(api_url)
        response.raise_for_status()

        guide_data = response.json()
        
        textos_filtrados = []
        extract_and_filter_text(guide_data, textos_filtrados) 

        final_text = "\n\n".join(textos_filtrados)

        with open(output_filename_trados, "w", encoding="utf-8") as f:
            f.write(final_text)

        print(f"Textos do guia {guide_id} salvos em '{output_filename_trados}' com sucesso.")

    except requests.exceptions.RequestException as e:
        print(f"Erro de requisição ao baixar guia {guide_id}: {e}")
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON para guia {guide_id}. Resposta inválida.")
    except Exception as e:
        print(f"Ocorreu um erro inesperado ao processar guia {guide_id}: {e}")

    time.sleep(0.5)

print("\nProcesso de download e extração concluído.")