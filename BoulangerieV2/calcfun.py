from database import *
from api_energie import *
import pandas as pd
from datetime import datetime, timedelta

def calcfun(id_produit, heure_debut, date, prices_series):
    taches = select_tache(f"id_produit = {id_produit} ORDER BY ordre")
    current_time = datetime.strptime(f"{date} {heure_debut}", "%Y-%m-%d %H:%M")
    totalcost = 0

    for tache in taches:
        id_tache, duree_min, ordre, id_produit_t, id_machine = tache
        machine = select_machine(f"id_machine = {id_machine}")[0]
        puissance = machine[2]

        duree_h = duree_min / 60
        energie = puissance * duree_h / 1000

        timestamp = pd.Timestamp(current_time, tz="Europe/Brussels")
        prix_MWh = prices_series.asof(timestamp)
        prix = prix_MWh / 1000

        totalcost += prix * energie
        current_time += timedelta(minutes=duree_min)

    return totalcost
