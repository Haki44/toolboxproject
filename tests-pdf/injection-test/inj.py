import argparse
import requests
import re

# Fonction pour scanner les injections SQL
def sql_injection_scan(url):
    sql_errors = [
        "you have an error in your sql syntax",
        "unclosed quotation mark after the character string",
        "syntax error",
        "sql server",
        "unexpected end of sql command",
    ]
    payload = "'"
    full_url = url + payload
    try:
        response = requests.get(full_url)
        for error in sql_errors:
            if error in response.text.lower():
                print(f"[!] SQL Injection Vulnerability found in {url}")
                return
        print(f"[+] No SQL Injection Vulnerability found in {url}")
    except requests.RequestException as e:
        print(f"[-] Error scanning {url} for SQL Injection: {str(e)}")

# Fonction pour scanner les failles XSS
def xss_scan(url):
    payload = "<script>alert('XSS')</script>"
    try:
        response = requests.get(url, params={"q": payload})
        if payload in response.text:
            print(f"[!] XSS Vulnerability found in {url}")
        else:
            print(f"[+] No XSS Vulnerability found in {url}")
    except requests.RequestException as e:
        print(f"[-] Error scanning {url} for XSS: {str(e)}")

# Fonction pour scanner les informations sensibles exposées
def sensitive_info_scan(url):
    sensitive_patterns = {
        "API Key": r"api_key\s*=\s*[\"'][a-zA-Z0-9]{32,}[\"']",
        "Password": r"password\s*=\s*[\"'][^\"']+[\"']",
    }
    try:
        response = requests.get(url)
        for info, pattern in sensitive_patterns.items():
            if re.search(pattern, response.text, re.IGNORECASE):
                print(f"[!] Sensitive {info} found in {url}")
                return
        print(f"[+] No sensitive information found in {url}")
    except requests.RequestException as e:
        print(f"[-] Error scanning {url} for sensitive information: {str(e)}")

# Fonction principale pour scanner une URL
def scan_url(url):
    print(f"[*] Scanning {url} for vulnerabilities...")
    sql_injection_scan(url)
    xss_scan(url)
    sensitive_info_scan(url)
    print("[*] Scanning completed.\n")

# Fonction main
def main():
    parser = argparse.ArgumentParser(description="Simple web vulnerability scanner")
    parser.add_argument("url", help="URL to scan for vulnerabilities")
    args = parser.parse_args()
    scan_url(args.url)

if __name__ == "__main__":
    main()
