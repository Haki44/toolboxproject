import os
import subprocess
from art import tprint

def generer_template(nom_cible):
    # Remplace les espaces par des underscores dans le nom de la cible
    nom_fichier = nom_cible.replace(" ", "_")
    chemin_fichier = f"report_{nom_fichier}.html"

    # Vérifie si le fichier existe déjà
    if os.path.exists(chemin_fichier):
        print(f"Le fichier {chemin_fichier} existe déjà. Le template ne sera pas recréé.")
        return chemin_fichier

    # Template HTML avec le titre inséré dans une balise <h1>
    template = f"""<!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Rapport de Vulnérabilités</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
            }}
            h1 {{
                text-align: center;
            }}
            p {{
                margin-left: 20px;
                margin-right: 20px;
            }}
        </style>
    </head>
    <body>
        <h1>Rapport des analyses de vulnérabilités pour : <b>{nom_cible}</b></h1>
    </body>
    </html>"""

    # Crée un fichier report_nom_de_la_cible.html et écrit le contenu HTML dedans
    with open(chemin_fichier, "w") as fichier:
        fichier.write(template)

    print(f"Le template a été généré dans le fichier {chemin_fichier}")
    return chemin_fichier

def menu(nom_fichier):
    # Affiche le menu
    print("\n     Menu script test :")
    print("         1 - Script n1")
    print("         2 - Détection des vulnérabilités\n")

    choix = input("Veuillez choisir une option: ")

    # Vérifie le choix de l'utilisateur
    if choix == "1":
        subprocess.run(['python3', 'script_n1.py', nom_fichier])  # Exécuter le script n1 avec le nom de fichier en argument
    elif choix == "2":
        subprocess.run(['python3', 'script_n2.py', nom_fichier])  # Exécuter le script n2 avec le nom de fichier en argument
    else:
        print("Option non valide.")
        menu(nom_fichier)  # Réafficher le menu en cas de choix non valide

if __name__ == "__main__":
    # Affichage de l'entête du menu
    print("=" * 82)
    tprint("  Cyber Toolbox  ")
    print("=" * 82)
    
    # Demande à l'utilisateur de saisir le nom de la cible
    nom_cible = input("\nVeuillez entrer le nom de la cible: ")
    nom_fichier = generer_template(nom_cible)

    if nom_fichier:  # Assure que nom_fichier n'est pas None
        menu(nom_fichier)
    else:
        print("Aucun fichier de rapport n'a été généré. Fin du programme.")
