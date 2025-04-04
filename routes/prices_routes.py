from flask import Blueprint, render_template, request, redirect, url_for, session
from forms.formPrixkwH import FormPrixkWh
# from services.prices_fonctions import load_prices, save_prices


prices_bp = Blueprint('prices', __name__)


    # Page d'administration pour gérer les prix
@prices_bp.route('/pricekWh', methods=['GET', 'POST'])
def pricekWh():
    if 'uid_admin' not in session:
        return redirect(url_for('login'))
    form = FormPrixkWh(request.form)
    if request.method == 'POST': # and form.validate():
        # prices = load_prices()
        # on recupere l'id le plus haut et on ajoute 1 pour le nouvel id
        new_id : int = max([price['idpays'] for price in prices]) + 1 if prices else 1
        # si il y a une virgule dans le prix, on la remplace par un point
        if ',' in form.prix.data:
            prix : float = float(form.prix.data.replace(',', '.'))
        new_price = {
            'idpays': new_id,
            'pays': form.pays.data,
            'prix': prix,
            'devise': form.devise.data
        }

        prices.append(new_price)
        # save_prices(prices)
        return redirect(url_for('pricekWh'))
    # prices = load_prices()
    return render_template('pricekWh.html', form=form, prices=prices)

@prices_bp.route('/pricekWh/update/<int:index>', methods=['POST'])
def pricekWh_update(index):
    if 'uid_admin' not in session:
        return redirect(url_for('login'))
    # prices = load_prices()
    # prices[index]['pays'] = request.form.get('pays')
    # prices[index]['prix'] = float(request.form.get('prix').replace(',', '.'))
    # prices[index]['devise'] = request.form.get('devise')
    # # save_prices(prices)
    return redirect(url_for('pricekWh'))

@prices_bp.route('/pricekWh/delete/<int:index>', methods=['GET'])
def pricekWh_delete(index):
    if 'uid_admin' not in session:
        return redirect(url_for('login'))
    # prices = load_prices()
    # del prices[index]
    # save_prices(prices)
    return redirect(url_for('pricekWh'))

