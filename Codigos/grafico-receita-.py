import os
import pandas as pd
import matplotlib.pyplot as plt

PASTA_SAIDA = r'C:\Users\User2025\Desktop\CASE\output'
ARQUIVO_PLANILHA = os.path.join(PASTA_SAIDA, 'Case_Nome_Sobrenome_Preenchido.xlsx')
ARQUIVO_GRAFICO = os.path.join(PASTA_SAIDA, 'grafico_receita_liquida.png')

def gerar_grafico_receita(arquivo_planilha, arquivo_saida):
    # Lê a aba 'Database', pegando colunas B até D, com cabeçalho na linha 3 (header=2)
    df = pd.read_excel(arquivo_planilha, sheet_name='Database', header=2, usecols="B:D")

    # Remove espaços extras dos nomes das colunas
    df.columns = df.columns.str.strip()

    print("✅ Colunas após strip:", df.columns.tolist())

    # Filtra somente Receita Líquida
    df_receita = df[df['Conta'] == 'Receita Líquida']

    # Ordena cronologicamente
    df_receita = df_receita.sort_values(by='Periodo')

    # Plot
    plt.figure(figsize=(12, 6))
    plt.plot(df_receita['Periodo'], df_receita['Valor em MM'], marker='o', linestyle='-', color='b')

    plt.title('Evolução da Receita Líquida - Celesc')
    plt.xlabel('Período')
    plt.ylabel('Receita Líquida (em MM)')
    plt.xticks(rotation=45)
    plt.grid(True)
    plt.tight_layout()

    # Salva o gráfico
    plt.savefig(arquivo_saida)
    print(f"✅ Gráfico salvo em: {arquivo_saida}")

    # Mostra o gráfico
    plt.show()

if __name__ == '__main__':
    gerar_grafico_receita(ARQUIVO_PLANILHA, ARQUIVO_GRAFICO)
    