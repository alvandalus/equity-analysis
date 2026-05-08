import yfinance as yf
import pandas as pd

def analizar_empresas(tickers):
    resultados = []
    total = len(tickers)
    
    for i, (nombre, ticker) in enumerate(tickers.items(), 1):
        print(f"Analizando {nombre} ({i}/{total})...")
        
        try:
            empresa = yf.Ticker(ticker)
            info = empresa.info

            ingresos = info.get("totalRevenue", 0) or 0
            beneficio_bruto = info.get("grossProfits", 0) or 0
            beneficio_neto = info.get("netIncomeToCommon", 0) or 0
            ebitda = info.get("ebitda", 0) or 0
            market_cap = info.get("marketCap", 0) or 0
            deuda = info.get("totalDebt", 0) or 0
            cash = info.get("totalCash", 0) or 0
            per = info.get("trailingPE", 0) or 0
            roe = info.get("returnOnEquity", 0) or 0
            precio = info.get("currentPrice", 0) or 0

            margen_bruto = round(beneficio_bruto / ingresos * 100, 2) if ingresos else 0
            margen_neto = round(beneficio_neto / ingresos * 100, 2) if ingresos else 0
            deuda_ebitda = round(deuda / ebitda, 2) if ebitda else 0

            resultados.append({
                "Empresa": nombre,
                "Ticker": ticker,
                "Precio (€)": round(precio, 2),
                "Ingresos (M€)": round(ingresos / 1e6, 2),
                "Margen Bruto %": margen_bruto,
                "Margen Neto %": margen_neto,
                "EBITDA (M€)": round(ebitda / 1e6, 2),
                "Market Cap (M€)": round(market_cap / 1e6, 2),
                "Deuda/EBITDA": deuda_ebitda,
                "PER": round(per, 2),
                "ROE %": round(roe * 100, 2),
                "Cash (M€)": round(cash / 1e6, 2)
            })

        except Exception as e:
            print(f"  Error con {nombre}: {e}")
            continue

    df = pd.DataFrame(resultados)
    df.to_csv("data/ibex35_analisis.csv", index=False)
    print(f"\nAnálisis completado: {len(df)} empresas")
    return df


def get_historico(tickers, periodo="5y"):
    print("\nDescargando datos históricos...")
    historico = {}
    
    for nombre, ticker in tickers.items():
        try:
            datos = yf.Ticker(ticker).history(period=periodo)
            if not datos.empty:
                historico[nombre] = datos["Close"]
                print(f"  {nombre} OK")
        except Exception as e:
            print(f"  Error {nombre}: {e}")
    
    return historico