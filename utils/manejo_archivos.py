import pandas as pd
from utils.dirs import obtener_ruta

def leer_viviendas():
    try:
        return pd.read_csv(obtener_ruta(".LED/datos/viviendas.csv")).values.tolist()
    except FileNotFoundError:
        return []

def guardar_vivienda(desc, precio, ubi, foto):
    try:
        df = pd.read_csv(obtener_ruta(".LED/datos/viviendas.csv"))
    except FileNotFoundError:
        df = pd.DataFrame(columns=["ID", "Descripcion", "Precio", "Ubicacion", "Foto"])
    
    nuevo_id = df["ID"].max() + 1 if not df.empty else 1
    nueva_vivienda = {"ID": nuevo_id, "Descripcion": desc, "Precio": precio, "Ubicacion": ubi, "Foto": foto}
    df.loc[len(df)] = nueva_vivienda
    df.to_csv("~/.LED/datos/viviendas.csv", index=False)

def eliminar_vivienda(vivienda_id):
    df = pd.read_csv(obtener_ruta(".LED/datos/viviendas.csv"))
    df = df[df["ID"] != int(vivienda_id)]
    df.to_csv(obtener_ruta(".LED/datos/viviendas.csv"), index=False)
