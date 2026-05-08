import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import os

# Crear carpetas si no existen
os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

# Las 3 empresas
tickers = {
    "Tesla": "TSLA",
    "Apple": "AAPL",
    "Inditex": "ITX.MC"
}

resultados = []

for nombre, ticker in tickers.items():
    empresa = yf.Ticker(ticker)
    info = empresa.info

    ingresos = info.get("totalRevenue", 0)
    beneficio_bruto = info.get("grossProfits", 0)
    beneficio_neto = info.get("netIncomeToCommon", 0)
    ebitda = info.get("ebitda", 0)
    precio = info.get("currentPrice", 0)
    per = info.get("trailingPE", 0)
    market_cap = info.get("marketCap", 0)

    margen_bruto = (beneficio_bruto / ingresos * 100) if ingresos else 0
    margen_neto = (beneficio_neto / ingresos * 100) if ingresos else 0

    resultados.append({
        "Empresa": nombre,
        "Ingresos (B$)": round(ingresos / 1e9, 2),
        "Margen Bruto %": round(margen_bruto, 2),
        "Margen Neto %": round(margen_neto, 2),
        "EBITDA (B$)": round(ebitda / 1e9, 2),
        "PER": round(per, 2) if per else "N/A",
        "Market Cap (B$)": round(market_cap / 1e9, 2)
    })

# Guardar en CSV
df = pd.DataFrame(resultados)
df.to_csv("data/resultados.csv", index=False)
print(df.to_string(index=False))

# Gráfico 1 — Ingresos
plt.figure(figsize=(8, 5))
plt.bar(df["Empresa"], df["Ingresos (B$)"], color=["#e31937", "#555555", "#00a0e0"])
plt.title("Ingresos totales (Billions $)")
plt.ylabel("USD Billions")
plt.tight_layout()
plt.savefig("outputs/ingresos.png")
plt.close()

# Gráfico 2 — Márgenes
x = range(len(df["Empresa"]))
width = 0.35
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar([i - width/2 for i in x], df["Margen Bruto %"], width, label="Margen Bruto", color="#00a0e0")
ax.bar([i + width/2 for i in x], df["Margen Neto %"], width, label="Margen Neto", color="#e31937")
ax.set_xticks(x)
ax.set_xticklabels(df["Empresa"])
ax.set_title("Comparativa de márgenes (%)")
ax.set_ylabel("%")
ax.legend()
plt.tight_layout()
plt.savefig("outputs/margenes.png")
plt.close()

print("\nListo. Mira las carpetas /data y /outputs.")