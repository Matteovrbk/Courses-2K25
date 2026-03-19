"""
main.py - Point d'entrée de l'application Voodoo Bakery
"""
import sys
import os

# Ajouter le dossier du projet au path
sys.path.insert(0, os.path.dirname(__file__))

def main():
    try:
        from PyQt6.QtWidgets import QApplication
        from PyQt6.QtCore import Qt
    except ImportError:
        print("PyQt6 n'est pas installé.")
        print("Installez-le avec : pip install PyQt6")
        sys.exit(1)

    app = QApplication(sys.argv)
    app.setApplicationName("Voodoo Bakery")
    app.setApplicationVersion("1.0.0")

    # Style global de l'application
    app.setStyle("Fusion")

    from ui.main_window import MainWindow
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
