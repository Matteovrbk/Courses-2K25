"""
Exemple 2.2 — Graphique de la consommation avec pandas + matplotlib
====================================================================
Extension de l'exemple 2.1 : affichage des données sous forme de graphique
à l'aide des fonctions intégrées de pandas (qui utilise matplotlib en arrière-plan).
"""

from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt
from config import API_TOKEN

# ─── Initialisation du client ─────────────────────────────────────────────────
client = EntsoePandasClient(api_key=API_TOKEN)

# ─── Paramètres ───────────────────────────────────────────────────────────────
country_code = "BE"
start_date   = pd.Timestamp("20230303", tz="Etc/Universal")
end_date     = pd.Timestamp("20230306", tz="Etc/Universal")

# ─── Récupération des données ─────────────────────────────────────────────────
data = client.query_load(country_code, start=start_date, end=end_date)

# ─── Affichage du graphique ───────────────────────────────────────────────────
plt.close("all")
data.plot()
plt.legend(loc="best")
plt.title("Belgian electrical consumption")
plt.xlabel("Date / Heure")
plt.ylabel("Puissance (MW)")
plt.tight_layout()
plt.show()
