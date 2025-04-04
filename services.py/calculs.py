
# Fonction pour calculer la consommation d’énergie
def calculer_consommation(puissance, heures, nombre, prixkWh, trigger_system, trigger_duration, prixheurescreuses, prixheurespleines, total_heures_pleines, total_heures_creuses):
    consommation = (puissance * heures * nombre * 30) / 1000
    consommation_led = consommation / 6  # Hypothèse : LED consomme 6x moins
    economie = consommation - consommation_led
    
    if trigger_system == 'Interrupteur manuel':
        consommation = consommation * (trigger_duration / 60)
        consommation_led = consommation_led * (trigger_duration / 60)
    
    coût = consommation * prixkWh
    coût_led = consommation_led * prixkWh
    
    if prixheurescreuses and prixheurespleines:
        coût = (total_heures_pleines * prixheurespleines + total_heures_creuses * prixheurescreuses) * (puissance * nombre * 30) / 1000
        coût_led = (total_heures_pleines * prixheurespleines + total_heures_creuses * prixheurescreuses) * (puissance * nombre * 30) / 6000
    
    return consommation, consommation_led, economie, round(coût, 2), round(coût_led, 2)