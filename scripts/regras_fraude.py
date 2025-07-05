import pandas as pd
import numpy as np
from faker import Faker
import random
import os

fake = Faker('pt_BR')
np.random.seed(42)
random.seed(42)

num_registros = 5000
departamentos = ['Vendas', 'RH', 'TI', 'Financeiro', 'Marketing', 'Logística']
tipos_despesa = ['Restaurante', 'Táxi', 'Hotel', 'Passagem Aérea', 'Transporte', 'Material Escritório']
status_list = ['Aprovado', 'Negado']
aprovadores = ['Carlos', 'João', 'Mariana', 'Paula', 'Roberto']

# Definindo aprovadores fraudulentos
aprovadores_fraudulentos = random.sample(aprovadores, 2)

# Gerar funcionários com tendência a fraudar
funcionarios_fraudulentos = [fake.name() for _ in range(5)]

dados = []

for i in range(1, num_registros + 1):
    # 10% de chance de duplicar um registro anterior
    if i > 10 and random.random() < 0.1:
        dados.append(dados[i - random.randint(2, 10)])
        continue

    funcionario = random.choice(funcionarios_fraudulentos) if random.random() < 0.15 else fake.name()
    departamento = random.choice(departamentos)
    data = fake.date_between(start_date='-6M', end_date='today')

    if funcionario in funcionarios_fraudulentos:
        valor = round(np.random.normal(1500, 600), 2)
    else:
        valor = round(np.random.exponential(scale=200), 2)

    tipo = random.choice(tipos_despesa)
    aprovador = random.choice(aprovadores_fraudulentos) if random.random() < 0.3 else random.choice(aprovadores)
    status = "Aprovado" if aprovador in aprovadores_fraudulentos or random.random() < 0.9 else "Negado"
    comentario = "Comprovante anexado" if random.random() > 0.9 else "-"

    dados.append([i, funcionario, departamento, data, valor, tipo, aprovador, status, comentario])

df = pd.DataFrame(dados, columns=[
    'ID', 'Funcionário', 'Departamento', 'Data', 'Valor',
    'Tipo de Despesa', 'Aprovador', 'Status', 'Comentário'
])

nome_arquivo = "dataset_reembolsos_simulado.xlsx"
if os.path.exists(nome_arquivo):
    try:
        os.remove(nome_arquivo)
    except PermissionError:
        print(f"❌ Feche o arquivo '{nome_arquivo}' para salvar.")
        exit()

df.to_excel(nome_arquivo, index=False)
print(f"✅ Dataset com fraudes realistas gerado com sucesso! Registros: {len(df)}")
