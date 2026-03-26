from database import *

createAllTables()

insert_machine("NULL", "Four", 5000, "Marie Dupont", "marie@boulangerie.be")
insert_machine("NULL", "Pétrin", 1500, "Jean Leroy", "jean@boulangerie.be")
insert_machine("NULL", "Laminoir", 800, "Jean Leroy", "jean@boulangerie.be")
insert_machine("NULL", "Vitrine", 300, "Marie Dupont", "marie@boulangerie.be")

insert_produit("NULL", "Baguette")
insert_produit("NULL", "Croissant")
insert_produit("NULL", "Pain de campagne")
insert_produit("NULL", "Brioche")

insert_tache("NULL", 15, 1, 1, 2)
insert_tache("NULL", 25, 2, 1, 1)
insert_tache("NULL", 10, 3, 1, 4)

insert_tache("NULL", 20, 1, 2, 2)
insert_tache("NULL", 10, 2, 2, 3)
insert_tache("NULL", 20, 3, 2, 1)
insert_tache("NULL", 10, 4, 2, 4)

insert_tache("NULL", 20, 1, 3, 2)
insert_tache("NULL", 35, 2, 3, 1)
insert_tache("NULL", 10, 3, 3, 4)

insert_tache("NULL", 15, 1, 4, 2)
insert_tache("NULL", 30, 2, 4, 1)
insert_tache("NULL", 10, 3, 4, 4)
