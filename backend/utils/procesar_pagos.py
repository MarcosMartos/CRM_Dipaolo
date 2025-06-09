import pandas as pd
from datetime import datetime

def parse_fecha(fecha_str):
    try:
        return datetime.strptime(str(fecha_str), "%Y%m%d").date()
    except:
        return None

def procesar_pagos(ruta_csv):
    df = pd.read_csv(ruta_csv, encoding="latin-1")

    # Dividir NROCRE_CUO en dos columnas
    df[['num_credito', 'num_cuota']] = df['NROCRE_CUO'].astype(str).str.split(expand=True)

    # Convertir tipos
    df['num_credito'] = df['num_credito'].astype(int)
    df['num_cuota'] = df['num_cuota'].astype(int)

    # Convertir fechas
    df['vencimiento'] = df['VENCIMIEN'].apply(parse_fecha)
    df['fecha_pago'] = df['FECHAPAGO'].apply(parse_fecha)

    # Renombrar columnas para que coincidan con el modelo
    df = df.rename(columns={
        'IMPORTE': 'importe',
        'IMPPAGO': 'importe_pago',
        'VENDEDOR': 'vendedor'
    })

    # Retornar solo los campos necesarios
    return df[['num_credito', 'num_cuota', 'vencimiento', 'fecha_pago', 'importe', 'importe_pago', 'vendedor']]
