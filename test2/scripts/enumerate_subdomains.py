import subprocess

def subdomenum(target):
    """Enumerate subdomains using Sublist3r."""
    try:
        command = ["sublist3r", "-d", target]
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print("Error executing Sublist3r. Make sure you have it installed:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)

if __name__ == "__main__":
    target = input("Enter the domain to enumerate subdomains: ")
    subdomenum(target)
