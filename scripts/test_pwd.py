import re # pour les RegEx
import getpass # Pour récupérer le mdp sans trace 
import hashlib
import urllib.request


def test_pwd():

    print("\n"+"╔"+"═" * 42 + "╗")
    print("║ Analyse de la sécurité des mots de passe ║")
    print("╚"+"═" * 42 + "╝")

    pwd = getpass.getpass("\n\033[1;36mEntrez votre mot de passe : \033[0m")
    score = 0
    Conditions= [0]*10
    print("\n[╦] \033[1;36mAnalyse MDP\033[0m")
    score, Conditions = longueur_mdp(pwd, score, Conditions)
    score, Conditions = contenu_mdp(pwd, score, Conditions)
    score, Conditions = suite_car_id(pwd, score, Conditions)
    score, Conditions = suite_car_log(pwd, score, Conditions)
    score, Conditions = ref_prohib(pwd, score, Conditions)
    score, Conditions = pattern(pwd, score, Conditions)
    score, Conditions = search_leak(pwd, score, Conditions)
    label = get_strength_label(score)
    print(f"[╩] \033[1;36mMDP Analysé\033[0m -> Votre mot de passe est : {label}\n")
    print("\n[╦] \033[1;36mPréconisations\033[0m")
    preconisation(Conditions)
    del pwd, Conditions # Maintenant qu'on a fini d'utiliser le mdp, on supprime la variable pour plus de sécurité
    print("[╩] Utiliser une \033[1;36mphrase de passe\033[0m est aussi une très bonne idée !\n")




# Fonctions prinipales

def longueur_mdp(pwd, score, Conditions):
    """  Vérification de la longueur minimale

    Si le mot de passe fait entre 12 et 16 caractères alors il respecte les conditions. 
    S'il fait plus de 16 alors c'est possiblement une phrase de passe et c'est encore mieux.

    """

    message = " ╠═[-] Possède la Longueur minimale : True"
    if len(pwd) < 12:
        message = " ╠═[\033[1;31mx\033[0m] Possède la Longueur minimale : \033[1;31mFalse\033[0m"
        score -= 6
        Conditions[0] = 0
    elif len(pwd) >= 16:
        score += 4
        Conditions[0] = 2
    else:
        score += 1     
        Conditions[0] = 1     
    print(message)
    return score, Conditions

def contenu_mdp(pwd, score, Conditions):
    """  Vérification du contenu requis

    Si le mdp ne possède pas un des caractères suivant alors il ne respecte pas les conditions 

    """

    patterns = [(r'[0-9]', 'Chiffre'),
                (r'[A-Z]', 'Majusucle'),
                (r'[a-z]', 'Minuscule'),
                (r'[!@#$%^&*(),.?":{}|<>]', 'Caractère Spécial')]
                
   
    char_types_count = 0
    special_chars = set()
    indice_pat = 0
    for pattern, name in patterns:
        indice_pat += 1
        if not re.search(pattern, pwd):
            print(f" ╠═[\033[1;31mx\033[0m] Présence de {name} : \033[1;31mFalse\033[0m")
            score -= 1
            Conditions[indice_pat] = 0

        else:
            print(f" ╠═[-] Présence de {name} :", True) 
            score += 1
            Conditions[indice_pat] = 1
            char_types_count += 1
            if name == 'Caractère Spécial':
                special_chars.update(re.findall(pattern, pwd))
    if len(special_chars) >= 2: #Si le mdp comporte plus de deux caractères spéciaux différents ça améliore la compléxité
        score += 1
    if char_types_count <= 2: # Si on utilise que trop peu de type de caractères alors la complexité sera faible
        score -= 4
    return score, Conditions

def suite_car_id(pwd, score, Conditions):

    """  Vérification présence suite de caractères identiques

    Si le mdp est comporte une suite de caractère identique tel aaa, 111 ou !!! alors il perd en force

    """

    Patern_mult = r'(.)\1\1'

    if not re.search(Patern_mult, pwd) :
        print(f" ╠═[-] Présence Suite de caractères identiques : False")
        score += 1
        Conditions[5] = 1
    else:
        print(f" ╠═[\033[1;31mx\033[0m] Présence Suite de caractères identiques :\033[1;31mTrue\033[0m") 
        score -= 3
        Conditions[5] = 0
    return score, Conditions

def suite_car_log(pwd, score, Conditions):
    """ Vérification présence suite de caractères logiques

    Si le mdp est comporte une suite de caractère logiques tel abc ou 123 alors il perd en force

    """

    Patern_mult = r'(.)\1\1'
    if not has_alphabet_sequence(pwd) and not has_number_sequence(pwd):
        print(f" ╠═[-] Présence Suite de caractères logiques : False")
        score += 1
        Conditions[6] = 1
    else:
        print(f" ╠═[\033[1;31mx\033[0m] Présence Suite de caractères logiques : \033[1;31mTrue\033[0m") 
        score -= 3
        Conditions[6] = 0
    return score, Conditions
    
