import pandas as pd
import os
from datetime import datetime

# === Datengrundlage (DAX 40) ===
data = [
    ["Adidas", 40, 40, 20, "Stabil, Nachfrage robust.", 45, 35, 20, "Leichte Erholung bei stabilem Konsum."],
    ["Airbus", 45, 35, 20, "Hohe Auftragslage, stabile Nachfrage.", 50, 30, 20, "Mittelfristig weiter stark dank Luftfahrtsektor."],
    ["Allianz", 38, 42, 20, "Seitwärts mit leicht positivem Ausblick.", 44, 36, 20, "Solide Gewinne, stabile Dividende."],
    ["BASF", 35, 45, 20, "Energiepreise beeinflussen Margen.", 42, 38, 20, "Leicht positiv bei sinkenden Kosten."],
    ["Bayer", 30, 45, 25, "Belastet durch Rechtsrisiken.", 40, 35, 25, "Stabilisierung möglich bei Fortschritten im Umbau."],
    ["Beiersdorf", 40, 40, 20, "Solide Konsumwerte, stabile Nachfrage.", 46, 34, 20, "Defensiver Wert bleibt gefragt."],
    ["BMW", 42, 38, 20, "Stabile Nachfrage, gute Margen.", 48, 32, 20, "Leicht positiv bei starkem Absatz."],
    ["Brenntag", 36, 44, 20, "Stabile Entwicklung, Rohstoffpreise relevant.", 43, 37, 20, "Moderater Aufwärtstrend."],
    ["Commerzbank", 38, 42, 20, "Zinsumfeld stützt Erträge.", 45, 35, 20, "Positiv bei stabilem Zinsniveau."],
    ["Continental", 37, 43, 20, "Automobilsektor schwankt.", 44, 36, 20, "Erholungspotenzial bei stabiler Nachfrage."],
    ["Daimler Truck", 40, 40, 20, "Solide Nachfrage, stabile Produktion.", 46, 34, 20, "Langfristig robust dank Infrastrukturprojekten."],
    ["Deutsche Bank", 39, 41, 20, "Zinsvorteil bleibt Stütze.", 45, 35, 20, "Positiv bei Kostendisziplin."],
    ["Deutsche Börse", 42, 38, 20, "Defensiver Wert mit stabilem Wachstum.", 48, 32, 20, "Profiteur von Marktvolatilität."],
    ["Deutsche Post", 38, 42, 20, "Konsolidierung nach starkem Jahr.", 44, 36, 20, "Stabiler Cashflow, leicht positiv."],
    ["Deutsche Telekom", 45, 35, 20, "Solider defensiver Wert.", 50, 30, 20, "Mittelfristig stabil durch Dividenden."],
    ["E.ON", 40, 40, 20, "Energiepreise stabil.", 46, 34, 20, "Defensiv, aber stetig wachsend."],
    ["Fresenius", 35, 45, 20, "Leichte Erholung möglich.", 42, 38, 20, "Restrukturierung trägt Früchte."],
    ["Fresenius Medical Care", 32, 48, 20, "Unsicheres Umfeld.", 40, 40, 20, "Verbesserte Effizienz könnte stützen."],
    ["GEA", 38, 42, 20, "Industriewert mit stabilem Wachstum.", 45, 35, 20, "Leicht positiv bei stabiler Nachfrage."],
    ["Hannover Rück", 40, 40, 20, "Solide Rückversicherung, stabile Gewinne.", 46, 34, 20, "Stetige Nachfrage, defensiver Wert."],
    ["Heidelberg Materials", 37, 43, 20, "Baumarkt stabilisiert sich.", 44, 36, 20, "Profiteur von Infrastrukturinvestitionen."],
    ["Henkel", 36, 44, 20, "Stabil, aber Konkurrenzdruck.", 43, 37, 20, "Leichte Erholung möglich."],
    ["Infineon", 50, 30, 20, "Chipnachfrage stützt klar.", 55, 25, 20, "Bullish dank Technologietrends."],
    ["Mercedes-Benz", 42, 38, 20, "Starke Margen, gute Absatzlage.", 48, 32, 20, "Solider Ausblick bei Premiumsegment."],
    ["Merck", 45, 35, 20, "Stabiler Pharmasektor.", 50, 30, 20, "Defensiv und wachstumsorientiert."],
    ["MTU Aero Engines", 48, 32, 20, "Luftfahrtsektor robust.", 54, 26, 20, "Langfristig wachstumsstark."],
    ["Münchener Rück", 44, 36, 20, "Defensiv, hohe Dividende.", 50, 30, 20, "Solide Nachfrage nach Rückversicherung."],
    ["Porsche", 40, 40, 20, "Konsolidierung auf hohem Niveau.", 46, 34, 20, "Positiv bei Luxussegmentstärke."],
    ["Qiagen", 38, 42, 20, "Biotech-Sektor ruhig.", 44, 36, 20, "Defensiv, langfristig stabil."],
    ["Rheinmetall", 55, 25, 20, "Stark durch Rüstungsnachfrage.", 60, 20, 20, "Mittelfristig sehr positiv."],
    ["RWE", 42, 38, 20, "Energiewende bleibt Treiber.", 48, 32, 20, "Leicht bullish durch Investitionen."],
    ["SAP", 50, 30, 20, "Technologiewert mit stabilem Wachstum.", 55, 25, 20, "Cloudgeschäft weiter stark."],
    ["Scout24", 40, 40, 20, "Digitale Plattform stabil.", 46, 34, 20, "Positiv bei starkem Immobilienmarkt."],
    ["Siemens", 46, 34, 20, "Breit diversifiziert, stabile Gewinne.", 52, 28, 20, "Langfristig solide Wachstumsstory."],
    ["Siemens Energy", 38, 42, 20, "Schwankend, aber stabilisierend.", 45, 35, 20, "Verbesserte Margen möglich."],
    ["Siemens Healthineers", 44, 36, 20, "Gesundheitssektor stabil.", 50, 30, 20, "Langfristig positiv."],
    ["Symrise", 42, 38, 20, "Stabile Nachfrage im Konsumsektor.", 48, 32, 20, "Defensiver Wachstumswert."],
    ["Volkswagen", 38, 42, 20, "Preisdruck, aber stabile Verkäufe.", 44, 36, 20, "Leichte Erholung möglich."],
    ["Vonovia", 35, 45, 20, "Zinsumfeld belastet Immobilien.", 42, 38, 20, "Leichte Entspannung bei sinkenden Zinsen."],
    ["Zalando", 40, 40, 20, "Volatil, aber stabiler Umsatz.", 46, 34, 20, "Positiv bei steigender Konsumnachfrage."]
]

cols = [
    "Anlageklasse",
    "1-5T_Steigt", "1-5T_Bleibt", "1-5T_Fällt", "Einschätzung_1-5T",
    "2-3W_Steigt", "2-3W_Bleibt", "2-3W_Fällt", "Einschätzung_2-3W"
]

df = pd.DataFrame(data, columns=cols)

# === Differenzen & Sortierung ===
df["Diff_1-5"] = abs(df["1-5T_Steigt"] - df["1-5T_Fällt"])
df["Diff_2-3W"] = abs(df["2-3W_Steigt"] - df["2-3W_Fällt"])
df = df.sort_values(by="Diff_1-5", ascending=False)

# === Datumsspalte hinzufügen (direkt nach Anlageklasse) ===
datum = datetime.now().strftime("%Y-%m-%d")
df.insert(1, "Datum", datum)

# === Alte CSV löschen ===
for f in os.listdir("."):
    if f.startswith("dax40_probabilities_") and f.endswith(".csv"):
        os.remove(f)

# === Neue CSV erzeugen ===
csv_name = f"dax40_probabilities_{datum}.csv"
df.to_csv(csv_name, index=False)

print(f"✅ Neue Datei erstellt: {csv_name}")
