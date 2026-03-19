import requests
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def fetch_belgian_load(security_token):
    # Paramètres définis selon l'énoncé de l'Exercice 1.1
    url = "https://webapi.tp.entsoe.eu/api"
    params = {
        "securityToken":'1b5256a4-4558-41ff-a92b-c1541c16f687',
        "documentType": "A65",              # System Total Load
        "processType": "A16",               # Realised (données réelles)
        "outBiddingZone_Domain": "10YBE----------2", # Code EIC Belgique
        "periodStart": "202601270000",      # 10 Février 2026 à 00:00 UTC
        "periodEnd": "202601272300"         # 10 Février 2026 à 23:00 UTC
    }

    # 1. Exécution de la requête HTTP GET
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Erreur API : {response.status_code}")
        return None

    # 2. Parsing du XML avec gestion du Namespace
    # ENTSO-E utilise des schémas XML spécifiques (urn:iec62325...)
    root = ET.fromstring(response.content)
    ns = {'ns': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}

    data = []
    # Extraction de chaque point de mesure (TimeSeries > Period > Point)
    for ts in root.findall('.//ns:TimeSeries', ns):
        for point in ts.findall('.//ns:Period/ns:Point', ns):
            pos = int(point.find('ns:position', ns).text)
            qty = float(point.find('ns:quantity', ns).text)
            data.append({"Position": pos, "Load_MW": qty})

    # 3. Création du DataFrame
    df = pd.DataFrame(data).sort_values("Position")
    return df

# --- Exécution et Visualisation ---
token = "1b5256a4-4558-41ff-a92b-c1541c16f687"
df_load = fetch_belgian_load(token)

if df_load is not None:
    # Visualisation adaptée Protanope (Haut contraste, bleu profond)
    plt.figure(figsize=(12, 6))
    plt.plot(df_load["Position"], df_load["Load_MW"], color='#004488', linewidth=2, label='Charge réelle (BE)')
    
    plt.title("Charge électrique en Belgique - 10/02/2026 (UTC)", fontsize=14)
    plt.xlabel("Position (Intervalle de 15 min)", fontsize=12)
    plt.ylabel("Puissance $P$ [MW]", fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.legend()
    
    plt.show()
    print(df_load.head())