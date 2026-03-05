"""
database.py - Gestion de la base de données SQLite pour Voodoo Bakery
"""
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "voodoo_bakery.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    # Table machines
    c.execute("""
        CREATE TABLE IF NOT EXISTS machines (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            puissance_w REAL NOT NULL DEFAULT 0,
            duree_cycle_min INTEGER NOT NULL DEFAULT 0,
            cout_fixe_eur REAL NOT NULL DEFAULT 0,
            operateur_nom TEXT,
            operateur_email TEXT,
            description TEXT
        )
    """)

    # Table produits
    c.execute("""
        CREATE TABLE IF NOT EXISTS produits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nom TEXT NOT NULL,
            description TEXT
        )
    """)

    # Table étapes d'un produit
    c.execute("""
        CREATE TABLE IF NOT EXISTS etapes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produit_id INTEGER NOT NULL,
            ordre INTEGER NOT NULL,
            nom TEXT NOT NULL,
            machine_id INTEGER,
            duree_min INTEGER NOT NULL DEFAULT 0,
            operateur_necessaire INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (produit_id) REFERENCES produits(id) ON DELETE CASCADE,
            FOREIGN KEY (machine_id) REFERENCES machines(id) ON DELETE SET NULL
        )
    """)

    # Table commandes
    c.execute("""
        CREATE TABLE IF NOT EXISTS commandes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            produit_id INTEGER NOT NULL,
            heure_debut TEXT NOT NULL,
            cout_estime_eur REAL,
            validee INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (produit_id) REFERENCES produits(id)
        )
    """)

    # Table seuils d'alerte
    c.execute("""
        CREATE TABLE IF NOT EXISTS seuils_alerte (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            produit_id INTEGER NOT NULL UNIQUE,
            seuil_eur REAL NOT NULL,
            FOREIGN KEY (produit_id) REFERENCES produits(id) ON DELETE CASCADE
        )
    """)

    conn.commit()
    conn.close()
    _insert_demo_data()


