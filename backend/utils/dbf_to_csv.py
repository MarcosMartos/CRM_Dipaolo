import os
import pandas as pd
from dbfread import DBF


UPLOAD_FOLDER = "uploads"
DATA_FOLDER = "data"

# Crear carpeta si no existe
os.makedirs(DATA_FOLDER, exist_ok=True)
def convertir_cremae():
    ruta = os.path.join(UPLOAD_FOLDER, "cremae.dbf")
    tabla = DBF(ruta, encoding="latin-1", load=True)
    df = pd.DataFrame(iter(tabla))

    campos_utiles = [
        'NROCREDI', 'APELLIDO', 'DOMICILIO', 'TELEFONO', 'DOCUMENTO',
        'VENDEDOR', 'SUCURSAL', 'NROFACT', 'TOTFACT', 'FECHREAL',
        'ANTICIPO', 'FINANCIA', 'CUOTAS', 'VTO1RA',
        'ARTIC1', 'CANT1', 'ARTIC2', 'CANT2', 'ARTIC3', 'CANT3',
        'ARTIC4', 'CANT4', 'ARTIC5', 'CANT5', 'ARTIC6', 'CANT6',
        'ARTIC7', 'CANT7', 'GARANTE', 'DOMGARAN'
    ]

    df_filtrado = df[campos_utiles].copy()
    df_filtrado['estado'] = 'activo'
    df_filtrado = df_filtrado[campos_utiles + ['estado']]

    df_filtrado.to_csv(os.path.join(DATA_FOLDER, "creditos.csv"), index=False, encoding="utf-8-sig")

def convertir_crepag():
    ruta = os.path.join(UPLOAD_FOLDER, "crepag.dbf")
    tabla = DBF(ruta, encoding="latin-1", load=True)
    df = pd.DataFrame(iter(tabla))

    campos_utiles = ['NROCRE_CUO', 'VENCIMIEN', 'FECHAPAGO', 'IMPORTE', 'IMPPAGO', 'VENDEDOR']
    df_filtrado = df[campos_utiles].copy()

    # Separar NROCRE_CUO en num_credito y num_cuota
    df_filtrado[['num_credito', 'num_cuota']] = df_filtrado['NROCRE_CUO'].astype(str).str.split(expand=True)

    # Reordenar y renombrar columnas
    df_final = df_filtrado.rename(columns={
        'VENCIMIEN': 'vencimiento',
        'FECHAPAGO': 'fecha_pago',
        'IMPORTE': 'importe',
        'IMPPAGO': 'importe_pago',
        'VENDEDOR': 'vendedor'
    })

    df_final = df_final[['num_credito', 'num_cuota', 'vencimiento', 'fecha_pago', 'importe', 'importe_pago', 'vendedor']]
    df_final.to_csv(os.path.join(DATA_FOLDER, "pagos.csv"), index=False, encoding="utf-8-sig")

def generar_clientes():
    df_creditos = pd.read_csv(os.path.join(DATA_FOLDER, "creditos.csv"), encoding="utf-8-sig")
    df_pagos = pd.read_csv(os.path.join(DATA_FOLDER, "pagos.csv"), encoding="utf-8-sig")

    df = df_creditos.rename(columns={
        'APELLIDO': 'apellido',
        'DOCUMENTO': 'documento',
        'TELEFONO': 'telefono',
        'DOMICILIO': 'domicilio'
    })

    clientes = df[['apellido', 'documento', 'telefono', 'domicilio']].drop_duplicates(subset='documento')
    clientes['historial_atraso'] = 0

    from datetime import datetime, timedelta
    hoy = datetime.today().date()
    hace_un_ano = hoy - timedelta(days=365)

    def calcular_estado(doc):
        creditos_cliente = df_creditos[df_creditos['DOCUMENTO'] == doc]
        creditos_recientes = creditos_cliente[
            pd.to_datetime(creditos_cliente['FECHREAL'], errors='coerce') >= pd.Timestamp(hace_un_ano)
        ]
        promedio = creditos_recientes['TOTFACT'].mean() if not creditos_recientes.empty else 0

        num_creditos = creditos_cliente['NROCREDI'].dropna().astype(str).unique()
        pagos_cliente = df_pagos[df_pagos['num_credito'].astype(str).isin(num_creditos)]

        pagos_vencidos = pagos_cliente[
            (pd.to_datetime(pagos_cliente['vencimiento'], errors='coerce') < pd.Timestamp(hoy)) &
            (pagos_cliente['importe_pago'] < pagos_cliente['importe'])
        ]

        atrasos = pagos_vencidos.shape[0]

        if atrasos == 0:
            return "excelente" if promedio > 300000 else "bueno"
        elif atrasos <= 2:
            return "remolon"
        else:
            return "malo"

    clientes["estado"] = clientes["documento"].apply(calcular_estado)

    clientes.to_csv(os.path.join(DATA_FOLDER, "clientes.csv"), index=False, encoding="utf-8-sig")
