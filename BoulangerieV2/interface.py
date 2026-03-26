from PyQt6 import QtWidgets, QtGui
from calcfun import *
from datetime import datetime, timedelta
from graphique import create_price_chart, create_alerte_widget
from database import *
from mailing import send_operator_email
import sys

createAllTables()
today = datetime.now().strftime("%d/%m/%Y")
produits = select_produit("")
machines = select_machine("")

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setWindowTitle("Boulangerie ECAM" + "  " + today)
window.resize(1000, 900)

table_machines = QtWidgets.QTableWidget()
table_machines.setColumnCount(5)
table_machines.setHorizontalHeaderLabels(["ID", "Nom", "Puissance (kW)", "Chef", "Email"])
table_machines.setRowCount(len(machines))
for row, machine in enumerate(machines):
    for col, valeur in enumerate(machine):
        table_machines.setItem(row, col, QtWidgets.QTableWidgetItem(str(valeur)))

table_produits = QtWidgets.QTableWidget()
table_produits.setColumnCount(2)
table_produits.setHorizontalHeaderLabels(["ID", "Nom"])
table_produits.setRowCount(len(produits))
for row, produit in enumerate(produits):
    for col, valeur in enumerate(produit):
        table_produits.setItem(row, col, QtWidgets.QTableWidgetItem(str(valeur)))

input_nom = QtWidgets.QLineEdit()
input_puissance = QtWidgets.QLineEdit()
input_chef = QtWidgets.QLineEdit()
input_email = QtWidgets.QLineEdit()
bouton_ajouter = QtWidgets.QPushButton("Nouvelle machine")
bouton_supprimer_machine = QtWidgets.QPushButton("Supprimer machine")
bouton_supprimer_produit = QtWidgets.QPushButton("Supprimer produit")

input_produit = QtWidgets.QLineEdit()
bouton_produit = QtWidgets.QPushButton("Nouveau produit")

combo_produit_tache = QtWidgets.QComboBox()
for p in produits:
    combo_produit_tache.addItem(p[1], p[0])

combo_machine_tache = QtWidgets.QComboBox()
for m in machines:
    combo_machine_tache.addItem(m[1], m[0])

input_ordre = QtWidgets.QLineEdit()
input_duree = QtWidgets.QLineEdit()
bouton_tache = QtWidgets.QPushButton("Nouvelle tâche")

config_tab = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()

ligne_machines = QtWidgets.QHBoxLayout()

colonne_table_machines = QtWidgets.QVBoxLayout()
colonne_table_machines.addWidget(QtWidgets.QLabel("Machines :"))
colonne_table_machines.addWidget(table_machines)
ligne_machines.addLayout(colonne_table_machines)

colonne_form_machines = QtWidgets.QVBoxLayout()
colonne_form_machines.addWidget(QtWidgets.QLabel("Nom :"))
colonne_form_machines.addWidget(input_nom)
colonne_form_machines.addWidget(QtWidgets.QLabel("Puissance (W) :"))
colonne_form_machines.addWidget(input_puissance)
colonne_form_machines.addWidget(QtWidgets.QLabel("Chef :"))
colonne_form_machines.addWidget(input_chef)
colonne_form_machines.addWidget(QtWidgets.QLabel("Email :"))
colonne_form_machines.addWidget(input_email)
colonne_form_machines.addWidget(bouton_ajouter)
colonne_form_machines.addWidget(bouton_supprimer_machine)
ligne_machines.addLayout(colonne_form_machines)

layout.addLayout(ligne_machines)

ligne_produits = QtWidgets.QHBoxLayout()

colonne_table_produits = QtWidgets.QVBoxLayout()
colonne_table_produits.addWidget(QtWidgets.QLabel("Produits :"))
colonne_table_produits.addWidget(table_produits)
ligne_produits.addLayout(colonne_table_produits)

