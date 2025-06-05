import os
import pandas as pd
import matplotlib.pyplot as plt

PASTA_SAIDA = r'C:\Users\User2025\Desktop\CASE\output'
ARQUIVO_PLANILHA = os.path.join(PASTA_SAIDA, 'Case_Nome_Sobrenome_Preenchido.xlsx')
ARQUIVO_GRAFICO_ACUMULADO = os.path.join(PASTA_SAIDA, 'grafico_receita_acumulada.png')

def gerar_grafico_receita_acumulada(arquivo_planilha, arquivo_saida):
    df = pd.read_excel(arquivo_planilha, sheet_name='Database', header=2, usecols="B:D")
    df.columns = df.columns.str.strip()
    
    df_receita = df[df['Conta'] == 'Receita Líquida']
    df_receita = df_receita.sort_values(by='Periodo')
    
    df_receita['Receita Acumulada'] = df_receita['Valor em MM'].cumsum()

    plt.figure(figsize=(12, 6))
    plt.plot(df_receita['Periodo'], df_receita['Receita Acumulada'], marker='o', linestyle='-', color='g')

    plt.title('Evolução da Receita Líquida Acumulada - Celesc')
    plt.xlabel('Período')
    plt.ylabel('Receita Líquida Acumulada (em MM)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    plt.savefig(arquivo_saida)
    print(f"✅ Gráfico acumulado salvo em: {arquivo_saida}")

    plt.close()

if __name__ == '__main__':
    gerar_grafico_receita_acumulada(ARQUIVO_PLANILHA, ARQUIVO_GRAFICO_ACUMULADO)
