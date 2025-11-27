
from fastapi import FastAPI, Query
import requests
import re

app = FastAPI()

API_KEY = "c64f4814177016aff6677a1d"  # Coloca tu clave de ExchangeRate-API
BASE_URL = f"https://v6.exchangerate-api.com/v6/{API_KEY}/pair"

@app.get("/convert")
def convertir(mensaje: str = Query(..., description="Texto con formato '<cantidad> UYU a USD o ARS'")):
    # Patrón más flexible: acepta espacios opcionales y mayúsculas/minúsculas
    patron = r"(\d+(?:\.\d+)?)\s*UYU\s*a\s*(USD|ARS)"
    match = re.search(patron, mensaje, re.IGNORECASE)

    if not match:
        return {"error": "Formato inválido. Usa: <cantidad> UYU a USD o ARS"}

    cantidad = float(match.group(1))
    moneda_destino = match.group(2).upper()

    # Llamar API
    url = f"{BASE_URL}/UYU/{moneda_destino}/{cantidad}"
    response = requests.get(url)

    if response.status_code != 200:
        return {"error": "Error al consultar la API"}

    data = response.json()
    resultado = data.get("conversion_result")

    return {"resultado": f"{cantidad} UYU = {resultado:.2f} {moneda_destino}"}
