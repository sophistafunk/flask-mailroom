import os
import base64
import logging

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = b'+\x8e\xf6=\xd1\x81\x0c\xfa\xa5\x85[\xfa\x81L|4Z\xb6ABx\xa9\x01f'

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.INFO, format=FORMAT)
logger = logging.getLogger(__name__)


@app.route('/')
def home():
    return redirect(url_for('all'))

@app.route('/donations/')
def all():
    donations = Donation.select()
    return render_template('donations.jinja2', donations=donations)

@app.route('/add', methods=['GET', 'POST'])
def add():
    code = base64.b32encode(os.urandom(8)).decode().strip("=")
    #sessions['donation']

    if 'donor' and 'donation' not in session:
        session['donor'] = ''
        session['donation'] = 0

    if request.method == 'POST':
        try:
            name = request.form['donor']
            #donor = Donor.get_or_create(name=name)[0]
            donor, _ = Donor.get_or_create(name=name) #alternative to the above
            amount = request.form['donation']
            logging.info(f'adding donor: {name} and donation: ${amount}')
            donation = Donation(value=amount, donor=donor)
            donation.save()
        except Exception as e:
            logging.info(f'failed to add {name} and {amount}')
            logging.info(e)
        return redirect(url_for('all'))

    return render_template('add_donations.jinja2', session=session)

@app.route('/lookup', methods=['GET'])
def lookup():
    try:
        name = request.form['donor']
        donor = Donor.get(name=name)
        donations = Donation.get(donor=donor)
        logging.info(donations)
        #donor_output = [donation for donation in donations]
        #logging.info(donor_output)
        #logging.info(session['donation'])
        #return donor_output
    except Exception as e:
        logging.info(e)
    return render_template('get_donations.jinja2')


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)
