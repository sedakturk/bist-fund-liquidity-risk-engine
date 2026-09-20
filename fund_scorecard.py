import pandas as pd
import matplotlib.pyplot as plt
from data_fetcher import build_fund_risk_metrics

def generate_live_scorecard():
    case_universe = [
        {"fund": "Fon A (Hisse - Kriz Vaka)", "aum": 1450.0, "top_ticker": "KENT", "top_ratio": 42.0, "float_ratio": 32.5},
        {"fund": "Fon B (Karma - Kriz Vaka)", "aum": 820.0, "top_ticker": "CONSE", "top_ratio": 37.5, "float_ratio": 29.0},
        {"fund": "Fon C (Serbest - Yuksek Risk)", "aum": 2100.0, "top_ticker": "INFO", "top_ratio": 28.0, "float_ratio": 21.0},
        {"fund": "Fon D (Para P. - Gozetim)", "aum": 3400.0, "top_ticker": "ISMEN", "top_ratio": 18.2, "float_ratio": 14.1},
        {"fund": "Benchmark 1 (BIST 30)", "aum": 5400.0, "top_ticker": "THYAO", "top_ratio": 8.5, "float_ratio": 1.1},
        {"fund": "Benchmark 2 (BIST 100)", "aum": 4800.0, "top_ticker": "TUPRS", "top_ratio": 7.8, "float_ratio": 0.8}
    ]
    
    records = []
    for item in case_universe:
        metric = build_fund_risk_metrics(
            fund_code=item["fund"],
            top_holding_ticker=item["top_ticker"],
            top_holding_ratio=item["top_ratio"],
            public_float_ratio=item["float_ratio"]
        )
        metric["Portföy (M TL)"] = item["aum"]
        records.append(metric)
        
    return pd.DataFrame(records)

def export_scorecard_image(df: pd.DataFrame, output_path: str = "fund_risk_scorecard.png"):
    fig, ax = plt.subplots(figsize=(14.5, 6.2), dpi=300)
    fig.patch.set_facecolor("#0f172a") # Koyu kurumsal arka plan
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    # Başlık Alanı
    plt.title(
        "BIST FON PIYASASI LIKIDITE & RISK DENETIM KARNESI\n"
        "Itfa Darbogazlari Neden Yasandi? Portfoy Yogunlasmasi ve Tasfiye Suresi Stres Testi",
        fontsize=13,
        weight="bold",
        color="#f8fafc",
        pad=26,
        loc="left"
    )

    columns = list(df.columns)
    cell_text = df.values.tolist()

    # Sütun Genişlik Oranları (Toplam = 1.0)
    # Fon adına geniş alan, sayılara kompakt alan
    col_widths = [0.24, 0.12, 0.13, 0.14, 0.14, 0.11, 0.12]

    table = ax.table(
        cellText=cell_text,
        colLabels=columns,
        colWidths=col_widths,
        cellLoc="center",
        loc="center"
    )

    table.auto_set_font_size(False)
    table.set_fontsize(9.5)
    table.scale(1.0, 2.3)

    # Başlık Hücreleri Biçimlendirmesi
    for col_idx in range(len(columns)):
        header_cell = table[(0, col_idx)]
        header_cell.set_facecolor("#1e293b")
        header_cell.set_text_props(weight="bold", color="#94a3b8")
        header_cell.set_edgecolor("#334155")

    # Veri Satırları ve Risk Alarm Renklendirmeleri
    for row_idx, row in df.iterrows():
        alarm = row["Denetim Alarmı"]
        
        if alarm == "KRİTİK ALARM":
            bg_color = "#450a0a"
            text_color = "#f87171"
        elif alarm in ["YÜKSEK RİSK", "GÖZETİM"]:
            bg_color = "#451a03"
            text_color = "#fbbf24"
        else:
            bg_color = "#052e16"
            text_color = "#4ade80"

        for col_idx in range(len(columns)):
            cell = table[(row_idx + 1, col_idx)]
            cell.set_facecolor("#1e293b" if col_idx != len(columns) - 1 else bg_color)
            
            # İlk sütun (Fon Kodu) sola dayalı ve ferah
            if col_idx == 0:
                cell.set_text_props(color="#e2e8f0", weight="bold", ha="left")
            elif col_idx == len(columns) - 1:
                cell.set_text_props(color=text_color, weight="bold")
            else:
                cell.set_text_props(color="#e2e8f0")
                
            cell.set_edgecolor("#334155")

    # Dipnot
    plt.figtext(
        0.04, 0.03,
        "* Metodoloji Notu: BIST hacim verileriyle beslenen analitik stres testi simülasyonudur. Belirli bir fonu doğrudan hedef göstermez.\n"
        "* Tasfiye Suresi (Days-to-Liquidate): Fonun ilgili pozisyonunu azami %10 piyasa katilim oraniyla bozmadan satabilecegi tahmini is gunudur.",
        fontsize=8.5,
        color="#64748b",
        ha="left"
    )

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    print(f"\n[OK] Kusursuz Hizalanmis Risk Karnesi Olusturuldu: {output_path}")

if __name__ == "__main__":
    df_live = generate_live_scorecard()
    export_scorecard_image(df_live)
    