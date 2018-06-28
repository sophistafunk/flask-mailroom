import os
import base64

from flask import Flask, render_template, request, redirect, url_for, session

from model import Donation, Donor

app = Flask(__name__)
app.secret_key = b'+\x8e\xf6=\xd1\x81\x0c\xfa\xa5\x85[\xfa\x81L|4Z\xb6ABx\xa9\x01f'

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
        donor = Donor(name=request.form['donor'])
        donor.save()
        donation = Donation(value=request.form['donation'], donor=donor)
        donation.save()
        return redirect(url_for('all'))

    return render_template('add_donations.jinja2', session=session)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 6738))
    app.run(host='0.0.0.0', port=port)

