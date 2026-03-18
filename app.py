from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    address = db.Column(db.String(200))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(15))


@app.route('/')
def index():

    search = request.args.get("search")

    if search:
        contacts = Contact.query.filter(
            Contact.first_name.contains(search)
        ).all()
    else:
        contacts = Contact.query.all()

    return render_template("index.html", contacts=contacts)


@app.route('/add', methods=['POST'])
def add_contact():

    first = request.form['first']
    last = request.form['last']
    address = request.form['address']
    email = request.form['email']
    phone = request.form['phone']

    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return "Invalid Email Format"

    existing = Contact.query.filter_by(email=email).first()

    if existing:
        return "Email already exists!"

    new_contact = Contact(
        first_name=first,
        last_name=last,
        address=address,
        email=email,
        phone=phone
    )

    db.session.add(new_contact)
    db.session.commit()

    return redirect('/')


@app.route('/delete/<int:id>')
def delete_contact(id):

    contact = Contact.query.get(id)

    db.session.delete(contact)
    db.session.commit()

    return redirect('/')


@app.route('/edit/<int:id>')
def edit_contact(id):

    contact = Contact.query.get(id)

    return render_template("edit.html", contact=contact)


@app.route('/update/<int:id>', methods=['POST'])
def update_contact(id):

    contact = Contact.query.get(id)

    contact.first_name = request.form['first']
    contact.last_name = request.form['last']
    contact.address = request.form['address']
    contact.email = request.form['email']
    contact.phone = request.form['phone']

    db.session.commit()

    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run()
