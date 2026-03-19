from PyQt6 import QtWidgets
from PyQt6 import QtWidgets, QtGui
from database import init_database, get_all_machines

from database import get_all_machines
import sys

init_database("voodoo.db")
machines = get_all_machines("voodoo.db")


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

config_tab = QtWidgets.QWidget()
layout = QtWidgets.QVBoxLayout()
layout.addWidget(QtWidgets.QLabel("Machines :"))
layout.addWidget(table_machines)
config_tab.setLayout(layout)


tabs = QtWidgets.QTabWidget()
tabs.addTab(config_tab, "Configuration")
tabs.addTab(QtWidgets.QWidget(), "Commandes")


window.setCentralWidget(tabs)


window.show()
sys.exit(app.exec())