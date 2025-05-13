import requests
from bs4 import BeautifulSoup

def preparar_pagina_dispositivo(url, output_filename):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        conteudo_traduzivel = []

        # Extrair Background
        background_heading = soup.find('h2', string='Background')
        if background_heading:
            conteudo_traduzivel.append(f"## Background ##\n")
            for sibling in background_heading.find_next_siblings():
                if sibling.name == 'h2':
                    break
                if sibling.name == 'p':
                    conteudo_traduzivel.append(sibling.get_text(strip=True) + "\n")
                elif sibling.name == 'div' and 'grid' in sibling.get('class', []):
                    for text in sibling.stripped_strings:
                        conteudo_traduzivel.append(text + "\n")

        # Extrair Identification
        identification_heading = soup.find('h2', string='Identification')
        if identification_heading:
            conteudo_traduzivel.append(f"\n## Identification ##\n")
            for sibling in identification_heading.find_next_siblings():
                if sibling.name == 'h2':
                    break
                if sibling.name == 'p':
                    conteudo_traduzivel.append(sibling.get_text(strip=True) + "\n")
                elif sibling.name == 'div' and 'grid' in sibling.get('class', []):
                    for text in sibling.stripped_strings:
                        conteudo_traduzivel.append(text + "\n")
                elif sibling.name == 'ul':
                    for li in sibling.find_all('li'):
                        conteudo_traduzivel.append(li.get_text(strip=True) + "\n")

        # Extrair Technical Specifications
        technical_specifications_heading = soup.find('h2', string='Technical Specifications')
        if technical_specifications_heading:
            conteudo_traduzivel.append(f"\n## Technical Specifications ##\n")
            next_element = technical_specifications_heading.find_next_sibling()
            while next_element and next_element.name != 'h2':
                if next_element.name in ['h3', 'p']:
                    conteudo_traduzivel.append(next_element.get_text(strip=True) + "\n")
                elif next_element.name == 'ul':
                    for li in next_element.find_all('li'):
                        conteudo_traduzivel.append("* " + li.get_text(strip=True) + "\n")
                elif next_element.name == 'dl':
                    for dt in next_element.find_all('dt'):
                        conteudo_traduzivel.append(dt.get_text(strip=True) + ": ")
                        dd = dt.find_next_sibling('dd')
                        if dd:
                            conteudo_traduzivel.append(dd.get_text(strip=True) + "\n")
                next_element = next_element.find_next_sibling()

        texto_final = "".join(conteudo_traduzivel).strip()

        with open(output_filename, 'w', encoding='utf-8') as f:
            f.write(texto_final)

        print(f"Conteúdo traduzível de '{url}' extraído e salvo em '{output_filename}'")

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar '{url}': {e}")
    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# URL da página em português
url_pt = "https://pt.ifixit.com/Device/HP_EliteBook_840_G9"
output_file = "hp_elitebook_840_g9_pt.txt"

preparar_pagina_dispositivo(url_pt, output_file)