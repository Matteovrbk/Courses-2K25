# Guide de Réalisation du Projet "Voodoo" (SI3B - 3BM)

Ce document explique pas à pas comment concevoir et implémenter le démonstrateur (PoC) demandé par la startup Voodoo, en liant chaque fonctionnalité du cahier des charges aux concepts vus dans vos cours (Cours 1 à 5).

---

## 1. Compréhension du Projet et de l'Information (Cours 1)
Le but est de créer un **Système d'Information (SI)** complet capable de *collecter* des données (via API), de les *stocker* (Base de données locale), de les *traiter* (Algorithme de calcul de prix) et de les *transmettre* (Envoi d'e-mails).
Selon la pyramide **DICS** (Données, Information, Connaissance, Sagesse) abordée au Cours 1 :
- **Données** : Les prix de l'électricité bruts (ex: 45€/MWh à 14h), les puissances des machines (ex: 7000W).
- **Information** : Le prix formaté et associé à un intervalle temporel, le coût d'utilisation d'une machine spécifique.
- **Connaissance / Sagesse** : Le programme tire des conclusions de ces données pour planifier la production au moment le moins coûteux et automatise les actions.

*Note sur l'IA (Cours 1)* : Vous pouvez utiliser ChatGPT ou Copilot pour vous aider à écrire des fonctions Python spécifiques, mais **vous** devez concevoir l'architecture globale et les schémas de base de données.

---

## 2. Modélisation et Stockage des Données (Cours 2 et 3)
*Cahier des charges : "L'application doit stocker la configuration (machines, processus, opérateurs) de façon persistante."*

### A. Pourquoi une Base de Données ? 
Plutôt que d'utiliser un fichier texte complexe, vous allez utiliser une base de données relationnelle en local (**SQLite**). Elle est parfaite pour ce cas car elle tient dans un seul fichier, ne nécessite pas de serveur, et est directement intégrable en Python.

### B. Schéma Entité-Association (MCD)
Il faut d'abord définir vos entités.
- Entité **Machine** : `ID` (PK), `Nom`, `Puissance`, `Durée`, `#ID_Operateur` (FK).
- Entité **Opérateur** : `ID` (PK), `Nom`, `Email`.
- Entité **Produit / Process** : `ID` (PK), `Nom`.
- **Associations** : Un processus utilise plusieurs machines, et une machine peut être dans plusieurs processus (Relation N-M). Il faut donc une table de jointure (ex: `Etape_Process`) qui contient le `#ID_Process`, le `#ID_Machine`, et son *ordre/moment d'utilisation*.

### C. Implémentation SQL / ORM
Pour créer ces tables dans SQLite, deux choix s'offrent à vous :
1. **SQL Brut** : Ecrire des `CREATE TABLE...`, utiliser la bilbiothèque native `sqlite3` de Python avec des `cursor.execute("SELECT...")`.
2. **Utiliser un ORM (Object-Relational Mapping)** : Comme SQLAlchemy (si abordé/autorisé). C'est plus maintenable (Cours 3).
*Astuce* : Utilisez **DB Browser for SQLite** pour visualiser et déboguer vos tables et données.

---

## 3. Communication réseau et API ENTSO-E (Cours 4)
*Cahier des charges : "Aller chercher automatiquement le prix de l'électricité et l'afficher."*

Votre système d'information doit communiquer avec le monde extérieur (L'architecture Client-Serveur).
- **Le Protocole HTTP(S)** : Vous allez faire une requête de type **GET** vers le serveur de l'API ENTSO-E.
- **L'API Client (entsoe-py)** : Plutôt que de forger l'URL "à la main" en insérant vos paramètres (`?securityToken=...`), vous pouvez utiliser le wrapper `entsoe-py`. Ce module agit comme pont (API Client) qui simplifie les appels et convertit le résultat XML du serveur directement en tableaux Python (DataFrames `pandas`).
- **Affichage** : Avec la bibliothèque `pandas` (mentionnée implicitement dans l'utilisation de DataFrames) et `matplotlib`, vous pourrez très facilement générer le tracé du prix de l'électricité de la journée.

---

## 4. Algorithme de Calcul (Cœur du Métier)
*Cahier des charges : "Estimer le prix total d'une commande selon l'heure de départ."*

En Python, votre logique devra :
1. Récupérer l'heure de démarrage demandée par l'utilisateur.
2. Tirer de la BDD SQLite les étapes successives du process choisi, avec les durées et puissances des machines impliquées.
3. Croiser ces tranches horaires avec le graphique des prix extraits de l'API ENTSO-E. *(Attention aux conversions : les puissances sont en W ou kW, le prix est souvent en €/MWh !)* 
4. Sommer le coût énergétique de chaque tranche pour obtenir le total.

**Dépassement potentiel** : Créer une boucle qui teste toutes les "heures de départ" possibles sur la journée, et sélectionne automatiquement celle dont le coût calculé est le plus faible.

---

## 5. Automatisation des Alertes par E-mail (Cours 5)
*Cahier des charges : "Envoyer un mail aux opérateurs selon le planning, et alerter de prix négatifs."*

Vous devrez configurer un client mail en Python utilisant le protocole **SMTP** (Simple Mail Transfer Protocol, sur le port 587 avec TLS pour la sécurité). 
- **Les acteurs** : Le MUA (votre script Python) envoie un courrier au serveur SMTP (ex: celui de l'ECAM ou Gmail), qui l'acheminera à l'adresse de l'opérateur tirée depuis votre base de données SQLite.
- **Implémentation** : Utilisez le module natif `smtplib` et `email.message.EmailMessage`. 
- **Application** : 
  1. Dès que le calcul est lancé et affiche un prix négatif, déclenchez l'appel SMTP pour alerter l'admin.
  2. Dès le process planifié, exécutez une requête SQL `SELECT email FROM operateur JOIN ...` et mettez le résultat dans le champ "To:" de la librairie SMTP pour envoyer les directives.

---

## Synthèse du Plan d'Action (Les 6 Séances)

| Étape | Action Technologique | Fait appel au... |
|-------|----------------------|------------------|
| **1.** | Test de l'API ENTSOE et graphiques (`pandas`, `matplotlib`). | Cours 4 (API, HTTP) |
| **2.** | Création sur papier du modèle MCD (Entités/Associations) des Commandes, Machines et Opérateurs. | Cours 2 (Bases de données) |
| **3.** | Écriture des requêtes `CREATE TABLE` et `INSERT` pour SQLite. | Cours 3 (SQL) |
| **4.** | Assemblage dans une application Python avec une interface (PyQt). | Intégration globale |
| **5.** | Ajout du module `smtplib` pour l'automatisation des envois d'e-mails. | Cours 5 (SMTP) |
| **6.** | Vérifications, tests croisés et préparation de la défense. | Sécurisation & Optimisation |
