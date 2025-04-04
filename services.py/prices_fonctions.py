
import pandas as pd





# Charger les prix du fichier CSV
def load_prices():
    prices_df = pd.read_csv('static/prices.csv')
    return prices_df.to_dict(orient='records')

# Sauvegarder les prix dans le fichier CSV
def save_prices(prices):
    prices_df = pd.DataFrame(prices)
    prices_df.to_csv('static/prices.csv', index=False)
