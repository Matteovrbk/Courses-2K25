from PyQt6 import QtWidgets
from PyQt6 import QtWidgets, QtGui
from database import init_database, get_all_machines
from calcfun import *
from datetime import datetime
from database import *
import sys



init_database("voodoo.db")
machines = get_all_machines("voodoo.db")
def addmachine():
    nom = input_nom.text()
    puissance = float(input_puissance.text())
    chef = input_chef.text()
    email = input_email.text()
    add_machine("voodoo.db", nom, puissance, chef, email)

app = QtWidgets.QApplication(sys.argv)
window = QtWidgets.QMainWindow()
window.setWindowTitle("Boulangerie ECAMMMM")
window.setWindowIcon(QtGui.QIcon(r'C:/Users/verbe/Desktop/Projet SI/Picture_with_Mbappé_(cropped)_(cropped).jpg'))
table_machines = QtWidgets.QTableWidget()
table_machines.setColumnCount(5)
table_machines.setHorizontalHeaderLabels(["ID", "Nom", "Puissance (kW)", "Chef", "Email"])


table_machines.setRowCount(len(machines))

for row, machine in enumerate(machines):
    for col, valeur in enumerate(machine):
        table_machines.setItem(row, col, QtWidgets.QTableWidgetItem(str(valeur)))

input_nom = QtWidgets.QLineEdit()
input_puissance = QtWidgets.QLineEdit()
input_chef = QtWidgets.QLineEdit()
input_email = QtWidgets.QLineEdit()
bouton_ajouter = QtWidgets.QPushButton("Nouvelle machine")

config_tab = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
layout.addWidget(QtWidgets.QLabel("Machines :"))
layout.addWidget(table_machines)
layout.addWidget(QtWidgets.QLabel("Nom :"))
layout.addWidget(input_nom)
layout.addWidget(QtWidgets.QLabel("Puissance (W) :"))
layout.addWidget(input_puissance)
layout.addWidget(QtWidgets.QLabel("Chef :"))
layout.addWidget(input_chef)
layout.addWidget(QtWidgets.QLabel("Email :"))
layout.addWidget(input_email)
layout.addWidget(bouton_ajouter)
config_tab.setLayout(layout)

commandes_tab = QtWidgets.QWidget()
layout_commandes = QtWidgets.QVBoxLayout()

combo_produits = QtWidgets.QComboBox()
produits = get_all_produits("voodoo.db")
for produit in produits:
    combo_produits.addItem(produit[1], produit[0])  # nom affiché, id stocké

input_heure = QtWidgets.QLineEdit()

btn_calculer = QtWidgets.QPushButton("Calculer")
resultat = QtWidgets.QLabel("Coût")

layout_commandes.addWidget(QtWidgets.QLabel("Produit :"))
layout_commandes.addWidget(combo_produits)
layout_commandes.addWidget(QtWidgets.QLabel("Heure de départ :"))
layout_commandes.addWidget(input_heure)
layout_commandes.addWidget(btn_calculer)
layout_commandes.addWidget(resultat)
commandes_tab.setLayout(layout_commandes)
bouton_ajouter.clicked.connect(addmachine)
tabs = QtWidgets.QTabWidget()
tabs.addTab(config_tab, "Configuration")
tabs.addTab(commandes_tab, "Commandes")

machines = get_all_machines("voodoo.db")
table_machines.setRowCount(len(machines))
for row, machine in enumerate(machines):
    for col, valeur in enumerate(machine):
        table_machines.setItem(row, col, QtWidgets.QTableWidgetItem(str(valeur)))

window.setCentralWidget(tabs)
def calculer_cout():
    id_produit = combo_produits.currentData()
    heure = input_heure.text().strip()
    date = datetime.now().strftime("%Y-%m-%d")
    
    prices = getprice()
    cout = calcfun(id_produit, heure, date, prices, "voodoo.db")
    
    resultat.setText(f"Coût : {cout:.4f} €")

btn_calculer.clicked.connect(calculer_cout)

window.show()
sys.exit(app.exec())