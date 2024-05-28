import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Configurações gerais
num_records = 100000
inadimplencia_rate = 0.15

# Funções auxiliares
def random_dates(start_date, end_date, n):
    start_u = start_date.value // 10**9
    end_u = end_date.value // 10**9
    return pd.to_datetime(np.random.randint(start_u, end_u, n), unit='s')

def create_data(num_records : int = 100000, inadimplencia_rate : float = 0.15, divida = [50, 350])->pd.DataFrame:
    # Gerar número do cliente
    cliente_ids = np.arange(1, num_records + 1)

    # Gerar idades (18 a 70 anos)
    idades = np.random.randint(18, 71, num_records)

    # Gerar sexo (0: Feminino, 1: Masculino)
    sexos = np.random.choice(['Feminino', 'Masculino'], num_records)

    # Gerar quantidades de parcelas (1 a 24 parcelas)
    parcelas = np.random.randint(1, 25, num_records)

    # Gerar datas de vencimento (últimos 2 anos)
    vencimento_inicial = datetime.now() - timedelta(days=730)
    vencimento_final = datetime.now()
    datas_vencimento = random_dates(pd.to_datetime(vencimento_inicial), pd.to_datetime(vencimento_final), num_records)

    # Gerar status de inadimplência 
    status_inadimplencia = np.random.choice([0, 1], num_records, p=[1-inadimplencia_rate, inadimplencia_rate])
    chance_inadimplencia = [np.random.uniform(0,0.5) if x == 0 else np.random.uniform(0.5,1) for x in status_inadimplencia]
    # Gerar datas de pagamento
    datas_pagamento = []
    for i in range(num_records):
        if status_inadimplencia[i] == 0:
            # Pagamento em dia
            pagamento = datas_vencimento[i] - timedelta(days=np.random.randint(0, 5))
        else:
            # Pagamento em atraso
            pagamento = datas_vencimento[i] + timedelta(days=np.random.randint(1, 90)) # Alterei de 30 para 90 para testes
        datas_pagamento.append(pagamento)
    
    valor_divida = []
    for i in range(num_records):
        if status_inadimplencia[i] == 0:
            # Pagamento em dia
            valor = 0
        else:
            # Pagamento em atraso
            valor = random.randint(divida[0], divida[1])
        valor_divida.append(valor)

    # Montar o DataFrame
    df = pd.DataFrame({
        'numero_cliente': cliente_ids,
        'idade': idades,
        'sexo': sexos,
        'quantidade_parcelas': parcelas,
        'data_vencimento': datas_vencimento,
        'data_pagamento': datas_pagamento,
        'inadimplente': status_inadimplencia,
        'chance_inadimplencia': chance_inadimplencia,
        'valor': valor_divida
    })

    # # Exibir as primeiras linhas do DataFrame
    # print(df.head())

    # # Salvar o DataFrame em um arquivo CSV
    # df.to_csv('dados_clientes.csv', index=False)
    return df