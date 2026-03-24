from database import *

DB = "voodoo.db"
init_database(DB)

add_machine(DB, "Four", 5000, "Marie Dupont", "marie@boulangerie.be")
add_machine(DB, "Pétrin", 1500, "Jean Leroy", "jean@boulangerie.be")
add_machine(DB, "Laminoir", 800, "Jean Leroy", "jean@boulangerie.be")
add_machine(DB, "Vitrine", 300, "Marie Dupont", "marie@boulangerie.be")

add_product(DB, "Baguette")
add_product(DB, "Croissant")
add_product(DB, "Pain de campagne")
add_product(DB, "Brioche")