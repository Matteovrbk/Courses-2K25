"""
Exemple 1.1 — Requête HTTP brute vers l'API ENTSO-E
====================================================
Obtenir la capacité installée par type de producteur en Belgique
le 27/01/2026 à 22h via une requête HTTP directe.

Documentation complète des requêtes :
https://documenter.getpostman.com/view/7009892/2s93JtP3F6#intro
"""

import requests
from config import API_TOKEN, BASE_URL, ZONE_BELGIQUE

# ─── Paramètres de la requête ─────────────────────────────────────────────────
params = {
    "securityToken": 1b5256a4-4558-41ff-a92b-c1541c16f687,
    "documentType":  "A68",           # Installed generation capacity
    "processType":   "A33",           # Day ahead
    "in_Domain":     ZONE_BELGIQUE,
    "periodStart":   "202601272200",  # 27/01/2026 22:00 UTC
    "periodEnd":     "202601272300",  # 27/01/2026 23:00 UTC
}

# ─── Envoi de la requête ──────────────────────────────────────────────────────
response = requests.get(BASE_URL, params=params)

print(f"Statut HTTP : {response.status_code}")
print(f"URL appelée : {response.url}\n")

if response.status_code == 200:
    # La réponse est au format XML
    print(response.text[:2000])  # Affiche les 2000 premiers caractères
else:
    print(f"Erreur : {response.text}")