def ref_prohib(pwd, score, Conditions):
    """  Vérification présence référence prohibé

    Si le mdp comporte à un lien quelques avec vous ou l'entreprise alors il perd en force.
    Il ne faut donc pas utilisé dans son mdp  : - nom appli,
                                                - code postaux,
                                                - ville, 
                                                - suite caractères logiques,
                                                - nom /prénom,
                                                - services, 
                                                - ...
    Il ne faut pas non plus utiliser d'expression trop courante tel que : Mot2passe, Password ou SesamOuvreToi
    Les mots prohibé sont référencé dans le fichier ref.txt

    """

    with open('includes/ref.txt', 'r') as f:
        ref_words = f.read().splitlines()

    found_reference = False   
    for word in ref_words:
        if re.search(word, pwd, re.IGNORECASE):
            print(f" ╠═[\033[1;31mx\033[0m] Présence de référence prohibé, \033[1;31m'{word}'\033[0m : \033[1;31mTrue\033[0m")
            found_reference = True   
            score -= 3
            Conditions[7] = 0
    if not found_reference:
        print(f" ╠═[-] Présence de référence prohibé :", False)
        score += 1
        Conditions[7] = 1
    return score, Conditions

def pattern(pwd, score, Conditions):
    """  Vérification du pattern du mdp

    Il faut éviter le format basique : Motsavecmajuscule-Nombres-Caractèrespéciaux
    ou le format : Motsavecmajuscule-Caractèrespéciaux-Nombres
    sinon le mdp perd en force 

    """

    Patern_basique1 = r'^[A-Z]*[a-z]*[A-Z]*[a-z]*[!@#$%^&*(),.?":{}|<>]*[0-9]*$'
    Patern_basique2 = r'^[A-Z]*[a-z]*[A-Z]*[a-z]*[0-9]*[!@#$%^&*(),.?":{}|<>]*$'
    if not re.match(Patern_basique1, pwd) and not re.match(Patern_basique2, pwd):
        print(f" ╠═[-] Pattern Basique : False")
        score += 2
        Conditions[8] = 1
    else:
        print(f" ╠═[\033[1;31mx\033[0m] Pattern Basique : \033[1;31mTrue\033[0m") 
        score -= 3
        Conditions[8] = 0
    return score, Conditions

def search_leak(pwd, score, Conditions):

    """  Vérification si le mdp a fuité

    Vérifie si le mdp a été compromis dans une fuite de données en utilisant l'API "Have I Been Pwned".

    Ce code hache d'abord le mot de passe en utilisant SHA-1, 
    puis récupère les 5 premiers caractères du hachage et les envoie à l'API. 
    L'API renvoie alors une liste de hachages qui correspondent aux 5 premiers caractères. 
    Le code vérifie ensuite si la seconde partie du hachage du mot de passe se trouve dans la liste renvoyée par l'API. 
    Si c'est le cas, cela signifie que le mot de passe a été compromis dans une fuite de données.

   """ 

    sha1_password = hashlib.sha1(pwd.encode('utf-8')).hexdigest().upper()
    range1, range2 = sha1_password[:5], sha1_password[5:]

    request = urllib.request.Request(f'https://api.pwnedpasswords.com/range/{range1}')
    response = urllib.request.urlopen(request)
    if response.getcode() != 200:
        print(f" ╠═[\033[1;31mx\033[0m] Erreur lors de la vérification de la fuite du mot de passe : \033[1;31mTrue\033[0m")
    else:
        hashes = (line.decode().split(':') for line in response.readlines())
        if any(hash_suffix == range2 for hash_suffix, count in hashes):
            print(f" ╠═[\033[1;31mx\033[0m] \033[1;31mLe mot de passe a fuité : True\033[0m")
            score = - 22 # Peut importe la force d'un mdp, s'il a fuité alors il ne vaut rien
            Conditions[9] = 0
        else:
            print(f" ╠═[-] Le mot de passe n'a pas fuité : False")
            score += 1
            Conditions[9] = 1

    

    return score, Conditions

