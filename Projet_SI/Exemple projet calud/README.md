# 🥐 Voodoo Bakery — Gestion intelligente de l'énergie

**Projet SI3B - 3BM** | Démonstrateur PoC Voodoo®

---

## 📋 Description

Application de gestion de production pour une boulangerie, optimisant les coûts
énergétiques en planifiant les process en fonction des prix de l'électricité sur
le marché de gros (ENTSO-E).

---

## 🚀 Installation

### 1. Prérequis

- Python 3.11 ou supérieur
- pip

### 2. Installation des dépendances

```bash
cd voodoo_bakery
pip install -r requirements.txt
```

### 3. Lancement

```bash
python main.py
```

---

## 🏗 Structure du projet

```
voodoo_bakery/
├── main.py              # Point d'entrée
├── database.py          # Base de données SQLite (CRUD)
├── api.py               # Récupération prix ENTSO-E + calculs coûts
├── mail.py              # Envoi emails automatiques
├── requirements.txt
├── voodoo_bakery.db     # Base de données (créée au premier lancement)
└── ui/
    ├── main_window.py   # Fenêtre principale + thème
    ├── tab_prix.py      # Onglet graphique prix électricité
    ├── tab_machines.py  # Onglet gestion des machines
    ├── tab_produits.py  # Onglet gestion des produits/process
    ├── tab_commandes.py # Onglet commandes du jour
    └── tab_parametres.py# Onglet configuration (SMTP, API)
```

---

## 🎯 Fonctionnalités implémentées

### Fonctionnalités de base (cahier des charges)

| # | Fonctionnalité | Statut |
|---|----------------|--------|
| 1 | Récupération automatique prix ENTSO-E + affichage graphique | ✅ |
| 2 | Interface graphique (onglets Configuration / Commandes) | ✅ |
| 3 | Base de données SQL persistante (SQLite) | ✅ |
| 4 | Estimation du coût par process et total journée | ✅ |
| 5 | Envoi automatique emails aux opérateurs | ✅ |
| 6 | Alerte prix négatifs (graphique + tableau) | ✅ |

### Dépassements implémentés

| Dépassement | Description |
|-------------|-------------|
| 🎯 Optimisation horaire | Trouve automatiquement l'heure de départ à moindre coût |
| ⚠️ Seuils d'alerte | Alerte si le coût de production dépasse un seuil configurable |

---

## 🏭 Données de démonstration (Boulangerie)

### Machines préconfigurées
| Nom | Puissance | Opérateur |
|-----|-----------|-----------|
| Four à pain | 4500 W | Jean Dupont |
| Pétrin électrique | 1500 W | Marie Lambert |
| Laminoir à pâte | 750 W | Marie Lambert |
| Chambre de pousse | 200 W | Jean Dupont |
| Machine à café | 800 W | Sophie Martin |
| Réfrigérateur pro | 300 W | Sophie Martin |

### Produits préconfigurés
1. **Baguette tradition** — Pétrissage → Pointage → Façonnage → Pousse → Cuisson
2. **Croissant au beurre** — Détrempe → Repos froid → Laminage → Façonnage → Pousse → Cuisson
3. **Pain de campagne** — Pétrissage → Fermentation → Façonnage → Pousse → Cuisson vapeur
4. **Tarte aux pommes** — Pâte sablée → Repos → Étalement → Garniture → Cuisson

---

## ⚙️ Configuration

### Clé API ENTSO-E (optionnel)
- Inscrivez-vous sur https://transparency.entsoe.eu/
- Entrez votre clé dans l'onglet **Paramètres**
- Sans clé : données simulées réalistes utilisées automatiquement

### Email (SMTP)
- Compatible Gmail, Outlook, etc.
- Pour Gmail : créez un **mot de passe d'application** (compte Google → Sécurité → Mots de passe d'application)

---

## 🗄 Schéma de la base de données

```
machines (id, nom, puissance_w, duree_cycle_min, cout_fixe_eur, operateur_nom, operateur_email, description)
produits (id, nom, description)
etapes (id, produit_id→produits, ordre, nom, machine_id→machines, duree_min, operateur_necessaire)
commandes (id, date, produit_id→produits, heure_debut, cout_estime_eur, validee)
seuils_alerte (id, produit_id→produits, seuil_eur)
```

---

## 📐 Schéma entité-association

```
MACHINE ─────── ETAPE ─────── PRODUIT ─────── COMMANDE
   1              N:1           1:N               N:1
              (machine_id)   (produit_id)      (produit_id)

PRODUIT ─────── SEUIL_ALERTE
   1:1
```

---

*Développé dans le cadre du cours SI3B — ECAM | Voodoo® PoC Demonstrator*
