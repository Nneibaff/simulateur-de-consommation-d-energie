
import matplotlib.pyplot as plt
import io
import base64


# afficher le graphique dans la page
def generate_chart(consommation, consommation_led, coût, coût_led):
    labels = ["installation", "LED"]
    valeurs = [consommation, consommation_led]
    prix_labels = ["Coût", "Coût LED"]
    prix_valeurs = [coût, coût_led]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    # Graphique de consommation
    ax1.bar(labels, valeurs, color=['#FF6347', '#32CD32'])
    ax1.set_ylabel('Consommation (kWh/mois)')
    ax1.set_title('Comparaison de consommation énergétique')
    for i, v in enumerate(valeurs):
        ax1.text(i, v + 0.5, f"{v:.2f}", ha='center', va='bottom')

    # Graphique de coût
    ax2.bar(prix_labels, prix_valeurs, color=['#1E90FF', '#FFD700'])
    ax2.set_ylabel('Coût par mois (€)')
    ax2.set_title('Comparaison des coûts')
    for i, v in enumerate(prix_valeurs):
        ax2.text(i, v + 0.5, f"{v:.2f}", ha='center', va='bottom')

    plt.tight_layout()

    # Fonction pour générer un graphique en base64
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    img_b64 = base64.b64encode(img.getvalue()).decode()
    plt.close(fig)

    return f"data:image/png;base64,{img_b64}"