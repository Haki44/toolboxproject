import subprocess
from art import tprint

def menu():
    # Affiche le menu
    print("\n     Menu script test :")
    print("         [1] - Scan de ports")
    print("         [2] - Scan de vulnérabilités\n")

    choix = input("Veuillez choisir une option: ")

    # Vérifie le choix de l'utilisateur
    if choix == "1":
        subprocess.run(['python3', 'script_n1.py'])  # Exécuter le script n1 avec le nom de fichier en argument
    elif choix == "2":
        subprocess.run(['python3', 'script_n2.py'])  # Exécuter le script n2 avec le nom de fichier en argument
    else:
        print("Option non valide.")

if __name__ == "__main__":
    # Affichage de l'entête du menu
    print("=" * 82)
    tprint("  Cyber Toolbox  ")
    print("=" * 82)
    menu()
