from flask import Flask, request, render_template, redirect, url_for, flash
from models import Voyage, Ville

app = Flask(__name__)
app.config["SECRET_KEY"] = "leovje_vnleknv099!efe#"

# CREATION DES DIFFÉRENTES TABLE DE LA BASE DE DONNÉES
try:
    Voyage("", "", "", "")
    Ville("")
except Exception as e:
    print(e)


@app.get("/")
def home():
    return render_template("index.html")

# AFFICHAGE DE LA PAGE POUR AJOUTER LES VOYAGES
@app.get("/voyage")
def page_voyage():
    ville = Ville()
    return render_template("voyage.html", villes=ville.get_all())

# AFFICHAGE DE LA PAGE POUR AFFICHER LA LISTE DES VOYAGES ENREGISTREES
@app.get("/voyages")
def page_voyages():
    voyages=Voyage()
    return render_template("list_voyage.html", voyages=voyages.get_all())

# LA GESTION DES DONNÉES POSTER POUR AJOUTER LE VOYAGE
@app.post("/voyage")
def add_voyage():
    depart = request.form.get("ville_depart").upper().strip()
    destination = request.form.get("ville_arrivee").upper().strip()
    date = request.form.get("date")
    heure = request.form.get("heure")
    
    if depart != destination:
        voyage = Voyage("", depart, destination, date, heure)
        try:
            if voyage.insert():
                flash(f"Le voyage vient d'être programmé!", "success")
        except Exception as e:
            flash(f"{e}", "error")
    else:
        flash(
            f"Impossible de programmer un voyage de '{depart.title()}' vers '{destination.title()}'",
            "error",
        )
    return redirect(url_for("page_voyage"))

#AFFICHAGE DE LA PAGE POUR AJOUTER LES VILLES
@app.get("/ville")
def page_ville():
    return render_template("ville.html")

# AFFICHAGE DE LA PAGE POUR AFFICHER LA LISTE DES VILLES ENREGISTREES
@app.get("/villes")
def page_villes():
    villes=Ville()
    return render_template("list_ville.html", villes=villes.get_all())

# LA GESTION DES DONNÉES POSTER POUR AJOUTER LA VILLE
@app.post("/ville")
def add_ville():
    nom = request.form.get("ville").upper().strip()
    nom = nom.replace("É","E") # BOUAKÉ sera éguale à BOUAKE     
                               # pour éviter une répétition à cause d'un accent en plus ou en moin
    print(nom)
    ville = Ville(nom_ville=nom)
    if not ville.is_exist():
        try:
            if ville.insert():
                flash(f"La ville '{nom}' vient d'être ajoutée!", "success")
        except Exception as e:
            flash(f"{e}", "error")
    else:
        flash(f"'{nom}' existe déja!", "error")
    return redirect(url_for("page_ville"))

# AFFICHAGE DE LA PAGE POUR AJOUTER CHERCHER UN VOYAGE
@app.get("/verifier")
def page_verifier():
    ville = Ville()
    return render_template("verifier_voyage.html", villes=ville.get_all())

# LA GESTION DES DONNÉES POSTER POUR CHERCHER UN VOYAGE
@app.post("/verifier")
def post_verifier():
    depart = request.form.get("ville_depart").upper().strip()
    destination = request.form.get("ville_arrivee").upper().strip()
    if depart != destination:
        voyage = Voyage("", depart, destination)
        voyages = voyage.is_exist()
        if voyages:
           return render_template("verifier_voyage_list.html", voyages=voyages)
        else:
            flash(
            f"Aucun voyage programmé de '{depart.title()}' vers '{destination.title()}'",
            "error",
        )
    else:
        flash(
            f"Impossible de programmer un voyage de '{depart.title()}' vers '{destination.title()}'",
            "error",
        )
    return redirect(url_for("page_verifier"))

if __name__ == "__main__":
    app.run()
