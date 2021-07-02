from flask import render_template, flash, redirect, url_for
from app import app, db
from app.forms import LoginForm, PublicacionForm, SignUpForm, NoteForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Note, Publicacion
import uuid


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html")


@app.route("/publicaciones")
@login_required
def view_publicaciones():
    publicaciones = Publicacion.query.filter_by(users_id=current_user.id).all()
    return render_template("publicaciones.html", publicaciones = publicaciones)

@app.route('/publicaciones/create', methods=['GET', 'POST'])
@login_required
def create_publicaciones():
    form = PublicacionForm()
    if form.validate_on_submit():
        #POST
        publicacion = Publicacion()
        publicacion.body = form.body.data
        publicacion.users_id = current_user.id
        db.session.add(publicacion)
        db.session.commit()
        return redirect(url_for("view_publicaciones")) 
    else:
        #GET
        return render_template("publicacion.html", title="Publicacion",form=form)
    return ""

@app.route('/delete/<int:id>')
def delete_publicaciones(id):
    publicaciones = Publicacion.query.filter_by(id=id).first()
    if publicaciones:
        if publicaciones.users_id != current_user.id:
            flash("ACCESO NO AUTORIZADO")
            return redirect(url_for("view_publicaciones"))
        Publicacion.query.filter_by(id=id).delete()
        db.session.commit()

@app.route("/notes")
@login_required
def view_notes():
    notes = Note.query.filter_by(users_id=current_user.id).all()
    # salida = ""
    # for note in notes:
    #     salida+=note.body
    return render_template("notes.html", notes = notes)


@app.route('/notes/create', methods=['GET', 'POST'])
@login_required
def create_notes():
    form = NoteForm()
    if form.validate_on_submit():
        #POST
        note = Note()
        note.title = form.title.data
        note.body = form.body.data
        note.UUID = str(uuid.uuid4())
        note.users_id = current_user.id
        db.session.add(note)
        db.session.commit()
        return redirect(url_for("view_notes")) 
    else:
        #GET
        return render_template("note.html", title="Nota",form=form)
    return ""

@app.route('/share/<int:id>')
@login_required
def share_notes(id):
    note = Note.query.filter_by(id=id).first()
    if note.users_id != current_user.id:
        flash("ACCESO NO AUTORIZADO")
        return redirect(url_for("view_notes"))
    return url_for("public_notes", id=note.UUID, _external=True)
    # return "share_notes" + str(id)

@app.route('/s/<uuid:id>')
def public_notes(id):
    note = Note.query.filter_by(UUID=str(id)).first()
    return render_template("public_note.html", title=note.title, note=note)

@app.route('/delete/<int:id>')
def delete_notes(id):
    note = Note.query.filter_by(id=id).first()
    if note:
        if note.users_id != current_user.id:
            flash("ACCESO NO AUTORIZADO")
            return redirect(url_for("view_notes"))
        Note.query.filter_by(id=id).delete()
        db.session.commit()
    
    return redirect(url_for("view_notes")) 

@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        #POST
        #Iniciar sesión con base de datos
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("No se encontro el usuario o la contraseña esta incorrecta")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        flash("Iniciaste Sesión correctamente, Hola {}".format(form.username.data))
        return redirect("/index")
    return render_template("login.html", title="Login",form=form)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = SignUpForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        print(form)
        if user is None:
            user = User()
            user.username = form.username.data
            user.email = form.email.data
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("Usuario creado exitosamente")

        else:
            flash("El usuario ya existe")
            return redirect(url_for("signup"))
        
        
        return redirect("/index")
    return render_template("signup.html", title="Signup",form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))