colonne_form_produits = QtWidgets.QVBoxLayout()
colonne_form_produits.addWidget(QtWidgets.QLabel("Produit :"))
colonne_form_produits.addWidget(input_produit)
colonne_form_produits.addWidget(bouton_produit)
colonne_form_produits.addWidget(bouton_supprimer_produit)
ligne_produits.addLayout(colonne_form_produits)

layout.addLayout(ligne_produits)

layout.addWidget(QtWidgets.QLabel("Tâche - Produit :"))
layout.addWidget(combo_produit_tache)
layout.addWidget(QtWidgets.QLabel("Tâche - Machine :"))
layout.addWidget(combo_machine_tache)
layout.addWidget(QtWidgets.QLabel("Ordre :"))
layout.addWidget(input_ordre)
layout.addWidget(QtWidgets.QLabel("Durée (min) :"))
layout.addWidget(input_duree)
layout.addWidget(bouton_tache)

config_tab.setLayout(layout)

combo_produits = QtWidgets.QComboBox()
for produit in produits:
    combo_produits.addItem(produit[1], produit[0])

input_heure = QtWidgets.QLineEdit()
btn_calculer = QtWidgets.QPushButton("Calculer")
resultat = QtWidgets.QLabel("Coût")

table_commandes = QtWidgets.QTableWidget()
table_commandes.setColumnCount(6)
table_commandes.setHorizontalHeaderLabels(["ID", "Date", "Produit", "Heure début", "Heure fin", "Coût (€)"])

commandes_tab = QtWidgets.QWidget()
layout_commandes = QtWidgets.QVBoxLayout()
layout_commandes.addWidget(QtWidgets.QLabel("Produit :"))
layout_commandes.addWidget(combo_produits)
layout_commandes.addWidget(QtWidgets.QLabel("Heure de départ :"))
layout_commandes.addWidget(input_heure)
layout_commandes.addWidget(btn_calculer)
layout_commandes.addWidget(resultat)
layout_commandes.addWidget(table_commandes)
commandes_tab.setLayout(layout_commandes)

prix_tab = QtWidgets.QWidget()
layout_prix = QtWidgets.QVBoxLayout()
prices = getprice()
save_prices(prices)
layout_prix.addWidget(create_alerte_widget(prices))
layout_prix.addWidget(create_price_chart(prices))
prix_tab.setLayout(layout_prix)

tabs = QtWidgets.QTabWidget()
tabs.addTab(config_tab, "Configuration")
tabs.addTab(commandes_tab, "Commandes")
tabs.addTab(prix_tab, "Prix")
window.setCentralWidget(tabs)


def addmachine():
    nom = input_nom.text()
    puissance = float(input_puissance.text())
    chef = input_chef.text()
    email = input_email.text()
    insert_machine("NULL", nom, puissance, chef, email)
    machines = select_machine("")
    table_machines.setRowCount(len(machines))
    for row, machine in enumerate(machines):
        for col, valeur in enumerate(machine):
            table_machines.setItem(row, col, QtWidgets.QTableWidgetItem(str(valeur)))
    combo_machine_tache.clear()
    for m in machines:
        combo_machine_tache.addItem(m[1], m[0])

def refresh_produits():
    produits = select_produit("")
    combo_produits.clear()
    combo_produit_tache.clear()
    for p in produits:
        combo_produits.addItem(p[1], p[0])
        combo_produit_tache.addItem(p[1], p[0])

def addproduit():
    insert_produit("NULL", input_produit.text())
    refresh_produits()
    produits = select_produit("")
    table_produits.setRowCount(len(produits))
    for r, p in enumerate(produits):
        for c, val in enumerate(p):
            table_produits.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))

def addtache():
    id_produit = combo_produit_tache.currentData()
    id_machine = combo_machine_tache.currentData()
    ordre = int(input_ordre.text())
    duree = float(input_duree.text())
    insert_tache("NULL", duree, ordre, id_produit, id_machine)

