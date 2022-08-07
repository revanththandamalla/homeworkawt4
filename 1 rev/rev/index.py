import os
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] =\
    'sqlite:///' + os.path.join(basedir, 'pages.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class page(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    c_n = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    email = db.Column(db.String(120))
    address = db.Column(db.String(220))

    def __init__(self, c_n, phone, email, address):
        self.c_n = c_n
        self.phone = phone
        self.email = email
        self.address = address


@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/", methods=['POST', 'GET'])
def index():
    pages = db.session.query(page).all()

    if(request.method == 'POST'):
        post_type = request.form['type']
        if(post_type == 'additem'):
            c_n = request.form['c_n']
            email = request.form['email']
            phone = request.form['phone']
            address = request.form['address']

            pag = page(c_n, email, phone, address)
            db.session.add(pag)
            db.session.commit()

            pages = db.session.query(page).all()

            return render_template('home.html', content=[pages])

        elif(post_type == 'search'):
            search_term = request.form['sea_trm']

            search_term = "%" + search_term + "%"

            res = db.session.query(page).filter(
                or_(
                    page.c_n.like(search_term),
                    page.phone.like(search_term),
                    page.email.like(search_term),
                    page.address.like(search_term)
                )
            ).all()

            pages = db.session.query(page).all()

            return render_template('home.html', content=[pages, "", res])

        elif(post_type == 'delete'):
            id = request.form['id']

            db.session.query(page).filter(page.id == id).delete()
            db.session.commit()

            pages = page.query.all()

            return render_template("home.html", content=[pages])

        elif(post_type == 'edit'):
            ed_id = request.form['id']

            pages = page.query.all()

            return render_template('home.html', content=[pages, ed_id])

        elif(post_type == 'edit_id'):
            
            id = request.form['id']
            c_n = request.form['c_n']
            email = request.form['email']
            phone = request.form['phone']

            db.session.query(page).filter(page.id == id).update(
                {'c_n': c_n,
                 'email': email,
                 'phone': phone
                 })

            db.session.commit()

            pages = page.query.all()

            return render_template("home.html", content=[pages, ""])

    return render_template('home.html', content=[pages, ""])


if __name__ == '__main__':
    app.run(debug=True)
