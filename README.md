# 📊 Case Celesc — Análise Automatizada de Demonstrações Financeiras

Este projeto foi desenvolvido como parte de um **case técnico**, com o objetivo de automatizar a extração e organização de dados financeiros da empresa **Celesc**, além de realizar análises complementares e coleta de informações públicas via **WebScraping**.

---

## ✅ Objetivos do Projeto

- 📥 Extrair dados da **Demonstração do Resultado do Exercício (DRE)** a partir dos PDFs disponibilizados no site de Relações com Investidores (RI) da Celesc.
- 🗃️ Organizar os dados em formato estruturado e preencher automaticamente a **planilha modelo**.
- 📈 Gerar **gráficos analíticos** sobre a evolução e acumulação da Receita Líquida.
- 🌐 Realizar **WebScraping** para coleta de **Fatos Relevantes** e **Avisos aos Acionistas**.

---

## ✅ Funcionalidades

- **Extração automatizada** da Receita Líquida (Conta 3.11) utilizando `pdfplumber`.
- **Conversão e tratamento de dados** em `pandas`.
- **Preenchimento automático** de planilhas com `openpyxl`.
- **Geração de gráficos** utilizando `matplotlib`.
- **Coleta automatizada de dados públicos** com `selenium`.

---

## ✅ Tecnologias Utilizadas

- Python 3
- pandas
- matplotlib
- pdfplumber
- openpyxl
- selenium
- webdriver-manager

---

## ✅ Estrutura do Projeto
````
Celesc-Case
│
├── data/
│ ├── receita_liquida.csv
│ ├── dados_extraidos.xlsx
│ └── aviso_acionistas.csv
│
├── output/
│ ├── grafico_receita_liquida.png
│ ├── grafico_receita_acumulada.png
│ └── Case_Nome_Sobrenome_Preenchido.xlsx
│
├── code/
│ ├── extrair_receita_liquida.py
│ ├── preencher_planilha_receita.py
│ ├── gerar_grafico_receita.py
│ ├── gerar_grafico_receita_acumulada.py
│ ├── csv_para_excel.py
│ └── webscraping_fatos_relevantes.py
│
├── README.md
└── Relatorio_Case_Celesc.pdf
````


---

## ✅ Como Executar

1. Clone este repositório:  
   ```bash
   git clone https://github.com/seu_usuario/celesc-case.git
   cd celesc-case
   ```
2. Instale as dependências:
```
pip install -r requirements.txt
```
3. Execute os scripts na seguinte ordem:
```
extrair_receita_liquida.py → Extrai os dados dos PDFs.

csv_para_excel.py → Converte o CSV para Excel.

preencher_planilha_receita.py → Preenche a planilha modelo.

gerar_grafico_receita.py → Gera o gráfico da Receita Líquida.

gerar_grafico_receita_acumulada.py → Gera o gráfico acumulado.

webscraping_fatos_relevantes.py → Coleta Fatos Relevantes.
```
## 4. Consulte o relatório final para detalhes da implementação e análises:
➡️ Relatorio_Case_Celesc.pdf

## 5. Resultados
- Base de dados estruturada e organizada.

- Gráficos demonstrando evolução e acumulação da Receita Líquida.

- Fatos Relevantes coletados automaticamente.

- Relatório técnico documentando todo o processo.
