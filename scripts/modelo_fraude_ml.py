import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from imblearn.over_sampling import SMOTE

# Verificar se o arquivo existe
arquivo = "tabela_final_reembolsos_com_score.xlsx"
if not os.path.exists(arquivo):
    print(f"❌ Arquivo '{arquivo}' não encontrado.")
    exit()

# Carregar dados
df = pd.read_excel(arquivo)

# Remover linhas com valores faltantes em colunas importantes
df = df.dropna(subset=['Valor', 'Comentário', 'fraude_score'])

# Garantir que 'Valor' seja positivo para log1p
df = df[df['Valor'] >= 0]

# Pré-processamento
df['Data'] = pd.to_datetime(df['Data'])
df['mes'] = df['Data'].dt.month
df['dia_semana'] = df['Data'].dt.dayofweek
df['valor_log'] = df['Valor'].apply(lambda x: round(np.log1p(x), 2))
df['comentario_vazio'] = df['Comentário'].apply(lambda x: int(str(x).strip() == '-'))

# Alvo
df['fraude_real'] = (df['fraude_score'] >= 2).astype(int)

# Features
features = [
    'duplicado', 'valor_acima_media', 'aprovador_suspeito', 'concentracao_gastos',
    'mes', 'dia_semana', 'valor_log', 'comentario_vazio'
]

# Garantir que não haja valores ausentes
X = df[features].fillna(0)
y = df['fraude_real']

# Balancear com SMOTE
smote = SMOTE(random_state=42)
X_res, y_res = smote.fit_resample(X, y)

# Modelo
modelo = RandomForestClassifier(n_estimators=100, random_state=42)
modelo.fit(X_res, y_res)

# Avaliar
scores = cross_val_score(modelo, X_res, y_res, cv=5, scoring='f1')
print("📈 F1 Score médio (cross-val):", round(scores.mean(), 4))

# Previsões
df['ml_predito'] = modelo.predict(X)

# Relatório
print("\n📊 Relatório de Classificação:")
print(classification_report(y, df['ml_predito']))

print("\n📌 Matriz de Confusão:")
print(confusion_matrix(y, df['ml_predito']))

# Exportar resultados
saida = "tabela_com_resultado_ml.xlsx"
df.to_excel(saida, index=False)
print(f"\n✅ Resultados salvos em: {saida}")
