"""
Exemple 2.1 — Consommation électrique belge avec entsoe-py
===========================================================
Utilisation de la librairie entsoe-py pour récupérer les données
de consommation (actual load) en Belgique du 03/03/2023 au 06/03/2023
et les afficher dans la console sous forme de DataFrame pandas.

Librairie : https://github.com/EnergieID/entsoe-py
Pandas doc : https://pandas.pydata.org/pandas-docs/stable/user_guide/10min.html
Timezones  : https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
"""

from entsoe import EntsoePandasClient
import pandas as pd
from config import API_TOKEN

# ─── Initialisation du client ENTSO-E ────────────────────────────────────────
client = EntsoePandasClient(api_key=API_TOKEN)

# ─── Définition des paramètres ───────────────────────────────────────────────
country_code = "BE"  # Belgique

# Les dates sont au format YYYYMMDD, tz = fuseau horaire de référence
start_date = pd.Timestamp("20230303", tz="Etc/Universal")
end_date   = pd.Timestamp("20230306", tz="Etc/Universal")

# ─── Récupération des données ─────────────────────────────────────────────────
data = client.query_load(country_code, start=start_date, end=end_date)

# ─── Affichage dans la console ───────────────────────────────────────────────
print("=== Consommation électrique belge (03-06 mars 2023) ===\n")
print(data)
print(f"\nDimensions : {data.shape[0]} lignes x {data.shape[1]} colonne(s)")
