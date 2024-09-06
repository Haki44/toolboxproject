# CYBER TOOLBOX
Projet d'étude : création d'une toolbox de cybersécurité.

# 🔐 Automated Penetration Testing Toolbox

## 🛠 Introduction

L'objectif de cette toolbox est de faciliter et d'automatiser les tests d'intrusion sur les systèmes et réseaux cibles. Elle permet de simplifier le processus en automatisant de nombreuses tâches complexes et en offrant une série de fonctionnalités avancées pour identifier et analyser les vulnérabilités mais aussi de tester la sécurité des systèmes.

Cette toolbox s'appuie entièrement sur des **librairies Python open source** et des **outils Kali Linux**. Tous les composants utilisés pour développer et exécuter la toolbox sont libres et accessibles à tous, ce qui garantit une transparence totale.

---

## 📥 Installation

### Prérequis

- 🐍 Python 3 ou plus
- Outils requis : `git`, `pip`
- Systèmes d'exploitation compatibles : Linux (🐉 kali recommandé)
- Outils Kali : `nmap`, `zaproxy`  
  **Commande d'installation Nmap**
   ```bash
   sudo apt install nmap
   ```
   **Commande d'installation Zaproxy**
   ```bash
   sudo apt install zaproxy
   ```
### Étapes d'installation

1. **Clonez le dépôt** :
   ```bash
   git clone https://github.com/Haki44/toolboxproject.git
   ```
2. **Accédez au répertoire du projet** :
   ```bash
   cd toolboxproject
   ```
3. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
    ```
   
---

## 🔍 Fonctionnalités et Utilisation 💻

### </> Lancement du script 📄
   ```bash
   python3 cyber_toolbox.py
   ```
![image](https://github.com/user-attachments/assets/64b0d59d-95d0-499d-963e-4507a8314065)

1. **Scan de ports** :  
   Analyse les ports ouverts d'une URL ou d'une IP spécifiée afin d'identifier les services exposés et leurs éventuelles vulnérabilités.
   
   ![image](https://github.com/user-attachments/assets/b812cf70-1b9d-4a38-8cf7-145edc3f716e)

2. **Scan de vulnérabilités** :  
   Effectue un audit des vulnérabilités d'un site web pour détecter les failles de sécurité connues.
    
   ![image](https://github.com/user-attachments/assets/9ed90a23-428c-40a6-82d9-ce8a48740531)
   
3. **Exploitation de vulnérabilités** :  
   Cherche et exploite en profondeur les vulnérabilités détectées pour évaluer l'impact potentiel sur le système cible.

   ![image](https://github.com/user-attachments/assets/42601154-b810-4812-91c0-3e4b8654b5a9)
   ![image](https://github.com/user-attachments/assets/deacdeb7-d1be-448e-a4a3-0e31e1f6e9c7)

4. **Test d'authentification** :  
   Réalise des attaques par force brute sur les connexions SSH pour tester la robustesse des identifiants de connexion.
     
   ![image](https://github.com/user-attachments/assets/eae19e58-a0c5-42a9-a871-31615d887f3b)

5. **Post exploitation** :  
   Une fois un accès obtenu, ce script récupère les fichiers sensibles et comprometants présents sur le système cible pour une analyse approfondie.

   - Utilisation : Pour utiliser ce module, il faut au préalable avoir un accès de la machine cible en SSH et connaitre l'OS
     
   ![Screenshot_1](https://github.com/user-attachments/assets/286c2167-45ee-41e7-afc4-18908ae830de)
   ![image](https://github.com/user-attachments/assets/31636acb-1ba4-483f-9ccc-a1d5cd994c2b)

6. **Analyse de la sécurité des mot de passes** :  
   Vérifie la sécurité d'un mot de passe en s'appuyant sur l'API Have I Been Pwned pour détecter les fuites ou réutilisations.
     
   ![image](https://github.com/user-attachments/assets/41aabe17-0874-41df-85a9-65e77ecfd511)

7. **Générer un rapport** (Cette fonctionnalité n'a pas encore été développée):  
   Compile les résultats des scans, des tests d'authentification, et des actions post-exploitation dans un rapport détaillé pour une analyse complète de la sécurité.


## 🔜 A venir ⏳

### Intégration Docker 🐋

Dans les prochaines versions, l'objectif est d'emballer la toolbox dans une image **Docker**. Cette intégration permettra de simplifier le déploiement et l'exécution de la toolbox sur n'importe quel environnement sans avoir à gérer manuellement les dépendances et les configurations système.

L'utilisation de Docker offrira les avantages suivants :
- **Portabilité** : Exécuter la toolbox sur n'importe quel système d'exploitation prenant en charge Docker.
- **Isolation** : Les tests d'intrusion et les scans se feront dans un environnement isolé, minimisant les risques d'interférence avec le système hôte.
- **Facilité de déploiement** : Un seul fichier `Dockerfile` pour configurer et déployer rapidement la toolbox.

---

## ⚠️ Limitations et Contexte d'Utilisation ⚠️

- Environnement de test : Cette toolbox doit être utilisée uniquement dans des environnements contrôlés (laboratoires de test, systèmes virtuels) ou sur des systèmes pour lesquels vous avez l'autorisation explicite d'effectuer des tests d'intrusion.

- Conformité : Assurez-vous de respecter les lois et règlements en vigueur concernant les tests d'intrusion, et utilisez cet outil uniquement dans des contextes légaux.

## 👥 Contributeurs
- Djibril Diallo (djib06) – M1 Cyber – SUP DE VINCI Nantes
- Maxence Bannier (Haki44) – M1 Cyber - SUP DE VINCI Nantes












