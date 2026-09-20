import matplotlib.pyplot as plt
from data_fetcher import build_fund_risk_metrics

def generate_single_ticker_card(ticker="SASA", fund_code="Ozel-Portfoy", holding_ratio=25.0, float_ratio=18.5):
    metric = build_fund_risk_metrics(
        fund_code=fund_code,
        top_holding_ticker=ticker,
        top_holding_ratio=holding_ratio,
        public_float_ratio=float_ratio
    )

    fig, ax = plt.subplots(figsize=(8.5, 4.5), dpi=300)
    fig.patch.set_facecolor("#0f172a")
    ax.set_facecolor("#0f172a")
    ax.axis("off")

    alarm = metric["Denetim Alarmı"]
    if alarm == "KRİTİK ALARM":
        badge_bg, badge_txt = "#450a0a", "#f87171"
    elif alarm in ["YÜKSEK RİSK", "GÖZETİM"]:
        badge_bg, badge_txt = "#451a03", "#fbbf24"
    else:
        badge_bg, badge_txt = "#052e16", "#4ade80"

    plt.text(0.05, 0.88, f"BIST LIKIDITE STRES TESTI: {ticker}", fontsize=14, weight="bold", color="#f8fafc")
    plt.text(0.05, 0.79, f"Portfoy: {fund_code} | Hacim Katilim Orani: %10", fontsize=9, color="#94a3b8")

    bbox_props = dict(boxstyle="round,pad=0.5", facecolor=badge_bg, edgecolor=badge_txt, lw=1.5)
    ax.text(0.85, 0.84, alarm, fontsize=10, weight="bold", color=badge_txt, ha="center", va="center", bbox=bbox_props)

    metrics_data = [
        ("Tasfiye Suresi", f"{metric['Tasfiye Süresi (İş Günü)']} Is Gunu"),
        ("Itfa Soku Dayanikligi", metric["İtfa Şoku"]),
        ("Portfoydeki Agirlik", f"%{metric['En Büyük Pay (%)']}"),
        ("Fiili Dolasim Payi", f"%{metric['Fiili Dolaşım Payı (%)']}")
    ]

    coords = [(0.05, 0.45), (0.52, 0.45), (0.05, 0.18), (0.52, 0.18)]
    for (label, val), (x, y) in zip(metrics_data, coords):
        ax.text(x, y + 0.10, label.upper(), fontsize=7.5, weight="bold", color="#64748b")
        ax.text(x, y, val, fontsize=13, weight="bold", color="#e2e8f0")

    output_filename = f"risk_rapor_{ticker}.png"
    plt.tight_layout()
    plt.savefig(output_filename, bbox_inches="tight", facecolor=fig.get_facecolor(), edgecolor="none")
    print(f"[OK] Risk Karti Olusturuldu: {output_filename}")

if __name__ == "__main__":
    # 1. Kart: SASA Analizi
    generate_single_ticker_card(
        ticker="SASA",
        fund_code="Yogunlasma-Portfoy",
        holding_ratio=25.0,
        float_ratio=18.5
    )

    # 2. Kart: ASELS Analizi
    generate_single_ticker_card(
        ticker="ASELS",
        fund_code="Kurumsal-Hisse-Fonu",
        holding_ratio=9.5,
        float_ratio=1.2
    )
    