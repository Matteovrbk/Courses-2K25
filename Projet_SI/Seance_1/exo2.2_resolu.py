# ==============================================================================
# LABORATOIRE 1 - EXERCICE 2.2 : PRIX DU MARCHÉ ET GRAPHIQUE
# ==============================================================================
# But : Obtenir le prix du marché de l'électricité (Day-Ahead) en Belgique 
# pour "Aujourd'hui" et tracer le graphique avec matplotlib.

from entsoe import EntsoePandasClient
import pandas as pd
import matplotlib.pyplot as plt

def draw_market_prices(security_token):
    print("\n--- DÉBUT EXERCICE 2.2 ---")
    
    # 1. Création de notre point d'accès API
    client = EntsoePandasClient(api_key=security_token)
    
    # 2. Paramètres de recherche
    code_pays = 'BE'  # Zone Belgique
    
    # Automatisation de la date d'aujourd'hui grâce a Pandas
    aujourd_hui = pd.Timestamp.now(tz='Europe/Brussels').normalize() # Force l'heure à minuit pilingue
    demain = aujourd_hui + pd.Timedelta(days=1)
    
    print(f"Récupération des prix prévisionnels (Day-Ahead) pour {aujourd_hui.strftime('%d/%m/%Y')}...")

    try:
        # 3. Interrogation (Méthode dédiée 'query_day_ahead_prices')
        prix_marche = client.query_day_ahead_prices(code_pays, start=aujourd_hui, end=demain)
        
        print("\n[Exo 2.2] Premières valeurs (Prix en EUR/MWh) :")
        print(prix_marche.head())
        
        # 4. Affichage Visuel (Graphique)
        plt.figure(figsize=(10, 5)) 
        
        # On trace le graphe rouge avec des petits points aux marqueurs
        prix_marche.plot(color='firebrick', linewidth=2, marker='.') 
        
        plt.title(f"Prix de gros de l'Électricité 'Day-Ahead' - Belgique ({aujourd_hui.strftime('%d/%m/%Y')})")
        plt.xlabel("Heure (Europe/Brussels)")
        plt.ylabel("Prix Spot [€ / MWh]")
        
        # Quadrillage pour lire les prix facilement
        plt.grid(True, linestyle=':', alpha=0.7) 
        plt.tight_layout() # Optimisation de l'affichage
        
        print("Génération du graphique OK. Décommentez `plt.show()` pour le voir.")
        
        # [!] plt.show() met le programme en pause jusqu'à ce qu'on ferme la fenêtre.
        # plt.show() 
        
        return prix_marche
        
    except Exception as e:
        print(f"Erreur d'exécution de l'exercice 2.2 : {e}")
        print("L'API peut ne pas avoir publié les prix pour cette date ou le token est invalide.")
        return None

# --- Exécution ---
if __name__ == "__main__":
    mon_token = "1b5256a4-4558-41ff-a92b-c1541c16f687"
    draw_market_prices(mon_token)
