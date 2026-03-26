from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt6 import QtWidgets


def create_price_chart(prices):
    fig = Figure(figsize=(10, 5))
    ax = fig.add_subplot()

    valeurs = prices.values
    x = range(len(valeurs))

    ax.plot(x, valeurs, color="steelblue", linewidth=2)

    ticks = range(0, len(valeurs), 4)
    labels = [f"{i // 4}h" for i in ticks]
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)

    ax.set_title("Prix de l'électricité", fontsize=14, fontweight="bold")
    ax.set_ylabel("€/MWh", fontsize=11)
    ax.set_xlabel("Heure", fontsize=11)
    ax.tick_params(axis="x", rotation=45)
    fig.tight_layout()

    canvas = FigureCanvas(fig)
    return canvas


def create_alerte_widget(prices):
    negatifs = prices[prices < 0]

    label = QtWidgets.QLabel()

    if negatifs.empty:
        label.setText("Aucun prix négatif aujourd'hui")
        label.setStyleSheet("color: green; font-size: 14px; padding: 10px;")
    else:
        texte = "ALERTE — Prix négatifs :\n"
        for heure, prix in negatifs.items():
            texte += f"   {heure.strftime('%H:%M')} → {prix:.2f} €/MWh\n"
        label.setText(texte)
        label.setStyleSheet("color: red; font-size: 14px; padding: 10px;")

    return label