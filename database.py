# Module généré par GenDB.py
#===========================
import sqlite3


def createAllTables():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# prix
	cur.execute('''
			CREATE TABLE IF NOT EXISTS prix
			(
				id_prix INTEGER NOT NULL,
				date TEXT NOT NULL,
				heure TEXT NOT NULL,
				prix REAL NOT NULL,
				PRIMARY KEY (id_prix)
			)
			''')

	# machine
	cur.execute('''
			CREATE TABLE IF NOT EXISTS machine
			(
				id_machine INTEGER NOT NULL,
				nom TEXT NOT NULL,
				puissance REAL NOT NULL,
				operateur_nom TEXT,
				operateur_mail TEXT,
				PRIMARY KEY (id_machine)
			)
			''')

	# commande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS commande
			(
				id_commande INTEGER NOT NULL,
				date TEXT NOT NULL,
				id_produit INTEGER NOT NULL,
				cout_tot REAL NOT NULL,
				heure_debut TEXT,
				heure_fin TEXT,
				PRIMARY KEY (id_commande)
			)
			''')

	# produit
	cur.execute('''
			CREATE TABLE IF NOT EXISTS produit
			(
				id_produit INTEGER NOT NULL,
				nom TEXT NOT NULL,
				PRIMARY KEY (id_produit)
			)
			''')

	# tache
	cur.execute('''
			CREATE TABLE IF NOT EXISTS tache
			(
				id_tache INTEGER NOT NULL,
				duree REAL NOT NULL,
				ordre INTEGER NOT NULL,
				id_produit INTEGER,
				id_machine INTEGER,
				PRIMARY KEY (id_tache),
				FOREIGN KEY (id_produit) REFERENCES produit(id_produit),
				FOREIGN KEY (id_machine) REFERENCES machine(id_machine)
			)
			''')
	conn.commit()
	conn.close()

def createTables_prix():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# prix
	cur.execute('''
			CREATE TABLE IF NOT EXISTS prix
			(
				id_prix INTEGER NOT NULL,
				date TEXT NOT NULL,
				heure TEXT NOT NULL,
				prix REAL NOT NULL,
				PRIMARY KEY (id_prix)
			)
			''')
	conn.commit()
	conn.close()

def createTables_machine():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# machine
	cur.execute('''
			CREATE TABLE IF NOT EXISTS machine
			(
				id_machine INTEGER NOT NULL,
				nom TEXT NOT NULL,
				puissance REAL NOT NULL,
				operateur_nom TEXT,
				operateur_mail TEXT,
				PRIMARY KEY (id_machine)
			)
			''')
	conn.commit()
	conn.close()

def createTables_commande():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# commande
	cur.execute('''
			CREATE TABLE IF NOT EXISTS commande
			(
				id_commande INTEGER NOT NULL,
				date TEXT NOT NULL,
				id_produit INTEGER NOT NULL,
				cout_tot REAL NOT NULL,
				heure_debut TEXT,
				heure_fin TEXT,
				PRIMARY KEY (id_commande)
			)
			''')
	conn.commit()
	conn.close()

def createTables_produit():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# produit
	cur.execute('''
			CREATE TABLE IF NOT EXISTS produit
			(
				id_produit INTEGER NOT NULL,
				nom TEXT NOT NULL,
				PRIMARY KEY (id_produit)
			)
			''')
	conn.commit()
	conn.close()

def createTables_tache():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	# tache
	cur.execute('''
			CREATE TABLE IF NOT EXISTS tache
			(
				id_tache INTEGER NOT NULL,
				duree REAL NOT NULL,
				ordre INTEGER NOT NULL,
				id_produit INTEGER,
				id_machine INTEGER,
				PRIMARY KEY (id_tache),
				FOREIGN KEY (id_produit) REFERENCES produit(id_produit),
				FOREIGN KEY (id_machine) REFERENCES machine(id_machine)
			)
			''')
	conn.commit()
	conn.close()

# INSERT INTO prix
def insert_prix(id_prix,date,heure,prix):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO prix (id_prix,date,heure,prix) "
	sqlQuery+=f"VALUES ({id_prix},'{date}','{heure}',{prix})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO machine
def insert_machine(id_machine,nom,puissance,operateur_nom,operateur_mail):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO machine (id_machine,nom,puissance,operateur_nom,operateur_mail) "
	sqlQuery+=f"VALUES ({id_machine},'{nom}',{puissance},'{operateur_nom}','{operateur_mail}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO commande
def insert_commande(id_commande,date,id_produit,cout_tot,heure_debut,heure_fin):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO commande (id_commande,date,id_produit,cout_tot,heure_debut,heure_fin) "
	sqlQuery+=f"VALUES ({id_commande},'{date}',{id_produit},{cout_tot},'{heure_debut}','{heure_fin}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO produit
def insert_produit(id_produit,nom):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO produit (id_produit,nom) "
	sqlQuery+=f"VALUES ({id_produit},'{nom}')"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# INSERT INTO tache
def insert_tache(id_tache,duree,ordre,id_produit,id_machine):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="INSERT OR IGNORE INTO tache (id_tache,duree,ordre,id_produit,id_machine) "
	sqlQuery+=f"VALUES ({id_tache},{duree},{ordre},{id_produit},{id_machine})"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# SELECT fields FROM prix WHERE condition
def select_prix(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_prix,date,heure,prix FROM prix"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM machine WHERE condition
def select_machine(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_machine,nom,puissance,operateur_nom,operateur_mail FROM machine"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM commande WHERE condition
def select_commande(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_commande,date,id_produit,cout_tot,heure_debut,heure_fin FROM commande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM produit WHERE condition
def select_produit(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_produit,nom FROM produit"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# SELECT fields FROM tache WHERE condition
def select_tache(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="SELECT id_tache,duree,ordre,id_produit,id_machine FROM tache"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	rows = cur.fetchall()
	conn.commit()
	conn.close()
	return rows

# UPDATE prix SET fields=value WHERE condition
def update_prix(id_prix,date,heure,prix,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE prix SET id_prix = {id_prix},date='{date}',heure='{heure}',prix = {prix}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE machine SET fields=value WHERE condition
def update_machine(id_machine,nom,puissance,operateur_nom,operateur_mail,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE machine SET id_machine = {id_machine},nom='{nom}',puissance = {puissance},operateur_nom='{operateur_nom}',operateur_mail='{operateur_mail}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE commande SET fields=value WHERE condition
def update_commande(id_commande,date,id_produit,cout_tot,heure_debut,heure_fin,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE commande SET id_commande = {id_commande},date='{date}',id_produit = {id_produit},cout_tot = {cout_tot},heure_debut='{heure_debut}',heure_fin='{heure_fin}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE produit SET fields=value WHERE condition
def update_produit(id_produit,nom,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE produit SET id_produit = {id_produit},nom='{nom}'"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# UPDATE tache SET fields=value WHERE condition
def update_tache(id_tache,duree,ordre,id_produit,id_machine,WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery=f"UPDATE tache SET id_tache = {id_tache},duree = {duree},ordre = {ordre},id_produit = {id_produit},id_machine = {id_machine}"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM prix WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_prix(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM prix"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM machine WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_machine(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM machine"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM commande WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_commande(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM commande"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM produit WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_produit(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM produit"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DELETE FROM tache WHERE condition 
# ATTENTION : Si pas de condition ("") efface toutes les données de la table !!!
def delete_tache(WHERE):
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DELETE FROM tache"
	if WHERE.strip()!="":
		sqlQuery+=f" WHERE {WHERE}"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE prix
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_prix():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE prix"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE machine
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_machine():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE machine"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE commande
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_commande():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE commande"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE produit
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_produit():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE produit"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()

# DROP TABLE tache
# ATTENTION : cette fonction détruit la table, elle devra (éventuellement) être recréée
def drop_tache():
	conn = sqlite3.connect("voodoo.db")
	cur = conn.cursor()
	sqlQuery="DROP TABLE tache"
	cur.execute(sqlQuery)
	conn.commit()
	conn.close()


def save_prices(prices):
	delete_prix("")
	for i, (timestamp, prix_val) in enumerate(prices.items()):
		date_str = timestamp.strftime("%Y-%m-%d")
		heure_str = timestamp.strftime("%H:%M")
		insert_prix("NULL", date_str, heure_str, float(prix_val))
