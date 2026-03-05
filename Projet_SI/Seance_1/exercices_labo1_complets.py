# Installation des dépendances si nécessaire
# pip install requests pandas matplotlib entsoe-py

from entsoe import EntsoePandasClient
import pandas as pd
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

# ==============================================================================
# LABORATOIRE 1 - EXERCICE 1.1 : OBTENTION VIA REQUÊTE HTTP (METHODE BRUTE API)
# ==============================================================================
# But : Obtenir la charge électrique sur le réseau belge (BE) le 10 février 2026.
# On utilise la librairie `requests` pour forger notre url de requête HTTP de A à Z.

def executer_exo_1_1(security_token):
    print("--- DÉBUT EXERCICE 1.1 ---")
    
    # 1. On définit l'URL de base de l'API ENTSO-E (adresse principale)
    url_base = "https://webapi.tp.entsoe.eu/api"
    
    # 2. Paramètres de la requête (comme expliqué dans la doc de l'API)
    parametres_api = {
        "securityToken": security_token,
        "documentType": "A65",              # A65 = "System Total Load" (Charge Totale du système - Consommation)
        "processType": "A16",               # A16 = "Realised" (Données réelles et mesurées, pas des prévisions)
        "outBiddingZone_Domain": "10YBE----------2", # 10YBE----------2 = Code Région EIC pour la Belgique
        # ATTENTION : La documentation demande le format "YYYYMMDDHHMM" pour la date
        # Période demandée : 10 février 2026 de 00:00 à 23:00
        "periodStart": "202602100000",      # Début : 10 Fév 2026, Minuit
        "periodEnd": "202602102300"         # Fin : 10 Fév 2026, 23h00
    }

    # 3. Lancement de la requête HTTP 'GET' avec les paramètres
    # requests va automatiquement construire une URL du style: https://webapi.tp.entsoe.eu/api?securityToken=XXXX&documentType=A65...
    reponse = requests.get(url_base, params=parametres_api)
    
    # 4. Vérification du statut de la requête (200 = Tout s'est bien passé / OK)
    if reponse.status_code != 200:
        print(f"Erreur lors de la requête API. Code HTTP : {reponse.status_code}")
        print("La raison probable est souvent liée au token ou à une mauvaise date/format.")
        return None

    # 5. Parsing (Lecture) du document XML qui est retourné par le serveur de l'API
    # ENTSO-E utilise du XML pour l'instant avec ce point d'accès. Or le XML a des 'espaces de noms' (namespaces).
    racine_xml = ET.fromstring(reponse.content)
    # L'espace de nom (namespace) nécessaire pour pouvoir lire les balises "TimeSeries" et "Point"
    namespace_entsoe = {'ns': 'urn:iec62325.351:tc57wg16:451-6:generationloaddocument:3:0'}

    donnees_extraites = []
    
    # 6. Extraction des points de données : 
    # Le fichier XML contient des balises TimeSeries (Série temporelle) -> Period -> Point (Point de mesure 1, 2, 3...)
    # On cherche tous les blocs "TimeSeries"
    for serie_temporelle in racine_xml.findall('.//ns:TimeSeries', namespace_entsoe):
        # Pour une série donnée, on cherche tous les points de mesure (généralement toutes les 15 minutes = 96 points/jour)
        for point_mesure in serie_temporelle.findall('.//ns:Period/ns:Point', namespace_entsoe):
            numero_position = int(point_mesure.find('ns:position', namespace_entsoe).text)
            quantite_mw = float(point_mesure.find('ns:quantity', namespace_entsoe).text)
            
            # On ajoute ces valeurs sous forme d'un dictionnaire à notre liste
            donnees_extraites.append({
                "Position (1/4 h)": numero_position, 
                "Consommation Totale (MW)": quantite_mw
            })

    # 7. Création finale du DataFrame Pandas avec ces enregistrements 
    dataframe_charge = pd.DataFrame(donnees_extraites).sort_values("Position (1/4 h)")
    
    print("\n[Exo 1.1] Données de consommation pour le 10/02/2026 (Format brut URL) :")
    print(dataframe_charge.head())  # Affichage des 5 premières lignes
    print(f"  --> Nombre total de points : {len(dataframe_charge)}")
    return dataframe_charge


# ==============================================================================
# LABORATOIRE 1 - EXERCICE 2.1 : OBTENTION VIA LA LIBRAIRIE "entsoe-py"
# ==============================================================================
# But : Obtenir les puissances installées par type de producteur en Belgique le 27 janvier 2026
# On utilise cette fois le client `EntsoePandasClient` qui simplifie toute la partie HTTP et XML.

