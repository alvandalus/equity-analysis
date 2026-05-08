# IBEX 35 — Análisis Financiero Automático

Análisis financiero completo y automatizado de las 35 empresas del IBEX 35 usando datos reales extraídos con Python.

## Herramientas
- Python (yfinance, pandas, matplotlib, reportlab)
- Power BI (próximamente)

## Qué hace este proyecto
- Carga automáticamente las 35 empresas del IBEX 35
- Descarga datos financieros reales desde Yahoo Finance
- Calcula métricas clave: márgenes, EBITDA, PER, ROE, Deuda/EBITDA, Market Cap
- Genera 4 gráficos comparativos automáticamente
- Exporta un informe PDF completo con tablas y gráficos

## Gráficos generados
- Top 10 empresas por Market Cap
- Comparativa de márgenes bruto y neto
- Evolución histórica de precios (base 100, últimos 5 años)
- PER vs ROE — mapa de valoración

## Cómo ejecutarlo

```bash
pip install yfinance pandas matplotlib reportlab
python main.py
```

Los resultados se guardan en:
- `data/ibex35_analisis.csv` — datos completos en CSV
- `outputs/informe_ibex35.pdf` — informe PDF con gráficos

## Estructura

equity-analysis/
├── src/
│   ├── scraper.py      ← lista de empresas IBEX 35
│   ├── analysis.py     ← descarga y calcula ratios financieros
│   └── report.py       ← genera gráficos y PDF
├── data/               ← CSV con resultados
├── outputs/            ← gráficos y PDF generados
├── main.py             ← ejecuta todo en orden
└── README.md

## Métricas calculadas
| Métrica | Descripción |
|--------|-------------|
| Margen Bruto % | Beneficio bruto / Ingresos |
| Margen Neto % | Beneficio neto / Ingresos |
| EBITDA | Beneficio antes de intereses, impuestos y amortizaciones |
| PER | Precio / Beneficio por acción |
| ROE % | Rentabilidad sobre fondos propios |
| Deuda/EBITDA | Nivel de endeudamiento relativo |
| Market Cap | Capitalización bursátil total |