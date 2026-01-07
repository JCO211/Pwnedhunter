import sys, requests, time, json, os, socket
from colorama import Fore, Style, init

init(autoreset=True)

def print_banner():
    os.system('clear')
    print(f"{Fore.RED}{Style.BRIGHT}" + r"""
    __________                          ________                __            
   / ____/ __ \_      ______  ___  ____/ /_  __/ /_  ________  / /____  _____
  / /_  / /_/ / | /| / / __ \/ _ \/ __  / / / / __ \/ ___/ _ \/ __/ _ \/ ___/
 / __/ / ____/| |/ |/ / / / /  __/ /_/ / / / / / / / /  /  __/ /_/  __/ /    
/_/   /_/     |__/|__/_/ /_/\___/\__,_/ /_/ /_/ /_/_/   \___/\__/\___/_/     
    """ + f"\n{Fore.WHITE}   >> Kali Intelligence Tool | Multi-API Edition | Dev by JCO211 <<\n")

def check_internet():
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=3)
        return True
    except OSError: return False

def scan_logic(email):
    # Lista de APIs de respaldo (Fuentes de inteligencia)
    sources = [
        f"https://api.pwned.run/v1/check/{email}",
        f"https://api.proxover.com/v1/pwned?email={email}"
    ]
    
    for url in sources:
        try:
            print(f"{Fore.YELLOW}[*] Consultando fuente: {url.split('/')[2]}...")
            res = requests.get(url, timeout=8, headers={'User-Agent': 'Mozilla/5.0'})
            if res.status_code == 200:
                return res.json()
            elif res.status_code == 404:
                return {"pwned": False}
        except Exception:
            print(f"{Fore.WHITE}[-] Fuente no disponible, saltando...")
            continue
    return None

if __name__ == "__main__":
    print_banner()
    if not check_internet():
        print(f"{Fore.RED}[!] ERROR: Kali no tiene conexión. Revisa /etc/resolv.conf")
        sys.exit()

    email = sys.argv[1] if len(sys.argv) > 1 else input("Introduce el correo: ")
    result = scan_logic(email)

    if result and (result.get("pwned") or result.get("found")):
        print(f"\n{Fore.RED}{Style.BRIGHT}[!!!] FILTRACIÓN ENCONTRADA")
        print(f"{Fore.WHITE}Resultados guardados en reporte_pwned.json")
        with open("reporte_pwned.json", "w") as f: json.dump(result, f, indent=4)
    else:
        print(f"\n{Fore.GREEN}[+] No se detectaron brechas en las fuentes actuales.")
