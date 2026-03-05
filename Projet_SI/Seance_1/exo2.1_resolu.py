# ==============================================================================
# LABORATOIRE 1 - EXERCICE 2.1 : OBTENTION VIA LA LIBRAIRIE "entsoe-py"
# ==============================================================================
# But : Obtenir les puissances installées par type de producteur en Belgique 
# le 27 janvier 2026, et les lister dans la console.

from entsoe import EntsoePandasClient
import pandas as pd

def fetch_installed_capacity(security_token):
    print("\n--- DÉBUT EXERCICE 2.1 ---")
    
    # 1. Création du client d'API ENTSO-E (Gère tout le réseau et le XML pour nous)
    client = EntsoePandasClient(api_key=security_token)
    
    # 2. Paramètres géographiques et temporels
    code_pays = 'BE'  # Belgique
    
    # ASTUCE : Pour entsoe-py et les capacités annuelles/journalières, 
    # obtenir la valeur du 27 janvier requiert d'encadrer la date : du 27 au 28.
    date_debut = pd.Timestamp('20260127', tz='Europe/Brussels')
    date_fin   = pd.Timestamp('20260128', tz='Europe/Brussels')

    try:
        print("Interrogation de l'API pour les capacités installées...")
        # 3. Requête simplifiée (Équivalent au documentType=A68)
        capacites = client.query_installed_generation_capacity(
            country_code=code_pays, 
            start=date_debut, 
            end=date_fin
        )
        
        # 4. Affichage des données (Entsoe-py renvoie directement un tableau Pandas)
        print("\n[Exo 2.1] Puissances installées (MW) par type de production :")
        print(capacites)
        return capacites

    except Exception as e:
        print(f"Erreur d'exécution de l'exercice 2.1 : {e}")
        return None

# --- Exécution du Script ---
if __name__ == "__main__":
    # Remplacer par la vraie clé API
    mon_token = "1b5256a4-4558-41ff-a92b-c1541c16f687"
    
    data = fetch_installed_capacity(mon_token)
