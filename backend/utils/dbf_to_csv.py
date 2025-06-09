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
    df = pd.read_csv(os.path.join(DATA_FOLDER, "creditos.csv"), encoding="utf-8-sig")

    df = df.rename(columns={
        'APELLIDO': 'apellido',
        'DOCUMENTO': 'documento',
        'TELEFONO': 'telefono',
        'DOMICILIO': 'domicilio'
    })

    clientes = df[['apellido', 'documento', 'telefono', 'domicilio']].drop_duplicates(subset='documento')
    clientes['historial_atraso'] = 0
    clientes = clientes[['apellido', 'documento', 'telefono', 'domicilio', 'historial_atraso']]
    clientes.to_csv(os.path.join(DATA_FOLDER, "clientes.csv"), index=False, encoding="utf-8-sig")
