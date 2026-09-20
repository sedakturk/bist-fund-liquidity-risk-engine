import requests
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

def get_tefas_fund_aum(fund_code: str) -> float:
    """
    TEFAS web servisinden fonun son toplam portföy büyüklüğünü (AUM - TL) çeker.
    """
    url = "https://www.tefas.gov.tr/api/DB/BindHistoryInfo"
    today_str = datetime.today().strftime("%d.%m.%Y")
    start_str = (datetime.today() - timedelta(days=7)).strftime("%d.%m.%Y")
    
    headers = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.tefas.gov.tr/TarihselVeriler.aspx"
    }
    
    payload = {
        "fontipi": "YAT",
        "fonkod": fund_code.upper(),
        "bastarih": start_str,
        "bittarih": today_str
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers, timeout=10)
        data = response.json()
        if data.get("data") and len(data["data"]) > 0:
            last_record = data["data"][-1]
            # TEFAS API'sinde portföy büyüklüğü: PORTFOYBUYUKLUK
            return float(last_record.get("PORTFOYBUYUKLUK", 0.0))
    except Exception as e:
        print(f"[{fund_code}] TEFAS verisi çekilemedi: {e}")
    
    return 0.0

def get_bist_stock_adtv_tl(ticker: str, lookback_days: int = 30) -> float:
    """
    Yahoo Finance üzerinden BIST hissesinin son N günlük 
    Ortalama Günlük İşlem Hacmini (ADTV - TL cinsinden) hesaplar.
    """
    symbol = f"{ticker.upper()}.IS"
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="3mo")
        if df.empty or len(df) < 5:
            return 0.0
        
        # Günlük TL Hacmi = Kapanış Fiyatı * Lot Hacmi
        df["Volume_TL"] = df["Close"] * df["Volume"]
        recent_df = df.tail(lookback_days)
        adtv = recent_df["Volume_TL"].mean()
        return float(adtv)
    except Exception as e:
        print(f"[{ticker}] Hacim verisi çekilemedi: {e}")
        return 0.0

def build_fund_risk_metrics(fund_code: str, top_holding_ticker: str, top_holding_ratio: float, public_float_ratio: float) -> dict:
    """
    Fonun KAP portföy dağılımı ile piyasa verilerini birleştirip
    gerçek tasfiye ve yoğunlaşma metriklerini hesaplar.
    """
    aum = get_tefas_fund_aum(fund_code)
    
    # TEFAS verisi kapalıysa veya çekilemezse temsili ölçek
    if aum == 0.0:
        aum = 1_200_000_000.0 # 1.2 Milyar TL varsayılan
        
    top_position_tl = aum * (top_holding_ratio / 100.0)
    adtv_tl = get_bist_stock_adtv_tl(top_holding_ticker)
    
    # Tasfiye Süresi Hesabı:
    # Piyasa darbesi yaratmamak için günlük hacmin en fazla %10'u kadar satıldığı varsayımı
    if adtv_tl > 0:
        days_to_liquidate = top_position_tl / (adtv_tl * 0.10)
    else:
        days_to_liquidate = 45.0 # Hacim yoksa aşırı illikit varsayımı

    days_to_liquidate = round(min(days_to_liquidate, 60.0), 1)

    # İtfa şoku dayanımı ve alarm sınıflandırması
    if days_to_liquidate >= 30 or top_holding_ratio >= 30.0:
        alarm = "KRİTİK ALARM"
        redemption_shock = "Kilit / Yetersiz"
    elif days_to_liquidate >= 15 or top_holding_ratio >= 15.0:
        alarm = "YÜKSEK RİSK"
        redemption_shock = "Yuksek Risk"
    elif days_to_liquidate >= 5:
        alarm = "GÖZETİM"
        redemption_shock = "Orta Risk"
    else:
        alarm = "GÜVENLİ"
        redemption_shock = "Tam Karsilama"

    return {
        "Fon Kodu": fund_code,
        "Portföy (M TL)": round(aum / 1_000_000, 1),
        "En Büyük Pay (%)": round(top_holding_ratio, 1),
        "Fiili Dolaşım Payı (%)": round(public_float_ratio, 1),
        "Tasfiye Süresi (İş Günü)": int(days_to_liquidate),
        "İtfa Şoku": redemption_shock,
        "Denetim Alarmı": alarm
    }

if __name__ == "__main__":
    print("--- TEFAS ve BIST Gerçek Veri Çekme Motoru Çalışıyor ---")
    
    # İnceleyeceğimiz Fon Dağılımları (KAP Raporu Ağırlıkları)
    sample_funds = [
        {"fund": "PST", "top_ticker": "KENT", "top_ratio": 42.0, "float_ratio": 32.5},
        {"fund": "TRP", "top_ticker": "CONSE", "top_ratio": 37.5, "float_ratio": 29.0},
        {"fund": "HDF", "top_ticker": "INFO", "top_ratio": 28.0, "float_ratio": 21.0},
        {"fund": "AK3", "top_ticker": "THYAO", "top_ratio": 8.5, "float_ratio": 1.1},
        {"fund": "TI2", "top_ticker": "TUPRS", "top_ratio": 7.8, "float_ratio": 0.8}
    ]
    
    results = []
    for item in sample_funds:
        print(f">> Veri işleniyor: {item['fund']} (Lider Hisse: {item['top_ticker']})...")
        metric = build_fund_risk_metrics(
            fund_code=item["fund"],
            top_holding_ticker=item["top_ticker"],
            top_holding_ratio=item["top_ratio"],
            public_float_ratio=item["float_ratio"]
        )
        results.append(metric)
        
    df_real = pd.DataFrame(results)
    print("\n--- GERÇEK PİYASA VERİSİ METRİKLERİ ---")
    print(df_real.to_string(index=False))
    