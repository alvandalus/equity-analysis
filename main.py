from src.scraper import get_ibex35_tickers
from src.analysis import analizar_empresas, get_historico
from src.report import generar_graficos, generar_pdf
import os

os.makedirs("data", exist_ok=True)
os.makedirs("outputs", exist_ok=True)

print("=" * 50)
print("IBEX 35 — Análisis Financiero Automático")
print("=" * 50)

# 1. Obtener tickers
print("\n1. Obteniendo empresas del IBEX 35...")
tickers = get_ibex35_tickers()

# 2. Analizar empresas
print("\n2. Descargando datos financieros...")
df = analizar_empresas(tickers)

# 3. Datos históricos
print("\n3. Descargando histórico de precios...")
historico = get_historico(tickers)

# 4. Generar gráficos
print("\n4. Generando gráficos...")
graficos = generar_graficos(df, historico)

# 5. Generar PDF
print("\n5. Generando informe PDF...")
pdf = generar_pdf(df, graficos)

print("\n" + "=" * 50)
print("COMPLETADO")
print(f"CSV: data/ibex35_analisis.csv")
print(f"PDF: outputs/informe_ibex35.pdf")
print("=" * 50)