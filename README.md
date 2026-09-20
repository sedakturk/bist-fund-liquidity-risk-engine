# BIST Mutual Funds Liquidity & Concentration Risk Engine

Borsa İstanbul ve TEFAS fon ekosisteminde yaşanan likidite ve itfa (redemption run) krizlerini modelleyen, **Portföy Yoğunlaşması** ve **Tasfiye Süresi (Days-to-Liquidate)** analitiği sunan açık kaynaklı risk denetim motoru.

![Fund Risk Scorecard](fund_risk_scorecard.png)

---

## 🎯 Projenin Amacı

Yatırım fonlarında kriz dönemlerinde yaşanan tıkanmalar genellikle salt "fiyat düşüşü"nden değil, **fiziksel likidite yetersizliğinden** kaynaklanır. Bir fon, işlem hacmi düşük ve fiili dolaşımı kısıtlı hisse senetlerinde aşırı yoğunlaştığında, olası bir ani itfa dalgasında piyasa darbesi (market impact) yaratmadan pozisyonlarını nakde çeviremez.

Bu motor:
1. Bir portföyün tek hissede veya ilişkili varlıklarda yarattığı yoğunlaşmayı ölçer.
2. Pozisyon büyüklüğünü Borsa İstanbul'daki **gerçekleşen ortalama günlük işlem hacmine (ADTV)** oranlayarak piyasayı bozmadan kaç iş gününde çıkılabileceğini (`Days-to-Liquidate`) hesaplar.
3. Fonların itfa şoku dayanımını test eden bir **Risk Denetim Karnesi** üretir.

---

## ⚙️ Metodoloji

### 1. Tasfiye Süresi (Days-to-Liquidate - DTL)
Fonun elindeki pozisyonu, piyasa fiyatını taban yapmamak adına **günlük hacmin en fazla %10'u ile** satabileceği varsayılır:

$$\text{Tasfiye Süresi (Gün)} = \frac{\text{Pozisyon Büyüklüğü (TL)}}{\text{ADTV (30 Günlük Hacim)} \times 0.10}$$

### 2. Yoğunlaşma & Fiili Dolaşım Etkisi
* Portföyün tek bir hissedeki payı > %20 ise yüksek konsantrasyon riski.
* Fonun ilgili şirketin fiili dolaşımdaki hisselerine oranı > %20 ise sistemik kilitlenme ve karşı taraf likidite riski.

---

## 🚀 Hızlı Başlangıç

### Kütüphanelerin Kurulumu
```bash
python3 -m pip install -r requirements.txt
