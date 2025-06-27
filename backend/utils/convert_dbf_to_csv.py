import os
import pandas as pd
from dbfread import DBF

UPLOAD_FOLDER = "uploads"
DATA_FOLDER = "data"

os.makedirs(DATA_FOLDER, exist_ok=True)

def parse_fecha_entero(valor):
    try:
        return pd.to_datetime(str(int(valor)), format="%Y%m%d", errors="coerce").date()
    except:
        return None

def convertir_creditos():
    ruta = os.path.join(UPLOAD_FOLDER, "cremae.dbf")
    tabla = DBF(ruta, encoding="latin-1", load=True)
    df = pd.DataFrame(iter(tabla))

    campos = [
        'NROCREDI', 'APELLIDO', 'DOMICILIO', 'TELEFONO', 'DOCUMENTO', 'VENDEDOR', 'SUCURSAL',
        'NROFACT', 'TOTFACT', 'FECHREAL', 'ANTICIPO', 'FINANCIA', 'CUOTAS', 'VTO1RA',
        'ARTIC1', 'CANT1', 'ARTIC2', 'CANT2', 'ARTIC3', 'CANT3', 'ARTIC4', 'CANT4',
        'ARTIC5', 'CANT5', 'ARTIC6', 'CANT6', 'ARTIC7', 'CANT7', 'GARANTE', 'DOMGARAN'
    ]
    df = df[campos]

    df['FECHREAL'] = df['FECHREAL'].apply(parse_fecha_entero)
    df['VTO1RA'] = df['VTO1RA'].apply(parse_fecha_entero)

    enteros = ['NROCREDI', 'VENDEDOR', 'SUCURSAL', 'NROFACT', 'CUOTAS',
               'ARTIC1', 'CANT1', 'ARTIC2', 'CANT2', 'ARTIC3', 'CANT3',
               'ARTIC4', 'CANT4', 'ARTIC5', 'CANT5', 'ARTIC6', 'CANT6',
               'ARTIC7', 'CANT7']
    for campo in enteros:
        df[campo] = pd.to_numeric(df[campo], errors='coerce').fillna(0).astype(int)

    df['DOCUMENTO'] = df['DOCUMENTO'].astype(str).str.strip().str.replace(r'\.0$', '', regex=True)
    df = df.rename(columns={
        'NROCREDI': 'num_credito',
        'APELLIDO': 'apellido',
        'DOMICILIO': 'domicilio',
        'TELEFONO': 'telefono',
        'DOCUMENTO': 'documento',
        'VENDEDOR': 'vendedor',
        'SUCURSAL': 'sucursal',
        'NROFACT': 'num_factura',
        'TOTFACT': 'total_facturado',
        'FECHREAL': 'fecha_real',
        'ANTICIPO': 'anticipo',
        'FINANCIA': 'financiacion',
        'CUOTAS': 'num_cuotas',
        'VTO1RA': 'vto_primer_cuota',
        'ARTIC1': 'articulo_1',
        'CANT1': 'cantidad_1',
        'ARTIC2': 'articulo_2',
        'CANT2': 'cantidad_2',
        'ARTIC3': 'articulo_3',
        'CANT3': 'cantidad_3',
        'ARTIC4': 'articulo_4',
        'CANT4': 'cantidad_4',
        'ARTIC5': 'articulo_5',
        'CANT5': 'cantidad_5',
        'ARTIC6': 'articulo_6',
        'CANT6': 'cantidad_6',
        'ARTIC7': 'articulo_7',
        'CANT7': 'cantidad_7',
        'GARANTE': 'garante',
        'DOMGARAN': 'domicilio_garante'
    })

    df.to_csv(os.path.join(DATA_FOLDER, "creditos.csv"), index=False, encoding="utf-8-sig")

def convertir_pagos():
    ruta = os.path.join(UPLOAD_FOLDER, "crepag.dbf")
    tabla = DBF(ruta, encoding="latin-1", load=True)
    df = pd.DataFrame(iter(tabla))

    campos = ['NROCRE_CUO', 'VENCIMIEN', 'FECHAPAGO', 'IMPORTE', 'IMPPAGO', 'VENDEDOR']
    df = df[campos].copy()

    df[['num_credito', 'num_cuota']] = df['NROCRE_CUO'].astype(str).str.split(expand=True)
    df['num_credito'] = pd.to_numeric(df['num_credito'], errors='coerce').fillna(0).astype(int)
    df['num_cuota'] = pd.to_numeric(df['num_cuota'], errors='coerce').fillna(0).astype(int)

    df['vencimiento'] = df['VENCIMIEN'].apply(parse_fecha_entero)
    df['fecha_pago'] = df['FECHAPAGO'].apply(parse_fecha_entero)

    df.rename(columns={
        'IMPORTE': 'importe',
        'IMPPAGO': 'importe_pago',
        'VENDEDOR': 'vendedor'
    }, inplace=True)

    df = df[['num_credito', 'num_cuota', 'vencimiento', 'fecha_pago', 'importe', 'importe_pago', 'vendedor']]
    df.to_csv(os.path.join(DATA_FOLDER, "pagos.csv"), index=False, encoding="utf-8-sig")

def generar_clientes():
    df = pd.read_csv(os.path.join(DATA_FOLDER, "creditos.csv"), encoding="utf-8-sig")
    clientes = df[['apellido', 'documento', 'telefono', 'domicilio']].drop_duplicates(subset='documento')
    clientes['estado'] = 'pendiente'
    clientes.to_csv(os.path.join(DATA_FOLDER, "clientes.csv"), index=False, encoding="utf-8-sig")

    # Testing

def revisar_archivos_csv():
    archivos = ["clientes.csv", "creditos.csv", "pagos.csv"]
    for archivo in archivos:
        ruta = os.path.join(DATA_FOLDER, archivo)
        print(f"\n📂 Revisando: {archivo}")
        try:
            df = pd.read_csv(ruta, encoding="utf-8-sig")
            print("🧬 Tipos de datos:")
            print(df.dtypes)
            print("\n🔍 Primeros 5 registros:")
            print(df.head())
        except Exception as e:
            print(f"⚠️ Error leyendo {archivo}: {e}")
    

if __name__ == "__main__":
    convertir_creditos()
    convertir_pagos()
    generar_clientes()
    revisar_archivos_csv()
    print("✔ Archivos CSV generados exitosamente.")