def executer_exo_2_1(security_token):
    print("\n--- DÉBUT EXERCICE 2.1 ---")
    
    # 1. Création du client Pandas en lui passant notre Token
    client = EntsoePandasClient(api_key=security_token)
    
    # 2. Paramètres de la recherche
    code_pays = 'BE'  # Pour la Belgique
    # Note importante sur entsoe-py: Pour obtenir uniquement la valeur au 27 Janvier, 
    # il faut définir une fenêtre qui commence le 27 et se termine le 28.
    date_debut = pd.Timestamp('20260127', tz='Europe/Brussels') # Utilisons le fuseau horaire Belge ou UTC
    date_fin   = pd.Timestamp('20260128', tz='Europe/Brussels')

    try:
        # 3. Requête simplifiée avec `query_installed_generation_capacity`
        # Cette méthode correspond directement au "documentType=A68" de l'API.
        # Pas de HTTP ni parsing XML ! Elle retourne le DataFrame pandas final.
        capacites_installees = client.query_installed_generation_capacity(country_code=code_pays, start=date_debut, end=date_fin)
        
        print("\n[Exo 2.1] Puissances installées par type de production (Belgique, 27/01/2026) :")
        print(capacites_installees) # Affiche les MW par type (Nucléaire, Gaz, Eolien, etc.)
        return capacites_installees

    except Exception as e:
        print(f"Erreur d'exécution de l'exercice 2.1 : {e}")
        return None


# ==============================================================================
# LABORATOIRE 1 - EXERCICE 2.2 : AFFICHAGE GRAPHIQUE DES PRIX DU MARCHÉ
# ==============================================================================
# But : Obtenir le prix du marché de l'électricité zone belge (BE) pour "Aujourd'hui"
# et tracer ce prix sur un graphique en utilisant `matplotlib`.

def executer_exo_2_2(security_token):
    print("\n--- DÉBUT EXERCICE 2.2 ---")
    
    # 1. Initialisation du client
    client = EntsoePandasClient(api_key=security_token)
    
    code_pays = 'BE'  # Belgique
    
    # 2. Nous voulons le prix pour 'Aujourd'hui'. Pour l'exemple, utilisons la date courante.
    # Récupération dynamique de la date d'aujourd'hui
    aujourd_hui = pd.Timestamp.now(tz='Europe/Brussels').normalize() # Force l'heure à 00:00:00
    demain = aujourd_hui + pd.Timedelta(days=1)
    
    print(f"  --> Récupération des prix pour la journée du : {aujourd_hui.strftime('%Y-%m-%d')}")

    try:
        # 3. Requête simplifiée des prix du marché ('Day-ahead Prices').
        # Correspond très probablement au process de marché classique (A44)
        prix_marche = client.query_day_ahead_prices(code_pays, start=aujourd_hui, end=demain)
        
        print("\n[Exo 2.2] Prix spot d'aujourd'hui (EUR/MWh) :")
        print(prix_marche.head())
        
        # 4. Dessin du graphique (Plot) avec Matplotlib.pyplot
        plt.figure(figsize=(10, 5)) # Taille de l'image (largeur x hauteur)
        # La série 'prix_marche' (Série temporelle Pandas) a déjà la date/heure en index (X) et le prix en valeur (Y)
        prix_marche.plot(color='crimson', linewidth=2, marker='o') # Couleur pourpre, épaisseur, petit rond sur chaque point
        
        plt.title(f"Prix de gros de l'Électricité 'Day-Ahead' - BE ({aujourd_hui.strftime('%d/%m/%Y')})")
        plt.xlabel("Heure de la journée (CET)")
        plt.ylabel("Prix (€ / MWh)")
        plt.grid(True, linestyle=':', alpha=0.7) # Ajoute une fine grille en arrière-plan
        plt.tight_layout() # Évite que le texte ne dépasse de l'image
        
        # Attention : `plt.show()` bloque l'exécution du script tant que la fenêtre n'est pas fermée par l'utilisateur!
        # Décommentez pour afficher en vrai :
        # plt.show() 
        print("  --> Affichage graphique (plt.show() simulé).")
        return prix_marche
        
    except Exception as e:
        print(f"Erreur d'exécution de l'exercice 2.2 : {e}")
        return None

# ==============================================================================
# BLOC PRINCIPAL : LANCEMENT DE TOUS LES EXERCICES
# ==============================================================================
if __name__ == "__main__":
    # N'oubliez pas d'utiliser votre propre jeton!
    mon_token_entsoe = '1b5256a4-4558-41ff-a92b-c1541c16f687'
    
    # Exo 1.1
    executer_exo_1_1(mon_token_entsoe)
    
    # Exo 2.1
    executer_exo_2_1(mon_token_entsoe)
    
    # Exo 2.2
    executer_exo_2_2(mon_token_entsoe)
    
    print("\n=== Exécution de tous les exercices du Labo 1 Terminée ===")
