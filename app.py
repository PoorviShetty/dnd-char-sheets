from flask import Flask, render_template, request, redirect, url_for, flash, session, abort
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from dotenv import load_dotenv
load_dotenv('.env')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

PASSWORD = os.getenv('PASSWORD')


def check_pw(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        status = session.get('status')
        if status != "good":
            return redirect(url_for('login'))
        return func(*args, **kwargs)

    return decorated_function


class Chars(db.Model):
    __tablename__ = 'chars'
    id = db.Column(db.Integer, primary_key=True)

    # PAGE 1

    # Intro
    name = db.Column(db.String(140))
    class_level = db.Column(db.String(100))
    background = db.Column(db.String(100))
    player_name = db.Column(db.String(140))
    race = db.Column(db.String(100))
    alignment = db.Column(db.String(50))
    exp = db.Column(db.String(10))

    # Char Stats
    armor_class = db.Column(db.String(5))
    initiative = db.Column(db.String(5))
    speed = db.Column(db.String(5))
    hit_point_max = db.Column(db.String(5))
    current_hit_points = db.Column(db.String(5))
    hit_dice = db.Column(db.String(5))
    total_hit_dic = db.Column(db.String(5))
    sucess_death_saves = db.Column(db.String(5))
    failure_death_saves = db.Column(db.String(5))

    # Modifiers
    strength_mod = db.Column(db.String(5))
    dexterity_mod = db.Column(db.String(5))
    constitution_mod = db.Column(db.String(5))
    intelligence_mod = db.Column(db.String(5))
    wisdom_mod = db.Column(db.String(5))
    charisma_mod = db.Column(db.String(5))
    passive_perception = db.Column(db.String(5))
    inspiration = db.Column(db.String(5))
    proficiency_bonus = db.Column(db.String(5))

    # Saving Throws
    strength_st = db.Column(db.String(5))
    dexterity_st = db.Column(db.String(5))
    constitution_st = db.Column(db.String(5))
    intelligence_st = db.Column(db.String(5))
    wisdom_st = db.Column(db.String(5))
    charisma_st = db.Column(db.String(5))

    # Skills
    proficienices = db.Column(db.String(500))
    other_proficienices = db.Column(db.String(1000))

    # Attacks
    attacks = db.Column(db.String(2000))

    # Features
    features = db.Column(db.String(2000))

    # Equipment
    cp = db.Column(db.String(5))
    sp = db.Column(db.String(5))
    ep = db.Column(db.String(5))
    gp = db.Column(db.String(5))
    pp = db.Column(db.String(5))
    inventory = db.Column(db.String(1000))

    # Character Motivation
    personality = db.Column(db.String(500))
    ideals = db.Column(db.String(500))
    bonds = db.Column(db.String(500))
    flaws = db.Column(db.String(500))

    # PAGE 2

    # Character Appearance and Traits
    age = db.Column(db.String(15))
    height = db.Column(db.String(15))
    weight = db.Column(db.String(15))
    eyes = db.Column(db.String(15))
    skin = db.Column(db.String(15))
    hair = db.Column(db.String(15))
    race = db.Column(db.String(3000))
    char_class = db.Column(db.String(3000))
    backstory = db.Column(db.String(3000))
    additional_features = db.Column(db.String(3000))
    treasure = db.Column(db.String(1000))

    # OPTIONAL PAGE 3

    # Intro
    spellcasting_class = db.Column(db.String(25))
    spellcasting_ability = db.Column(db.String(25))
    spell_save_dc = db.Column(db.String(5))
    spell_attack_bonus = db.Column(db.String(5))
    level_1_spells = db.Column(db.String(500))
    level_2_spells = db.Column(db.String(500))
    level_3_spells = db.Column(db.String(500))
    level_4_spells = db.Column(db.String(500))
    level_5_spells = db.Column(db.String(500))
    level_6_spells = db.Column(db.String(500))
    level_7_spells = db.Column(db.String(500))
    level_8_spells = db.Column(db.String(500))
    level_9_spells = db.Column(db.String(500))


@app.route('/', methods=['GET', 'POST'])
@check_pw
def index():
    chars = Chars.query.all()
    return render_template('index.html', chars=chars)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        req = request.form
        password = req.get("pw")

        if password != PASSWORD:
            flash('wrong password! try again...')
            return redirect(request.url)

        session["status"] = 'good'
        return redirect(url_for("index"))
    return render_template('login.html')


@app.route('/char/<int:id>')
def view(id):
    char = Chars.query.filter_by(id=id).first()
    if char:
        return render_template('view.html', char=char)

    print(f"Char with id = {id} does not exist")
    return redirect(url_for("index"))


@app.route("/add", methods=["GET", "POST"])
@check_pw
def add():
    if request.form:
        char = Chars()
        for k, v in request.form.items():
            setattr(char, k, v)

        db.session.add(char)
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("add.html")


@app.route('/char/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    char = Chars.query.filter_by(id=id).first()
    if not char:
        print(f"Char with id = {id} does not exist")
        return redirect(url_for("index"))
    if request.method == 'POST':
        if char:
            db.session.delete(char)
            db.session.commit()

            char = Chars()
            setattr(char, 'id', id)

            for k, v in request.form.items():
                setattr(char, k, v)

            db.session.add(char)
            db.session.commit()
            return redirect(f'/char/{id}')
        print(f"Char with id = {id} does not exist")

    return render_template('edit.html', char=char)


@app.route('/char/<int:id>/delete', methods=['GET', 'POST'])
def delete(id):
    char = Chars.query.filter_by(id=id).first()
    if not char:
        print(f"Char with id = {id} does not exist")
        return redirect(url_for("index"))
    if request.method == 'POST':
        if char:
            db.session.delete(char)
            db.session.commit()
            return redirect(url_for("index"))
        abort(404)

    return render_template('delete.html', char=char)


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
