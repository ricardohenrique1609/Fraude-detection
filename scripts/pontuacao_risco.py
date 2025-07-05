import pandas as pd
import os

# Verificação de acesso ao arquivo
arquivo = "dataset_reembolsos_simulado.xlsx"
if os.path.exists(arquivo):
    try:
        with open(arquivo, "rb") as f:
            pass
    except PermissionError:
        print(f"❌ Feche o arquivo '{arquivo}' no Excel antes de rodar o script.")
        exit()
else:
    print("❌ Arquivo não encontrado.")
    exit()

# Carregar o dataset
df = pd.read_excel(arquivo)

# Converter a coluna de data
df['Data'] = pd.to_datetime(df['Data'])

# REGRA 1: Duplicidade — mesmo funcionário, valor, tipo de despesa e aprovador
df['duplicado'] = df.duplicated(subset=['Funcionário', 'Valor', 'Tipo de Despesa', 'Aprovador'], keep=False)

# REGRA 2: Valor anormal — acima da média + 0.8 * desvio padrão, com pelo menos 3 registros por funcionário
df['valor_acima_media'] = False
for nome in df['Funcionário'].unique():
    grupo = df[df['Funcionário'] == nome]
    if len(grupo) >= 3:
        media = grupo['Valor'].mean()
        std = grupo['Valor'].std()
        if std > 0:
            limite = media + 0.8 * std
            idx = grupo[grupo['Valor'] > limite].index
            df.loc[idx, 'valor_acima_media'] = True


# REGRA 3: Aprovadores com taxa de aprovação > 90%
aprovador_stats = df.groupby('Aprovador')['Status'].value_counts(normalize=True).unstack().fillna(0)
aprovadores_suspeitos = aprovador_stats[aprovador_stats['Aprovado'] > 0.90].index.tolist()
df['aprovador_suspeito'] = df['Aprovador'].isin(aprovadores_suspeitos)

# REGRA 4: Funcionários com mais de 10% do total reembolsado
total_geral = df['Valor'].sum()
gasto_funcionario = df.groupby('Funcionário')['Valor'].sum()
func_suspeitos = gasto_funcionario[gasto_funcionario > 0.1 * total_geral].index.tolist()
df['concentracao_gastos'] = df['Funcionário'].isin(func_suspeitos)

# SCORE FINAL
df['fraude_score'] = (
    df['duplicado'].astype(int) +
    df['valor_acima_media'].astype(int) +
    df['aprovador_suspeito'].astype(int) +
    df['concentracao_gastos'].astype(int)
)

# Classificação do risco
def classificar_risco(score):
    if score == 0:
        return "Sem risco"
    elif score == 1:
        return "Baixo"
    elif score == 2:
        return "Médio"
    else:
        return "Alto"

df['nivel_risco'] = df['fraude_score'].apply(classificar_risco)

# Exportar resultado
arquivo_saida = "tabela_final_reembolsos_com_score.xlsx"
if os.path.exists(arquivo_saida):
    try:
        os.remove(arquivo_saida)
    except PermissionError:
        print(f"❌ Feche o arquivo '{arquivo_saida}' antes de rodar o script.")
        exit()

df.to_excel(arquivo_saida, index=False)

# Mostrar resumo no terminal
print("📊 Score de fraude aplicado com sucesso!")
print("\nDistribuição por nível de risco:")
print(df['nivel_risco'].value_counts())

print("\nTSop 10 registros mais suspeitos:")
print(df[df['fraude_score'] > 0][['Funcionário', 'Valor', 'Tipo de Despesa', 'fraude_score', 'nivel_risco']].head(10))
