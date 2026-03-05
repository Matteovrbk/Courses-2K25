# Explications des Labos SI3B

Ce document vise à expliquer de manière très détaillée les concepts abordés dans les laboratoires 1 (Requêtes API) et 2 (Bases de données).

---

## 1. Laboratoire 1 : Requêtes API (ENTSO-E)

### Contexte
Le projet requiert de récupérer des données énergétiques automatiquement plutôt que de les télécharger manuellement sur le site de [transparency.entsoe.eu](https://transparency.entsoe.eu/). Pour ce faire, on utilise une **API (Application Programming Interface)** qui permet à votre script Python de « parler » directement au serveur d’ENTSO-E.

### Concept de "Security Token" (Jeton de sécurité)
Une API n'est généralement pas en accès libre, pour éviter que les serveurs ne soient surchargés. ENTSO-E demande donc un **jeton de sécurité (Security Token)**. C'est comme un passeport ou un badge d'accès. Il faut l'inclure dans chaque requête que vous envoyez, pour prouver que vous êtes autorisé à récupérer les données.

### Méthode 1 : Requête HTTP native (avec `requests`)
C'est la méthode "brute". Vous construisez manuellement un lien (URL) qui contient tous les paramètres de votre demande.

**Anatomie d'une URL de requête HTTP :**
`https://url_de_destination/api?param1=valeur1&param2=valeur2`
- `?` : Indique le début des paramètres.
- `&` : Permet de séparer les différents paramètres.

Dans l'**Exercice 1.1**, on vous demande de récupérer la **Charge électrique (Consommation totale)** de la Belgique le 10 février 2026.
Pour ce faire, via `requests.get()`, on passe un dictionnaire de paramètres (token, type de document "A65" qui correspond à la charge totale, le pays, etc.). L'API répond avec un fichier au format **XML** (un format de balisage ressemblant au HTML). Il faut ensuite "parser" (décortiquer) ce XML pour en extraire les données chiffrées.

*(Voir le code expliqué dans `exo1.1.py`)*

---

### Méthode 2 : Utilisation de la librairie Python `entsoe-py`
La méthode HTTP native (requête brute + parsing XML) est fastidieuse. Heureusement, la communauté a créé une librairie Python nomée `entsoe-py`. C'est une surcouche ("wrapper") qui gère les requêtes HTTP et le décodage du XML automatiquement.

#### Exemple 2.1 (Capacité installée)
Ce script utilise `entsoe-py` pour récupérer les données.

```python
from entsoe import EntsoePandasClient
import pandas as pd

# 1. Création du "client" qui va discuter avec l'API grâce au token
client = EntsoePandasClient(api_key='VOTRE_TOKEN')

# 2. Définition des paramètres
country_code = 'BE' # Code pays
start_date = pd.Timestamp('20230303', tz='Etc/Universal') # Début (Format YYYYMMDD)
end_date = pd.Timestamp('20230306', tz='Etc/Universal')   # Fin

# 3. La magie opère ici : La méthode query_load récupère les données de consommation
# et retourne directement un DataFrame (tableau de données de Pandas, très facile à utiliser).
data = client.query_load(country_code, start=start_date, end=end_date)
print(data)
```
**Explication :** `Pandas` est une puissante librairie Python pour manipuler des tableaux (DataFrames). `EntsoePandasClient` nous évite de gérer le XML et nous livre les données sur un plateau d'argent (un DataFrame).

#### Exemple 2.2 (Affichage graphique)
On reprend la même base que l'Exemple 2.1, mais au lieu de juste faire un `print()`, on utilise la librairie `matplotlib` pour faire un graphique.

```python
import matplotlib.pyplot as plt

# ... (Même code de récupération que l'exemple 2.1) ...

# plt est le module pyplot de matplotlib
plt.close("all") # Ferme les anciennes fenêtres de graphiques s'il y en a
data.plot()      # La méthode .plot() d'un DataFrame Pandas génère automatiquement un graphe basique.
plt.legend(loc='best') # Place la légende au "meilleur" endroit pour ne pas cacher la courbe
plt.title('Belgian electrical consumption') # Titre du graphe
plt.show() # Ouvre la fenêtre pour afficher visuellement le graphe
```

---

## 2. Laboratoire 2 : Database (Modélisation E-A et Relationnelle)

Le laboratoire 2 se concentre sur la conception de bases de données, en passant par deux étapes cruciales avant de toucher au code SQL :
1. **Le Modèle Entité-Association (MCD - Modèle Conceptuel de Données)** : Représentation visuelle des concepts métiers (les "Entités") et de comment ils interagissent ensemble (les "Associations").
2. **Le Schéma Relationnel (MLD - Modèle Logique de Données)** : Traduction du modèle précédent sous forme de tables (colonnes, clés primaires, clés étrangères) prêtes à être implémentées dans un SGBD (comme MySQL, PostgreSQL).

### Les concepts :
- **Entité :** Un objet du monde réel (ex: un Soldat, une Voiture, une Option).
- **Propriétés (Attributs) :** Les caractéristiques d'une entité (ex: Nom du soldat, couleur de la voiture).
- **Identifiant / Clé Primaire (PK) :** Une propriété unique qui identifie sans ambiguïté une instance de l'entité (ex: Matricule National, Numéro de Châssis). On le souligne dans le schéma.
- **Association (Relation) :** Le lien entre deux ou plusieurs entités. Parfois, elle porte elle-même des attributs (ex: la "Date d'obtention" est un attribut de l'association "*obtient*" entre un Soldat et un Grade).
- **Cardinalités :** Indique le minimum et le maximum de fois qu'une entité participe à une association. (ex: 0,N - 1,1).
- **Clé Étrangère (FK) :** Dans le schéma relationnel, lorsqu'une entité "pointe" vers une autre (par exemple une association 1,N vers 1,1 ou 0,1), la table "enfant" (celle du côté 1,1/0,1) reçoit la clé primaire de l'autre table en tant que clé étrangère (souvent notée avec une astérisque ou un `#`).

*(Les exercices du Labo 2 sont résolus dans des fichiers séparés `labo2_exoX.md`)*
