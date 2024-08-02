import sys
import os

# Lire le nom du fichier à partir des arguments de ligne de commande
nom_fichier = sys.argv[1]

# Ajouter le paragraphe au fichier HTML spécifié
with open(nom_fichier, "r+") as fichier:
    # Lire le contenu existant
    contenu = fichier.read()
    # Trouver l'index pour insérer le nouveau contenu avant la balise </body>
    index_insertion = contenu.index("</body>")

    section_script2 = """
    <hr>
    <section>
        <p>ceci est un test du script 2</p>
    </section>
    """
    # Nouveau contenu à insérer
    nouveau_contenu = contenu[:index_insertion] + section_script2 + contenu[index_insertion:]
    # Aller au début du fichier et écrire le nouveau contenu
    fichier.seek(0)
    fichier.write(nouveau_contenu)
    fichier.truncate()

print(f"Le texte a été ajouté au fichier {nom_fichier}")

# Importer et exécuter la fonction menu du script principal
import menu_script
menu_script.menu(nom_fichier)