def _insert_demo_data():
    """Insère les données de démo boulangerie si la BDD est vide."""
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT COUNT(*) FROM machines")
    if c.fetchone()[0] > 0:
        conn.close()
        return

    # Machines boulangerie
    machines = [
        ("Four à pain",         4500, 60,  0.0,  "Jean Dupont",    "jean.dupont@boulangerie.be",    "Four électrique rotatif 4.5kW"),
        ("Pétrin électrique",   1500, 20,  0.0,  "Marie Lambert",  "marie.lambert@boulangerie.be",  "Pétrin spirale 1.5kW"),
        ("Laminoir à pâte",      750, 10,  0.0,  "Marie Lambert",  "marie.lambert@boulangerie.be",  "Laminoir 750W"),
        ("Chambre de pousse",    200, 90,  0.0,  "Jean Dupont",    "jean.dupont@boulangerie.be",    "Étuve chauffante 200W"),
        ("Machine à café",       800,  5,  0.0,  "Sophie Martin",  "sophie.martin@boulangerie.be",  "Cafetière pro 800W"),
        ("Réfrigérateur pro",    300,  0,  0.0,  "Sophie Martin",  "sophie.martin@boulangerie.be",  "Froid continu 300W"),
    ]
    c.executemany(
        "INSERT INTO machines (nom, puissance_w, duree_cycle_min, cout_fixe_eur, operateur_nom, operateur_email, description) VALUES (?,?,?,?,?,?,?)",
        machines
    )

    # Produits
    produits = [
        ("Baguette tradition",   "Baguette au levain naturel, façonnée à la main"),
        ("Croissant au beurre",  "Croissant feuilleté en beurre AOP"),
        ("Pain de campagne",     "Miche ronde à la farine de seigle"),
        ("Tarte aux pommes",     "Tarte sablée garnie de pommes caramélisées"),
    ]
    c.executemany("INSERT INTO produits (nom, description) VALUES (?,?)", produits)

    conn.commit()

    # Récupérer IDs machines
    c.execute("SELECT id, nom FROM machines")
    mach = {row["nom"]: row["id"] for row in c.fetchall()}
    # Récupérer IDs produits
    c.execute("SELECT id, nom FROM produits")
    prod = {row["nom"]: row["id"] for row in c.fetchall()}

    # Étapes par produit
    etapes = [
        # Baguette tradition
        (prod["Baguette tradition"], 1, "Pétrissage",       mach["Pétrin électrique"],  20, 0),
        (prod["Baguette tradition"], 2, "Pointage (repos)", None,                        60, 0),
        (prod["Baguette tradition"], 3, "Façonnage main",   None,                        15, 1),
        (prod["Baguette tradition"], 4, "Pousse finale",    mach["Chambre de pousse"],   90, 0),
        (prod["Baguette tradition"], 5, "Cuisson",          mach["Four à pain"],          25, 0),

        # Croissant au beurre
        (prod["Croissant au beurre"], 1, "Pétrissage détrempe", mach["Pétrin électrique"],  20, 0),
        (prod["Croissant au beurre"], 2, "Repos froid",         mach["Réfrigérateur pro"],  60, 0),
        (prod["Croissant au beurre"], 3, "Laminage beurre",     mach["Laminoir à pâte"],    20, 1),
        (prod["Croissant au beurre"], 4, "Découpe & façonnage",  None,                       20, 1),
        (prod["Croissant au beurre"], 5, "Pousse",               mach["Chambre de pousse"], 120, 0),
        (prod["Croissant au beurre"], 6, "Cuisson",              mach["Four à pain"],         18, 0),

        # Pain de campagne
        (prod["Pain de campagne"], 1, "Pétrissage seigle",  mach["Pétrin électrique"],  25, 0),
        (prod["Pain de campagne"], 2, "Fermentation",       mach["Chambre de pousse"],  120, 0),
        (prod["Pain de campagne"], 3, "Façonnage miche",    None,                        10, 1),
        (prod["Pain de campagne"], 4, "Pousse finale",      mach["Chambre de pousse"],   60, 0),
        (prod["Pain de campagne"], 5, "Cuisson vapeur",     mach["Four à pain"],          50, 0),

        # Tarte aux pommes
        (prod["Tarte aux pommes"], 1, "Préparation pâte sablée", mach["Pétrin électrique"], 15, 1),
        (prod["Tarte aux pommes"], 2, "Repos pâte au froid",     mach["Réfrigérateur pro"], 30, 0),
        (prod["Tarte aux pommes"], 3, "Étalement pâte",          mach["Laminoir à pâte"],   10, 1),
        (prod["Tarte aux pommes"], 4, "Garniture pommes",         None,                      20, 1),
        (prod["Tarte aux pommes"], 5, "Cuisson tarte",           mach["Four à pain"],        40, 0),
    ]
    c.executemany(
        "INSERT INTO etapes (produit_id, ordre, nom, machine_id, duree_min, operateur_necessaire) VALUES (?,?,?,?,?,?)",
        etapes
    )

    # Seuils d'alerte par défaut
    for pid in prod.values():
        c.execute("INSERT OR IGNORE INTO seuils_alerte (produit_id, seuil_eur) VALUES (?,?)", (pid, 2.0))

    conn.commit()
    conn.close()


# ─── CRUD Machines ───────────────────────────────────────────────────────────

def get_all_machines():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM machines ORDER BY nom").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def add_machine(nom, puissance_w, duree_cycle_min, cout_fixe_eur, operateur_nom, operateur_email, description):
    conn = get_connection()
    conn.execute(
        "INSERT INTO machines (nom,puissance_w,duree_cycle_min,cout_fixe_eur,operateur_nom,operateur_email,description) VALUES (?,?,?,?,?,?,?)",
        (nom, puissance_w, duree_cycle_min, cout_fixe_eur, operateur_nom, operateur_email, description)
    )
    conn.commit()
    conn.close()


def update_machine(id, nom, puissance_w, duree_cycle_min, cout_fixe_eur, operateur_nom, operateur_email, description):
    conn = get_connection()
    conn.execute(
        "UPDATE machines SET nom=?,puissance_w=?,duree_cycle_min=?,cout_fixe_eur=?,operateur_nom=?,operateur_email=?,description=? WHERE id=?",
        (nom, puissance_w, duree_cycle_min, cout_fixe_eur, operateur_nom, operateur_email, description, id)
    )
    conn.commit()
    conn.close()


