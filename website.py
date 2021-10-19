from flask import Flask, redirect, render_template, request
from datetime import timedelta, datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "123"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class users(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, name, email):
        self.name = name
        self.email = email

@app.route('/delete/<int:id>')
def delete(id):
    user_to_delete = users.query.get_or_404(id)
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        return redirect('/view')
    except:
        return "Não foi possível deletar o usuário"

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    user_to_update = users.query.get(id)
    if request.method == "POST":
        user_to_update.name = request.form['name']
        user_to_update.email = request.form['email']
        try:
            db.session.commit()
            return redirect('/view')
        except:
            return "Erro"
    else:
        return render_template('update.html', user_to_update=user_to_update)

# render_template: renderização de arquivos templates
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/view")
def view():
    return render_template("view.html", values = users.query.all())

# HTTP methods POST e GET  
@app.route("/registrar", methods=["POST", "GET"])
def registrar():
    if request.method == "POST":
        user_name = request.form['name']
        user_email = request.form['email']
        new_user = users(name=user_name, email=user_email)

        try:
            db.session.add(new_user)
            db.session.commit()
            return redirect('/view')
        except:
            return "Erro"
    else:
        return render_template("registro.html")

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)