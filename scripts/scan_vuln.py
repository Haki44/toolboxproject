import subprocess

def run_command(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = process.communicate()
    return stdout.decode(errors='ignore'), stderr.decode(errors='ignore')

def run_nikto(target):
    command = f"nikto -h {target}"
    stdout, stderr = run_command(command)
    return stdout, stderr

def scan_vulnerabilities():
    print("\n" + "╔" + "═" * 39 + "╗")
    print("║ Analyse des vulnérabilités avec Nikto ║")
    print("╚" + "═" * 39 + "╝")

    url = input("\n\033[1;36mEntrez l'URL à scanner : \033[0m")
    print("\n[╦] \033[1;36mLancement du scan Nikto\033[0m\n")
    
    stdout, stderr = run_nikto(url)

    if stdout:
        print("\n[╦] \033[1;36mRésultat du scan Nikto\033[0m\n")
        print(stdout)
    
    if stderr:
        print("\n[╦] \033[1;31mErreurs du scan Nikto\033[0m\n")
        print(stderr)
        
    # try:
        # Exécution de Nikto avec capture de la sortie
    # result = subprocess.run(['nikto', '-h', url], capture_output=True, text=True)
    # print(result.stdout)
    # output = result.stdout
    # error_output = result.stderr

    #     print("\n[╦] \033[1;36mRésultat du scan Nikto\033[0m\n")
    #     print(output)
        
    #     if error_output:
    #         print("\n[╦] \033[1;31mErreurs du scan Nikto\033[0m\n")
    #         print(error_output)
    
    # except FileNotFoundError:
    #     print("\033[1;31mErreur : Nikto n'est pas installé ou introuvable. Veuillez l'installer et réessayer.\033[0m")

