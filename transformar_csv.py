import os
import pandas as pd

PASTA_SAIDA = r'C:\Users\User2025\Desktop\CASE\output'
ARQUIVO_DADOS = os.path.join(PASTA_SAIDA, 'receita_liquida.csv')
ARQUIVO_EXCEL = os.path.join(PASTA_SAIDA, 'dados_extraidos.xlsx')

def csv_para_excel(arquivo_csv, arquivo_excel):
    df = pd.read_csv(arquivo_csv)
    df.to_excel(arquivo_excel, index=False)
    print(f"✅ Arquivo Excel criado: {arquivo_excel}")

if __name__ == '__main__':
    csv_para_excel(ARQUIVO_DADOS, ARQUIVO_EXCEL)
