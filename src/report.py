import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd
import os

def generar_graficos(df, historico):
    os.makedirs("outputs", exist_ok=True)
    graficos = []

    # Gráfico 1 — Top 10 por Market Cap
    top10 = df.nlargest(10, "Market Cap (M€)")
    fig, ax = plt.subplots(figsize=(10, 6))
    bars = ax.barh(top10["Empresa"], top10["Market Cap (M€)"], color="#00a0e0")
    ax.set_title("Top 10 IBEX 35 por Market Cap (M€)")
    ax.set_xlabel("M€")
    plt.tight_layout()
    path = "outputs/top10_marketcap.png"
    plt.savefig(path)
    plt.close()
    graficos.append(path)

    # Gráfico 2 — Comparativa márgenes
    df_valido = df[(df["Margen Bruto %"] > 0) & (df["Margen Neto %"] > 0)].nlargest(10, "Margen Bruto %")
    x = range(len(df_valido))
    width = 0.35
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar([i - width/2 for i in x], df_valido["Margen Bruto %"], width, label="Margen Bruto", color="#00a0e0")
    ax.bar([i + width/2 for i in x], df_valido["Margen Neto %"], width, label="Margen Neto", color="#e31937")
    ax.set_xticks(x)
    ax.set_xticklabels(df_valido["Empresa"], rotation=45, ha="right")
    ax.set_title("Top 10 IBEX 35 — Comparativa de Márgenes (%)")
    ax.set_ylabel("%")
    ax.legend()
    plt.tight_layout()
    path = "outputs/margenes.png"
    plt.savefig(path)
    plt.close()
    graficos.append(path)

    # Gráfico 3 — Evolución histórica de precios
    if historico:
        fig, ax = plt.subplots(figsize=(12, 6))
        for nombre, serie in list(historico.items())[:5]:
            serie_norm = serie / serie.iloc[0] * 100
            ax.plot(serie_norm.index, serie_norm.values, label=nombre)
        ax.set_title("Evolución histórica de precios — Top 5 (base 100)")
        ax.set_ylabel("Precio base 100")
        ax.legend()
        plt.tight_layout()
        path = "outputs/historico.png"
        plt.savefig(path)
        plt.close()
        graficos.append(path)

    # Gráfico 4 — PER vs ROE
    df_per = df[(df["PER"] > 0) & (df["PER"] < 100) & (df["ROE %"] > 0)]
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.scatter(df_per["PER"], df_per["ROE %"], color="#00a0e0", s=80)
    for _, row in df_per.iterrows():
        ax.annotate(row["Empresa"], (row["PER"], row["ROE %"]), fontsize=7, ha="left")
    ax.set_title("PER vs ROE — IBEX 35")
    ax.set_xlabel("PER")
    ax.set_ylabel("ROE %")
    plt.tight_layout()
    path = "outputs/per_vs_roe.png"
    plt.savefig(path)
    plt.close()
    graficos.append(path)

    print(f"{len(graficos)} gráficos generados")
    return graficos


def generar_pdf(df, graficos):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from datetime import datetime

    path_pdf = "outputs/informe_ibex35.pdf"
    doc = SimpleDocTemplate(path_pdf, pagesize=landscape(A4), leftMargin=1*cm, rightMargin=1*cm, topMargin=1*cm, bottomMargin=1*cm)
    styles = getSampleStyleSheet()
    elementos = []

    # Título
    titulo_style = ParagraphStyle("titulo", fontSize=18, fontName="Helvetica-Bold", spaceAfter=6)
    sub_style = ParagraphStyle("sub", fontSize=10, fontName="Helvetica", textColor=colors.grey, spaceAfter=20)
    elementos.append(Paragraph("Informe Financiero — IBEX 35", titulo_style))
    elementos.append(Paragraph(f"Generado automáticamente el {datetime.now().strftime('%d/%m/%Y %H:%M')}", sub_style))

    # Gráficos
    for grafico in graficos:
        if os.path.exists(grafico):
            elementos.append(Image(grafico, width=24*cm, height=10*cm))
            elementos.append(Spacer(1, 0.5*cm))

    # Tabla de datos
    elementos.append(Paragraph("Datos financieros completos", styles["Heading2"]))
    elementos.append(Spacer(1, 0.3*cm))

    cols = ["Empresa", "Precio (€)", "Ingresos (M€)", "Margen Bruto %", "Margen Neto %", "EBITDA (M€)", "Market Cap (M€)", "PER", "ROE %", "Deuda/EBITDA"]
    data = [cols]
    for _, row in df.iterrows():
        data.append([str(row.get(c, "N/A")) for c in cols])

    tabla = Table(data, repeatRows=1)
    tabla.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#00a0e0")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f5f5")]),
        ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#dddddd")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elementos.append(tabla)

    doc.build(elementos)
    print(f"\nPDF generado: {path_pdf}")
    return path_pdf