import yfinance as yf
import pandas as pd
from datetime import datetime
import ta
import numpy as np
import time

# === DAX40-Ticker (Yahoo) ===
tickers = {
    "Adidas": "ADS.DE",
    "Airbus": "AIR.DE",
    "Allianz": "ALV.DE",
    "BASF": "BAS.DE",
    "Bayer": "BAYN.DE",
    "Beiersdorf": "BEI.DE",
    "BMW": "BMW.DE",
    "Brenntag": "BNR.DE",
    "Commerzbank": "CBK.DE",
    "Continental": "CON.DE",
    "Daimler Truck": "DTG.DE",
    "Deutsche Bank": "DBK.DE",
    "Deutsche Börse": "DB1.DE",
    "Deutsche Post": "DPW.DE",
    "Deutsche Telekom": "DTE.DE",
    "E.ON": "EOAN.DE",
    "Fresenius": "FRE.DE",
    "Fresenius Medical Care": "FME.DE",
    "GEA": "GEA.DE",
    "Hannover Rück": "HNR1.DE",
    "Heidelberg Materials": "HEI.DE",
    "Henkel": "HEN3.DE",
    "Infineon": "IFX.DE",
    "Mercedes-Benz": "MBG.DE",
    "Merck": "MRK.DE",
    "MTU Aero Engines": "MTX.DE",
    "Münchener Rück": "MUV2.DE",
    "Porsche": "PAH3.DE",
    "Qiagen": "QIA.DE",
    "Rheinmetall": "RHM.DE",
    "RWE": "RWE.DE",
    "SAP": "SAP.DE",
    "Scout24": "S24.DE",
    "Siemens": "SIE.DE",
    "Siemens Energy": "ENR.DE",
    "Siemens Healthineers": "SHL.DE",
    "Symrise": "SY1.DE",
    "Volkswagen": "VOW3.DE",
    "Vonovia": "VNA.DE",
    "Zalando": "ZAL.DE"
}

datum = datetime.now().strftime("%Y-%m-%d")
results = []

def compute_probabilities(df):
    """Berechnet Wahrscheinlichkeiten aus RSI & gleitenden Durchschnitten"""
    latest_close = df['Close'].iloc[-1]
    ma5 = df['Close'].rolling(window=5).mean().iloc[-1]
    ma20 = df['Close'].rolling(window=20).mean().iloc[-1]
    rsi = ta.momentum.RSIIndicator(df['Close'], window=14).rsi().iloc[-1]

    # 1–5 Tage
    if latest_close > ma5:
        prob_up_short = 55 + (rsi-50)/2
    else:
        prob_up_short = 45 - (50-rsi)/2
    prob_up_short = np.clip(prob_up_short, 20, 80)
    prob_down_short = 100 - prob_up_short - 15
    prob_stable_short = 15

    # 2–3 Wochen
    if latest_close > ma20:
        prob_up_mid = 55 + (rsi-50)/2
    else:
        prob_up_mid = 45 - (50-rsi)/2
    prob_up_mid = np.clip(prob_up_mid, 20, 80)
    prob_down_mid = 100 - prob_up_mid - 20
    prob_stable_mid = 20

    return prob_up_short, prob_stable_short, prob_down_short, prob_up_mid, prob_stable_mid, prob_down_mid, rsi

# === Funktion, die Daten einmal versucht, bei Fehlern wiederholt ===
def fetch_data(ticker, retries=3, wait_sec=2):
    for attempt in range(retries):
        try:
            tk = yf.Ticker(ticker)
            df_price = tk.history(period="1mo", interval="1d")
            if not df_price.empty and 'Close' in df_price.columns:
                return df_price
            else:
                print(f"⚠️ Leere Daten für {ticker}, Versuch {attempt+1}/{retries}")
        except Exception as e:
            print(f"⚠️ Fehler beim Abrufen von {ticker}: {e}, Versuch {attempt+1}/{retries}")
        time.sleep(wait_sec)
    return pd.DataFrame()  # Rückgabe eines leeren DataFrames bei allen Fehlschlägen

# === Daten sammeln ===
for name, ticker in tickers.items():
    df_price = fetch_data(ticker)
    if df_price.empty:
        print(f"⚠️ Keine Daten für {name} nach {3} Versuchen, Platzhalter werden gesetzt.")
        s1, s2, s3 = 33.3, 33.3, 33.4
        w1, w2, w3 = 33.3, 33.3, 33.4
        rsi = None
        change_5d = None
        change_15d = None
    else:
        s1, s2, s3, w1, w2, w3, rsi = compute_probabilities(df_price)
        change_5d = (df_price['Close'].iloc[-1] - df_price['Close'].iloc[-5])/df_price['Close'].iloc[-5]*100 if len(df_price) >=6 else None
        change_15d = (df_price['Close'].iloc[-1] - df_price['Close'].iloc[-15])/df_price['Close'].iloc[-15]*100 if len(df_price) >=16 else None

    results.append([
        name, datum,
        round(s1,1), round(s2,1), round(s3,1), "Kurzfristige Tendenz",
        round(w1,1), round(w2,1), round(w3,1), "Mittelfristige Tendenz",
        round(rsi,1) if rsi else None,
        round(change_5d,2) if change_5d else None,
        round(change_15d,2) if change_15d else None,
        abs(round(s1-s3,1)),
        abs(round(w1-w3,1))
    ])

# === DataFrame & Sortierung nach Diff_1-5 ===
cols = [
    "Aktie","Datum",
    "1-5T_Steigt","1-5T_Bleibt","1-5T_Fällt","Einschätzung_1-5T",
    "2-3W_Steigt","2-3W_Bleibt","2-3W_Fällt","Einschätzung_2-3W",
    "RSI","5T_Change(%)","15T_Change(%)","Diff_1-5","Diff_2-3W"
]
df_result = pd.DataFrame(results, columns=cols)
df_result = df_result.sort_values(by="Diff_1-5", ascending=False)

# === CSV speichern ===
csv_name = f"dax40_complete_retry_{datum}.csv"
df_result.to_csv(csv_name, index=False)
print(f"✅ Datei erstellt: {csv_name} mit {len(df_result)} Einträgen")
