# Méthodologie du Labo 2 : Bases de Données

Ce document explique **comment faire**, étape par étape, pour résoudre les exercices de conception de bases de données tels qu'ils sont présentés dans le Labo 2.

## Étape 1 : Analyser le texte et trouver les Entités
La première étape consiste à lire l'énoncé et en dégager les **Noms** (souvent les sujets principaux de l'énoncé). Ces mots deviendront vos **Entités** (les "boîtes" dans le schéma).
- *Exemple :* "Un **historien** souhaite établir des statistiques sur des **soldats**..." 
  → L'historien est l'utilisateur (pas stocké). Mais "Soldat" est une entité !
- *Exemple :* "La **Croix-Rouge** enregistre ses **véhicules** et ses **volontaires**." 
  → Entités : `Vehicule`, `Volontaire`.

## Étape 2 : Définir les Propriétés (Attributs) et la Clé Primaire
Pour chaque entité trouvée, il faut lui définir ses caractéristiques (les **attributs**).
- *Astuce :* S'il y a un numéro d'identification, un matricule, ou un code barre, c'est votre **Clé Primaire (PK)**. C'est obligatoire.
- *Exemple pour Soldat :* `Matricule` (PK), `Nom`, `Prénom`.

## Étape 3 : Trouver les Associations (Relations)
Identifiez ensuite les **Verbes** qui lient les entités entre elles.
- *Exemple :* Un Soldat **obtient** un Grade.
- *Exemple :* Un Volontaire **participe** à une Intervention.
Ces verbes deviennent les lignes reliant vos entités dans le Diagramme Entité-Association (Schéma E-A). 
Attention, parfois une association possède elle-même un attribut (ex: le soldat obtient un grade *à une certaine date*. Cette date appartient à l'action "Obtenir").

## Étape 4 : Déterminer les Cardinalités
Posez-vous deux questions pour chaque branche du lien :
1. "Combien de fois **au minimum** l'entité A peut participer à la relation ?" (Souvent 0 ou 1)
2. "Combien de fois **au maximum** l'entité A peut participer à la relation ?" (Souvent 1 ou N)
- *Exemple :* Un Volontaire appartient à 1 et 1 seule Unité (Cardinalités : `1,1`). 
- *Exemple :* Une Unité peut accueillir 0, 1 ou N Volontaires (Cardinalités : `0,N`).

## Étape 5 : Transformer en Schéma Relationnel (Base de données SQL)
C'est la partie mathématique finale : "Comment on stocke ça en vrai ?"
Il y a deux grandes règles universelles à retenir pour le relationnel :

1. **Règle des relations 1 à N (Ex: Une unité a plusieurs véhicules)**
   - L'entité qui a le `N` maximum "aspire" la clé primaire de l'autre table en tant que **Clé Étrangère (Foreign Key - FK)**.
   - *Pratique :* La table `VEHICULE` aura une colonne `#ID_Unite`.

2. **Règle des relations N à M (Ex: Un volontaire a plusieurs formations, et une formation compte plusieurs volontaires)**
   - Il est **impossible** de stocker ça dans une seule table sans répéter les données.
   - Il faut créer une **Table de Jointure** (Table intermédiaire).
   - Cette table contiendra les deux clés primaires en tant que Clés Étrangères, et elles formeront ensemble une *Clé Primaire Composée*.
   - *Pratique :* Création d'une table `FORMATION_VOLONTAIRE( #ID_Volontaire, #ID_Formation )`. Si l'association possédait des attributs (comme une date d'obtention de la formation), on la rajoute dans cette table relais.

---
En suivant cette logique pour chaque phrase de vos énoncés, vous arriverez aux mêmes résultats que ceux proposés dans les fichiers exercices !