def delete_machine(id):
    conn = get_connection()
    conn.execute("DELETE FROM machines WHERE id=?", (id,))
    conn.commit()
    conn.close()


# ─── CRUD Produits ────────────────────────────────────────────────────────────

def get_all_produits():
    conn = get_connection()
    rows = conn.execute("SELECT * FROM produits ORDER BY nom").fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_produit_with_etapes(produit_id):
    conn = get_connection()
    produit = dict(conn.execute("SELECT * FROM produits WHERE id=?", (produit_id,)).fetchone())
    etapes = conn.execute(
        """SELECT e.*, m.nom AS machine_nom, m.puissance_w, m.cout_fixe_eur, m.operateur_nom, m.operateur_email
           FROM etapes e
           LEFT JOIN machines m ON e.machine_id = m.id
           WHERE e.produit_id=? ORDER BY e.ordre""",
        (produit_id,)
    ).fetchall()
    produit["etapes"] = [dict(e) for e in etapes]
    conn.close()
    return produit


def add_produit(nom, description):
    conn = get_connection()
    cur = conn.execute("INSERT INTO produits (nom, description) VALUES (?,?)", (nom, description))
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


def update_produit(id, nom, description):
    conn = get_connection()
    conn.execute("UPDATE produits SET nom=?,description=? WHERE id=?", (nom, description, id))
    conn.commit()
    conn.close()


def delete_produit(id):
    conn = get_connection()
    conn.execute("DELETE FROM produits WHERE id=?", (id,))
    conn.commit()
    conn.close()


def add_etape(produit_id, ordre, nom, machine_id, duree_min, operateur_necessaire):
    conn = get_connection()
    conn.execute(
        "INSERT INTO etapes (produit_id,ordre,nom,machine_id,duree_min,operateur_necessaire) VALUES (?,?,?,?,?,?)",
        (produit_id, ordre, nom, machine_id, duree_min, operateur_necessaire)
    )
    conn.commit()
    conn.close()


def delete_etapes_produit(produit_id):
    conn = get_connection()
    conn.execute("DELETE FROM etapes WHERE produit_id=?", (produit_id,))
    conn.commit()
    conn.close()


# ─── Commandes ───────────────────────────────────────────────────────────────

def add_commande(date, produit_id, heure_debut, cout_estime_eur):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO commandes (date, produit_id, heure_debut, cout_estime_eur, validee) VALUES (?,?,?,?,0)",
        (date, produit_id, heure_debut, cout_estime_eur)
    )
    new_id = cur.lastrowid
    conn.commit()
    conn.close()
    return new_id


def get_commandes_du_jour(date):
    conn = get_connection()
    rows = conn.execute(
        """SELECT c.*, p.nom AS produit_nom
           FROM commandes c JOIN produits p ON c.produit_id=p.id
           WHERE c.date=? ORDER BY c.heure_debut""",
        (date,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def valider_commande(commande_id):
    conn = get_connection()
    conn.execute("UPDATE commandes SET validee=1 WHERE id=?", (commande_id,))
    conn.commit()
    conn.close()


def delete_commande(commande_id):
    conn = get_connection()
    conn.execute("DELETE FROM commandes WHERE id=?", (commande_id,))
    conn.commit()
    conn.close()


# ─── Seuils alerte ────────────────────────────────────────────────────────────

def get_seuil(produit_id):
    conn = get_connection()
    row = conn.execute("SELECT seuil_eur FROM seuils_alerte WHERE produit_id=?", (produit_id,)).fetchone()
    conn.close()
    return row["seuil_eur"] if row else None


def set_seuil(produit_id, seuil_eur):
    conn = get_connection()
    conn.execute(
        "INSERT OR REPLACE INTO seuils_alerte (produit_id, seuil_eur) VALUES (?,?)",
        (produit_id, seuil_eur)
    )
    conn.commit()
    conn.close()
