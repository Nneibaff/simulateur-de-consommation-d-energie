
# Importer les modules nécessaires
import io
import base64
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.units import cm
from flask import send_file, request, Blueprint


pdf_bp = Blueprint('prices', __name__)


@pdf_bp.route('/generate_pdf', methods=['POST'])
def generate_pdf():
    project_name = request.form.get('project_name')
    location_type = request.form.get('location_type')
    luminaire_type = request.form.get('luminaire_type')
    consommation = request.form.get('consommation')
    consommation_led = request.form.get('consommation_led')
    economie = request.form.get('economie')
    coût = request.form.get('coût')
    coût_led = request.form.get('coût_led')
    total_heures_pleines = request.form.get('total_heures_pleines')
    total_heures_creuses = request.form.get('total_heures_creuses')
    graph = request.form.get('graph')


    buffer = io.BytesIO()

    # Créer un document PDF
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Titre du rapport
    title = Paragraph(f"Rapport de Consommation d'Énergie - {project_name}", styles['Title'])
    story.append(title)
    story.append(Spacer(1, 12))

    # Date de génération
    date = Paragraph(f"Date : {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}", styles['Normal'])
    story.append(date)
    story.append(Spacer(1, 24))

    # Section 1 : Résultats de la simulation
    section1_title = Paragraph(f"Résultats de la Simulation pour le remplacement de vos {luminaire_type} pour votre {location_type}", styles['Heading2'])
    story.append(section1_title)
    story.append(Spacer(1, 12))

    # Tableau des résultats
    results_data = [
        ["Consommation actuelle", f"{consommation} kWh/mois"],
        ["Consommation avec LED", f"{consommation_led} kWh/mois"],
        ["Économie potentielle", f"{economie} kWh/mois"],
        ["Coût actuel", f"{coût} €/mois"],
        ["Coût avec LED", f"{coût_led} €/mois"],
        ["Prix économisé", f"{float(coût) - float(coût_led)} €/mois"],
        ["Total heures pleines", f"{total_heures_pleines} heures"],
        ["Total heures creuses", f"{total_heures_creuses} heures"]
    ]
    results_table = Table(results_data, colWidths=[8 * cm, 6 * cm])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    story.append(results_table)
    story.append(Spacer(1, 24))

    # Section 2 : Explications détaillées
    section2_title = Paragraph("Explications Détaillées", styles['Heading2'])
    story.append(section2_title)
    story.append(Spacer(1, 12))

    explications = [
        "Ce rapport présente les résultats de la simulation de consommation d'énergie.",
        "La consommation actuelle est calculée en fonction de la puissance des luminaires, du nombre d'heures d'utilisation et du nombre de luminaires.",
        "En passant aux LED, la consommation est réduite grâce à leur efficacité énergétique supérieure.",
        "Les économies potentielles sont calculées en comparant la consommation actuelle avec celle des LED.",
        "Le coût est estimé en fonction du prix du kWh et de la consommation mensuelle.",
        "Les heures pleines et creuses sont indiquées pour une meilleure compréhension des périodes d'utilisation."
    ]
    for explication in explications:
        p = Paragraph(explication, styles['BodyText'])
        story.append(p)
        story.append(Spacer(1, 6))
    story.append(Spacer(1, 24))

    # Section 3 : Graphique
    section3_title = Paragraph("Graphique de Comparaison", styles['Heading2'])
    story.append(section3_title)
    story.append(Spacer(1, 12))

    # Ajouter le graphique
    graph_data = base64.b64decode(graph.split(',')[1])
    graph_image = Image(io.BytesIO(graph_data), width=18 * cm, height=9 * cm) 
    story.append(graph_image)

    # Générer le PDF
    doc.build(story)
    buffer.seek(0)

    # Retourner le PDF en tant que fichier téléchargeable
    return send_file(buffer, as_attachment=True, download_name="rapport_consommation.pdf", mimetype='application/pdf')
