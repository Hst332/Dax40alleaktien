import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import ta

# DAX40-Ticker (funktionierende Yahoo-Symbole)
dax40_tickers = {
    "Adidas": "ADS.DE", "Airbus": "AIR.DE", "Allianz": "ALV.DE", "BASF": "BAS.DE",
    "Bayer": "BAYN.DE", "Beiersdorf": "BEI.DE", "BMW": "BMW.DE", "Brenntag": "BNR.DE",
    "Commerzbank": "CBK.DE", "Continental": "CON.DE", "Daimler Truck": "DTG.DE",
    "Deutsche Bank": "DBK.DE", "Deutsche Börse": "DB1.DE", "Deutsche Post": "DPW.DE",
    "Deutsche Telekom": "DTE.DE", "E.ON": "EOAN.DE", "Fresenius": "FRE.DE",
    "Fresenius Medical Care": "FME.DE", "GEA": "G1A.DE", "Hannover Rück": "HNR1.DE",
    "Heidelberg Materials": "HEI.DE", "Henkel": "HEN3.DE", "Infineon": "IFX.DE",
    "Mercedes-Benz": "MBG.DE", "Merck": "MRK.DE", "MTU Aero Engines": "MTX.DE",
    "Münchener Rück": "MUV2.DE", "Porsche": "PAH3.DE", "Qiagen": "QIA.DE",
    "Rheinmetall": "RHM.DE", "RWE": "RWE.DE", "SAP": "SAP.DE", "Scout24": "S24.DE",
    "Siemens": "SIE.DE", "Siemens Energy": "ENR.DE", "Siemens Healthineers": "SHL.DE",
    "Symrise": "SY1.DE", "Volkswagen": "VOW3.DE", "Vonovia": "VNA.DE", "Zalando": "ZAL.DE"
}

results = []
datum = datetime.now().strftime("%Y-%m-%d")

for name, ticker in dax40_tickers.items():
    try:
        data = yf.download(ticker, period="1mo", interval="1d", progress=False, auto_adjust=True)
        if data.empty:
            print(f"⚠️ Keine Daten für {name}")
            continue

        rsi = ta.momentum.RSIIndicator(data['Close'], window=14).rsi().iloc[-1]
        change_5d = (data['Close'].iloc[-1] - data['Close'].iloc[-5]) / data['Close'].iloc[-5] * 100
        change_15d = (data['Close'].iloc[-1] - data['Close'].iloc[-15]) / data['Close'].iloc[-15] * 100
        returns = data['Close'].pct_change().dropna()
        volatility = returns.rolling(window=15).std().iloc[-1] * 100

        def calc_probs(change, rsi):
            base_up = 50 + change*2 + (rsi-50)/2
            base_up = max(min(base_up, 90), 10)
            base_down = 100 - base_up - 10
            base_stable = 10
            return round(base_up,1), round(base_stable,1), round(base_down,1)

        prob_1_5T_steigt, prob_1_5T_bleibt, prob_1_5T_faellt = calc_probs(change_5d, rsi)
        prob_2_3W_steigt, prob_2_3W_bleibt, prob_2_3W_faellt = calc_probs(change_15d, rsi)

        def label_prob(up, down):
            if up > down + 10:
                return "Bullish"
            elif down > up + 10:
                return "Bearish"
            else:
                return "Seitwärts"

        einschaetzung_1_5T = label_prob(prob_1_5T_steigt, prob_1_5T_faellt)
        einschaetzung_2_3W = label_prob(prob_2_3W_steigt, prob_2_3W_faellt)
        diff_1_5 = abs(prob_1_5T_steigt - prob_1_5T_faellt)
        diff_2_3W = abs(prob_2_3W_steigt - prob_2_3W_faellt)

        results.append([
            name, datum,
            prob_1_5T_steigt, prob_1_5T_bleibt, prob_1_5T_faellt, einschaetzung_1_5T,
            prob_2_3W_steigt, prob_2_3W_bleibt, prob_2_3W_faellt, einschaetzung_2_3W,
            round(rsi,1), round(change_5d,2), round(change_15d,2), round(volatility,2),
            diff_1_5, diff_2_3W
        ])

    except Exception as e:
        print(f"⚠️ Fehler bei {name}: {e}")

cols = [
    "Aktie","Datum",
    "1-5T_Steigt","1-5T_Bleibt","1-5T_Fällt","Einschätzung_1-5T",
    "2-3W_Steigt","2-3W_Bleibt","2-3W_Fällt","Einschätzung_2-3W",
    "RSI","5T_Change(%)","15T_Change(%)","Volatilität(%)",
    "Diff_1-5","Diff_2-3W"
]

df = pd.DataFrame(results, columns=cols)
df = df.sort_values(by="Diff_1-5", ascending=False)

csv_name = f"dax40_{datum}.csv"
df.to_csv(csv_name, index=False)
print(f"✅ Datei erstellt: {csv_name} mit {len(df)} Einträgen")
