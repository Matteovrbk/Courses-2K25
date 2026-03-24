from database import *
from api_energie import *
import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def calcfun(id_produit, heure_debut, date, prices_series, db_path):

    taches = get_all_taches(db_path, id_produit)
    
    current_time = datetime.strptime(f"{date} {heure_debut}", "%Y-%m-%d %H:%M")
    
    totalcost = 0
    
    for tache in taches:
        id_tache, id_produit, id_machine, ordre, duree_min = tache
        machine = get_machine_by_id(db_path, id_machine)
        puissance = machine[2]   
        
        duree_h = duree_min / 60

        energie = puissance*duree_h/1000
    
        timestamp = pd.Timestamp(current_time, tz="Europe/Brussels")
        prix_MWh = prices_series.asof(timestamp)
        prix = prix_MWh / 1000

        totalcost += prix * energie

        current_time += timedelta(minutes=duree_min)
    
    return totalcost