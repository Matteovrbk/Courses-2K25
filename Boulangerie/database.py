import sqlite3


def init_database(db_path="voodoo.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS produit(id_produit INTEGER PRIMARY KEY NOT NULL, nom TEXT NOT NULL);
        CREATE TABLE IF NOT EXISTS commande(id_commande INTEGER PRIMARY KEY NOT NULL, date TEXT NOT NULL, id_produit INTEGER NOT NULL, heure_debut TEXT, cout_tot REAL NOT NULL);
        CREATE TABLE IF NOT EXISTS machine(id_machine INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT NOT NULL, puissance REAL NOT NULL, operateur_nom TEXT , operateur_mail TEXT);
        CREATE TABLE IF NOT EXISTS tache(id_tache INTEGER PRIMARY KEY NOT NULL, id_produit INT REFERENCES produit(id_produit), id_machine INT REFERENCES machine(id_machine), ordre INTEGER NOT NULL, duree REAL NOT NULL);
    """)

    conn.commit()
    conn.close()

def add_machine(db_path, nom, puissance, operateur_nom, operateur_mail):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO machine (nom, puissance, operateur_nom, operateur_mail) VALUES (?, ?, ?, ?)",
        (nom, puissance, operateur_nom, operateur_mail)
    )
    conn.commit()
    conn.close()

def add_product(db_path,nom):
    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO produit (nom) VALUES (?)",
        (nom,)
    )
    conn.commit()
    conn.close()

def get_all_machines(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM machine")
    machines = cursor.fetchall()
    conn.close()
    return machines

def get_all_produits(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produit")
    produit = cursor.fetchall()
    conn.close()
    return produit

def delete_machine(db_path, id_machine):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Machine WHERE id_machine = ?,")
    conn.commit()
    conn.close()
    return 