def preconisation(Conditions):
    
    """  Préconisation de choix de mot de passe

    Cette fonction fera apparaître les messages de préconisations pour aider l'utilisateur à améliorer son mot de passe en fonction de l'analyse faite précédement
    Conditions est une liste composée de variables dans l'ordre d'appel des différentes fonctions
    Si une variable est égale à 0 alors ça signifie qu'elle n'est pas respecté
    Si elle est égale à 1 alors la condition est respecté
    Si elle est égale à 2 alors elle la condition est plus que respecté, et des dipositions supplémentaire ont été prisent. (ex : + 16 caractères)
    
    """

    Preco =["\033[1;32mRalonger\033[0m votre mot de passe.",
            "\033[1;32mRajouter\033[0m quelques chiffres.",
            "\033[1;32mRajouter\033[0m quelques majuscules.",
            "\033[1;32mRajouter\033[0m quelques minuscules.",
            "\033[1;32mRajouter\033[0m quelques caractères spéciaux.",
            "\033[1;32mEviter\033[0m les suites de caractères identiques (!!!, ***, 111, etc).",
            "\033[1;32mEviter\033[0m les suites de caractères logiques (abc, 123, 321, etc).",
            "\033[1;32mEviter\033[0m les mots de passe avec un lien avec vous ou l'entreprise (prenom, data de naissance, nom d'application, code postal, etc).\n ╠═[\033[1;35m!\033[0m] \033[1;32mEviter\033[0m aussi les expressions trop courantes comme 'Mot2passe', 'Password', etc.",
            "\033[1;32mEviter\033[0m le format basique : \033[1;32mMotsavecmajuscule\033[0m\033[1;33mNombres\033[0m\033[1;35mCaractèrespéciaux\033[0m, répartissez les caractères de manière aléatoire (non groupé).",
            "\033[1;32mChanger totalement\033[0m votre mot de passe parce qu'il a fuité, reprennez les bonnes pratiques pour un recréer un.\n ╠═[\033[1;35m!\033[0m] Vous pouvez quand même prendre en compte les remarques ci dessus."]


    for i in range(len(Conditions)):
        if Conditions[i] == 0 :
            print(" ╠═[\033[1;35m!\033[0m]", Preco[i])
        else :
            pass
    if Conditions[0] == 1 : # Dans le cas où le mot de passe fait entre 12 et 16 caractère de long
        print(" ╠═[\033[1;35m!\033[0m] La longueur du mot de passe est acceptable mais vous pouvez encore \033[1;32mrajouter un caractère\033[0m ou plus si vous le souhaitez")

    
    if Conditions == [1]*10 or Conditions == [2, 1, 1, 1, 1, 1, 1, 1, 1, 1]: # Dans le cas où toutes les conditions ont été validées
        print(" ╠═[\033[1;35m!\033[0m] Votre mot de passe est déjà suffisament fort, n'hésitez pas à le changer assez réguliérement et à garder ce niveau de complexité. ")
        print(" ╠═[\033[1;35m!\033[0m] Si vous voulez vraiment l'améliorer vous pouvez néamoins ajouter un ou deux caractères de plus.")



# Fonctions secondaires

def has_alphabet_sequence(s):
    for i in range(len(s) - 2):
        if (s[i].isalpha() and s[i+1].isalpha() and s[i+2].isalpha() # si les trois caractères sont des lettres
                and ord(s[i+1].lower()) - ord(s[i].lower()) == 1 # si la deuxième lettre suit la première dans l'alphabet
                and ord(s[i+2].lower()) - ord(s[i+1].lower()) == 1): # si la troisième lettre suit la deuxième dans l'alphabet
            return True
    return False

def has_number_sequence(s):
    for i in range(len(s) - 2):
        if s[i].isdigit() and s[i+1].isdigit() and s[i+2].isdigit(): # Vérifie si les trois caractères courants sont des chiffres
            if (int(s[i]) + 1 == int(s[i+1]) and int(s[i+1]) + 1 == int(s[i+2])) or \
               (int(s[i]) - 1 == int(s[i+1]) and int(s[i+1]) - 1 == int(s[i+2])): # Vérifie si les trois chiffres sont consécutifs dans l'ordre décroissant et sur la ligne du dessus c'est dans l'ordre croissant
               return True
    return False

def get_strength_label(score):

    """  Force d'un mot de passe

    La force F d'un mot de passe à été décrite arbitrairement suivant les critères suivant : F ∈ [-26, 16]

    Mot de passe "Très Fort" ↔ F ∈ [7, 16] ↔ Mot de passe respectant toutes les préconisations et ne possédant pas de pattern basique (ou avec une longueur conséquente)
    Mot de passe "Fort" ↔ F ∈ [4, 6] ↔ Mot de passe respectant toutes les préconisations
    Mot de passe "Moyen" ↔ F ∈ [1, 3] ↔ Mot de passe ne respectant pas toutes les préconisations (suite de caractères, etc.) ou avec un pattern basique
    Mot de passe "Faible" ↔ F ∈ [-5, 0] ↔ Mot de passe ne respectant pas toutes les préconisations (suite de caractères, etc.) et/ou avec un pattern basique
    Mot de passe "Très Faible" ↔ F ∈ [-26, -6] ↔ Mot de passe ne respectant pas les règles de base et/ou ayant fait l'objet d'une fuite

    """

    if score <= 16 and score >= 7:
        return "\033[1;32mTrès fort\033[0m"
    elif score <= 6 and score >= 4:
        return "\033[1;34mFort\033[0m"
    elif score <= 3 and score >= 1:
        return "Moyen"
    elif score <= 0 and score >= -5:
        return "\033[1;33mFaible\033[0m"
    elif score <= -6 and score >= -24:
        return "\033[1;31mTrès faible\033[0m"
    else:
        return "Score invalide"

# test_pwd()