def suppmachine():
    row = table_machines.currentRow()
    if row < 0:
        return
    id_machine = int(table_machines.item(row, 0).text())
    delete_machine(f"id_machine = {id_machine}")
    machines = select_machine("")
    table_machines.setRowCount(len(machines))
    for r, machine in enumerate(machines):
        for c, valeur in enumerate(machine):
            table_machines.setItem(r, c, QtWidgets.QTableWidgetItem(str(valeur)))
    combo_machine_tache.clear()
    for m in machines:
        combo_machine_tache.addItem(m[1], m[0])

def suppproduit():
    row = table_produits.currentRow()
    if row < 0:
        return
    id_produit = int(table_produits.item(row, 0).text())
    delete_produit(f"id_produit = {id_produit}")
    table_produits.clearContents()
    produits = select_produit("")
    table_produits.setRowCount(len(produits))
    for r, p in enumerate(produits):
        for c, val in enumerate(p):
            table_produits.setItem(r, c, QtWidgets.QTableWidgetItem(str(val)))
    refresh_produits()

def calculer_cout():
    id_produit = combo_produits.currentData()
    heure = input_heure.text().strip()
    date = datetime.now().strftime("%Y-%m-%d")
    taches = select_tache(f"id_produit = {id_produit} ORDER BY ordre")
    total = 0
    for t in taches:
        total = total + t[1]

    debut = datetime.strptime(date + " " + heure, "%Y-%m-%d %H:%M")
    fin = debut + timedelta(minutes=total)

    if fin.hour == 0 and fin.day != debut.day:
        resultat.setText("Erreur : dépasse la journée")
        return
    if fin.day != debut.day:
        resultat.setText("Erreur : dépasse la journée")
        return

    prices = getprice()
    cout = calcfun(id_produit, heure, date, prices)
    resultat.setText("Coût : " + str(round(cout, 4)) + " €")
    heure_fin = fin.strftime("%H:%M")
    insert_commande("NULL", date, id_produit, cout, heure, heure_fin)

    current_time = debut
    for t in taches:
        id_tache, duree_min, ordre, id_prod, id_mach = t
        machine = select_machine(f"id_machine = {id_mach}")[0]
        op_nom = machine[3]
        op_mail = machine[4]
        heure_tache = current_time.strftime("%H:%M")
        if op_mail and op_mail.strip():
            try:
                send_operator_email(op_mail, op_nom, f"{machine[1]} à {heure_tache} pendant {duree_min} min")
            except Exception:
                QtWidgets.QMessageBox.warning(window, "Erreur mail", f"Impossible d'envoyer le mail à {op_nom} ({op_mail})")
        current_time += timedelta(minutes=duree_min)

    commandes = select_commande("")
    table_commandes.setRowCount(len(commandes))
    for row, c in enumerate(commandes):
        table_commandes.setItem(row, 0, QtWidgets.QTableWidgetItem(str(c[0])))
        table_commandes.setItem(row, 1, QtWidgets.QTableWidgetItem(str(c[1])))
        nom = "?"
        for p in select_produit(""):
            if p[0] == c[2]:
                nom = p[1]
        table_commandes.setItem(row, 2, QtWidgets.QTableWidgetItem(nom))
        table_commandes.setItem(row, 3, QtWidgets.QTableWidgetItem(str(c[4])))
        table_commandes.setItem(row, 4, QtWidgets.QTableWidgetItem(str(c[5])))
        table_commandes.setItem(row, 5, QtWidgets.QTableWidgetItem(str(round(c[3], 4))))




bouton_ajouter.clicked.connect(addmachine)
bouton_supprimer_machine.clicked.connect(suppmachine)
bouton_produit.clicked.connect(addproduit)
bouton_tache.clicked.connect(addtache)
btn_calculer.clicked.connect(calculer_cout)
bouton_supprimer_produit.clicked.connect(suppproduit)

window.show()
sys.exit(app.exec())
