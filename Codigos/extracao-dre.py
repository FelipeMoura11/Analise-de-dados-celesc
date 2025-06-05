import os
import re
import pdfplumber
import pandas as pd
import logging

# Configuração básica de logs
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

PASTA_PDFS = r'C:\Users\User2025\Desktop\CASE\pdfs'
PASTA_SAIDA = r'C:\Users\User2025\Desktop\CASE\output'
ARQUIVO_DADOS = os.path.join(PASTA_SAIDA, 'receita_liquida.csv')

def extrair_periodo(nome_arquivo):
    nome = nome_arquivo.lower()

    # Caso 1: padrão 1t20, 2t19 etc.
    match = re.search(r'(\d)t(\d{2})', nome)
    if match:
        return f"{match.group(1).upper()}T{match.group(2)}"

    # Caso 2: padrões como 1itr2020, 1tri2020, 1tr2020
    match = re.search(r'(\d)[a-z]{2,3}(\d{4})', nome)
    if match:
        trimestre = match.group(1)
        ano = match.group(2)[-2:]
        return f"{trimestre}T{ano}"

    # Caso 3: padrão tipo '2_itr_2020' ou '2-itr-2020' ou '2.itr.2020'
    match = re.search(r'(\d)[_\-\.]?[a-z]{2,3}[_\-\.]?(\d{4})', nome)
    if match:
        trimestre = match.group(1)
        ano = match.group(2)[-2:]
        return f"{trimestre}T{ano}"

    # Caso 4: padrão tipo '202019' (6 dígitos)
    # Aqui o trimestre é o quarto dígito e o ano os dois últimos
    match = re.search(r'(\d{6})', nome)
    if match:
        num = match.group(1)
        trimestre = num[3]
        ano = num[4:6]
        if trimestre.isdigit():
            return f"{trimestre}T{ano}"

    return 'Desconhecido'


def extrair_receita_liquida(pdf_path):
    periodo = extrair_periodo(os.path.basename(pdf_path))
    dados = []

    with pdfplumber.open(pdf_path) as pdf:
        total_paginas = len(pdf.pages)

        pagina_dfs = None
        for i in range(total_paginas):
            texto = pdf.pages[i].extract_text()
            if texto:
                logging.info(f"Página {i+1} texto (primeiros 200 chars): {texto[:200].replace(chr(10), ' ')}")
                if 'dfs consolidadas' in texto.lower():
                    pagina_dfs = i
                    logging.info(f"✅ Página 'DFs Consolidadas' encontrada: {pagina_dfs + 1}")
                    break
        if pagina_dfs is None:
            logging.warning(f"⚠️ 'DFs Consolidadas' não encontrado no arquivo {os.path.basename(pdf_path)}")
            return dados

        pagina_dre = None
        for i in range(pagina_dfs, total_paginas):
            texto = pdf.pages[i].extract_text()
            if texto and 'demonstração do resultado' in texto.lower():
                pagina_dre = i
                logging.info(f"✅ Página 'Demonstração do Resultado' encontrada: {pagina_dre + 1}")
                break
        if pagina_dre is None:
            logging.warning(f"⚠️ 'Demonstração do Resultado' não encontrado após 'DFs Consolidadas' no arquivo {os.path.basename(pdf_path)}")
            return dados

        for i in range(pagina_dre, total_paginas):
            pagina = pdf.pages[i]
            texto = pagina.extract_text()
            if texto and '3.11' in texto and ('lucro' in texto.lower() or 'prejuízo' in texto.lower()):
                logging.info(f"✅ Página com '3.11 Lucro/Prejuízo' encontrada: {i + 1}")

                pattern = r'3\.11.*?[-+]?\d[\d\.\,]*'
                matches = re.findall(pattern, texto, re.IGNORECASE)
                if matches:
                    for match in matches:
                        logging.info(f"Encontrado trecho: {match}")
                        valor_str = re.findall(r'[-+]?\d[\d\.\,]*', match)
                        if valor_str:
                            valor_str = valor_str[-1]  # pegar o último número na linha
                            try:
                                valor = float(valor_str.replace('.', '').replace(',', '.'))
                                dados.append({
                                    'Conta': 'Lucro/Prejuízo Consolidado',
                                    'Valor': valor,
                                    'Período': periodo
                                })
                                logging.info(f"➡️ Valor encontrado: {valor} para o período {periodo}")
                                return dados
                            except Exception as e:
                                logging.error(f"Erro ao converter valor: {valor_str} - {e}")
                else:
                    logging.warning(f"⚠️ Valor '3.11 Lucro/Prejuízo' não encontrado no texto da página {i+1}")

        logging.warning(f"⚠️ Valor '3.11 Lucro/Prejuízo' não encontrado no arquivo {os.path.basename(pdf_path)}")
    return dados

def processar_todos_pdfs(pasta_pdfs):
    todos_dados = []
    arquivos = [f for f in os.listdir(pasta_pdfs) if f.lower().endswith('.pdf')]
    logging.info(f"➡️ {len(arquivos)} arquivos encontrados na pasta '{pasta_pdfs}'.")

    for arquivo in arquivos:
        caminho_pdf = os.path.join(pasta_pdfs, arquivo)
        logging.info(f"Processando arquivo: {arquivo}")
        dados_pdf = extrair_receita_liquida(caminho_pdf)
        if dados_pdf:
            todos_dados.extend(dados_pdf)
        else:
            logging.warning(f"⚠️ Nenhum dado extraído do arquivo {arquivo}.")

    return todos_dados

def salvar_em_csv(dados, arquivo_saida):
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
    df = pd.DataFrame(dados)
    df.to_csv(arquivo_saida, index=False)
    logging.info(f"✅ Dados de Receita Líquida salvos em: {arquivo_saida}")

if __name__ == '__main__':
    logging.info("🚀 Iniciando extração de Receita Líquida de todos os PDFs...")
    dados_extraidos = processar_todos_pdfs(PASTA_PDFS)
    if dados_extraidos:
        salvar_em_csv(dados_extraidos, ARQUIVO_DADOS)
    else:
        logging.warning("⚠️ Nenhum dado extraído. Verifique os arquivos.")
