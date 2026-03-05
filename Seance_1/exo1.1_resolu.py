# ==============================================================================
# LABORATOIRE 1 - EXERCICE 1.1 : OBTENTION VIA REQUÊTE HTTP BRUTE (API)
# ==============================================================================
# But : Obtenir la charge électrique sur le réseau belge (BE) le 10 février 2026.
# On utilise la librairie `requests` pour forger l'URL HTTP de A à Z.

import requests
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

def fetch_belgian_load(security_token):
    print("--- DÉBUT EXERCICE 1.1 ---")
    
    # 1. On définit l'URL de base de l'API ENTSO-E
    url_base = "https://webapi.tp.entsoe.eu/api"
    
    # 2. Paramètres de la requête
    parametres = {
        "securityToken": security_token,
        "documentType": "A65",              # A65 = "System Total Load" (Consommation)
        "processType": "A16",               # A16 = "Realised" (Données réelles mesurées)
        "outBiddingZone_Domain": "10YBE----------2", # 10YBE----------2 = Code Région EIC pour la Belgique
        # ATTENTION : La doc exige le format "YYYYMMDDHHMM"
        # 10 Février 2026 de 00:00 à 23:00 UTC
        "periodStart": "202602100000",      
        "periodEnd": "202602102300"         
    }

    # 3. Exécution de la requête HTTP
    print(f"Envoi de la requête à {url_base}...")
    reponse = requests.get(url_base, params=parametres)
    
    # 4. Vérification d'erreur
    if reponse.status_code != 200:
        print(f"Erreur API : {reponse.status_code}")
        print("Vérifiez le token et le format des dates.")
        return None

    # 5. Parsing du document XML (ENTSO-E renvoie un XML avec des "Namespace")
    print("Parsing du XML...")
    racine_xml = ET.fromstring(reponse.content)
    # Espace de nom (namespace) nécessaire pour lire les balises "TimeSeries"
    namespace = {'ns': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}

    donnees = []
    
    # 6. Extraction des points (Toutes les 15 minutes = une balise 'Point')
    for ts in racine_xml.findall('.//ns:TimeSeries', namespace):
        for point in ts.findall('.//ns:Period/ns:Point', namespace):
            position = int(point.find('ns:position', namespace).text)
            quantite_mw = float(point.find('ns:quantity', namespace).text)
            
            donnees.append({"Position": position, "Charge (MW)": quantite_mw})

    # 7. Création du DataFrame final
    df = pd.DataFrame(donnees).sort_values("Position")
    return df

# --- Exécution Normale ---
if __name__ == "__main__":
    # REMPLACEZ CE TOKEN PAR VOTRE VRAI TOKEN (Issu du script 'check_api' ou du site)
    mon_token = "1b5256a4-4558-41ff-a92b-c1541c16f687"
    df_charge = fetch_belgian_load(mon_token)

    if df_charge is not None:
        print("\n[Exo 1.1] 5 premières lignes du résultat :")
        print(df_charge.head())
        print(f"Nombre de points : {len(df_charge)} (Un point par 1/4H)")
        
        # Optionnel: Affichage
        df_charge.plot(x="Position", y="Charge (MW)", title="Consommation Belge - 10 Fev 2026")
        # plt.show() # Décommenter pour afficher la fênetre graphique
