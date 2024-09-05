# CYBER TOOLBOX
Projet d'étude : création d'une toolbox de cybersécurité.

# 🔐 Automated Penetration Testing Toolbox

## 🛠 Introduction

L'objectif de cette toolbox est de faciliter et d'automatiser les tests d'intrusion sur les systèmes et réseaux cibles. Elle permet de simplifier le processus en automatisant de nombreuses tâches complexes et en offrant une série de fonctionnalités avancées pour identifier et analyser les vulnérabilités mais aussi de tester la sécurité des systèmes.

---

## 📥 Installation

### Prérequis

- 🐍 Python 3 ou plus
- Systèmes d'exploitation compatibles : Linux (🐉 kali recommandé)
- Outils requis : `git`, `pip`

### Étapes d'installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/Haki44/toolboxproject.git
2. **Accédez au répertoire du projet** :
   ```bash
   cd toolboxproject
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt

---

## 🔍 Fonctionnalités et Utilisation 💻

### </> Lancement du script 📄
   ```bash
   python3 cyber_toolbox.py
   ```
![image](https://github.com/user-attachments/assets/64b0d59d-95d0-499d-963e-4507a8314065)

1. **Scan de ports** :
   Analyse les ports ouverts d'une URL ou d'une IP spécifiée afin d'identifier les services exposés et leurs éventuelles vulnérabilités.
2. **Scan de vulnérabilités** :
   Effectue un audit des vulnérabilités d'un site web pour détecter les failles de sécurité connues.
3. **Exploitation de vulnérabilités** :
   Cherche et exploite en profondeur les vulnérabilités détectées pour évaluer l'impact potentiel sur le système cible.
4. **Test d'authentification** :
   Réalise des attaques par force brute sur les connexions SSH pour tester la robustesse des identifiants de connexion.
5. **Post exploitation** :
   Une fois un accès obtenu, ce script récupère les fichiers sensibles et comprometants présents sur le système cible pour une analyse approfondie.
6. **Analyse de la sécurité des mot de passes** :
   Vérifie la sécurité d'un mot de passe en s'appuyant sur l'API Have I Been Pwned pour détecter les fuites ou réutilisations.
7. **Générer un rapport** :
   Compile les résultats des scans, des tests d'authentification, et des actions post-exploitation dans un rapport détaillé pour une analyse complète de la sécurité.
   
---

## ⚠️ Limitations et Contexte d'Utilisation ⚠️

- Environnement de test : Cette toolbox doit être utilisée uniquement dans des environnements contrôlés (laboratoires de test, systèmes virtuels) ou sur des systèmes pour lesquels vous avez l'autorisation explicite d'effectuer des tests d'intrusion.

- Conformité : Assurez-vous de respecter les lois et règlements en vigueur concernant les tests d'intrusion, et utilisez cet outil uniquement dans des contextes légaux.

## 👥 Contributeurs
- Djibril Diallo – M1 Cyber – SUP DE VINCI Nantes
- Maxence Bannier (Haki44) – M1 Cyber - SUP DE VINCI Nantes












