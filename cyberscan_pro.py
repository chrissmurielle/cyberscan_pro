import subprocess
import platform
import re
import socket
import http.client
import time
import os
import datetime

def get_ttl(ip_address):
    # Détermine la commande selon l'OS de l'utilisateur
    system = platform.system().lower()
    if system == "windows":
        command = ["ping", "-n", "1", ip_address]
    else:  # Linux ou macOS
        command = ["ping", "-c", "1", ip_address]

    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        
        # Recherche de la valeur TTL dans la sortie
        ttl_match = re.search(r"ttl[=|:](\d+)", output, re.IGNORECASE)
        if ttl_match:
            ttl_value = int(ttl_match.group(1))
            return ttl_value
        else:
            print("TTL non trouvé dans la réponse.")
            return None
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors du ping : {e}")
        return None

def detect_os(ttl):
    if ttl is None:
        return "Inconnu"
    elif ttl <= 64:
        return "Probablement Linux/Unix"
    elif ttl <= 128:
        return "Probablement Windows"
    elif ttl <= 255:
        return "Probablement un routeur ou un équipement réseau"
    else:
        return "Inconnu"
    
def reverse_dns(ip_address):
    try:
        host, _, _ = socket.gethostbyaddr(ip_address)
        return host
    except socket.herror as e:
        return f"Erreur de résolution : {e}"
    

#verifie si les ports sont ouverts et tente de lire la banniere si le port est ouvert    
ports = [22, 80, 443, 3306]
open_ports = []
timeout = 3  # secondes
def scan_port(ip_address, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((ip_address, port))
            if result == 0:
                print(f"[+] Port {port} est ouvert")
                rapport.append(f"Port {port} ouvert")#
                open_ports.append(port)
                try:
                    # Tenter de lire la bannière
                    s.sendall(b'\r\n')  # pour déclencher parfois une réponse
                    banner = s.recv(1024)
                    if banner:
                        print(f"Bannière : {banner.decode(errors='ignore').strip()}")
                        rapport.append(f"Bannière : {banner}")#
                    else:
                        print("    Aucune bannière reçue.")
                except Exception as e:
                    print(f"    Erreur lors de la lecture de la bannière : {e}")
            else:
                print(f"[-] Port {port} est fermé")
    except Exception as e:
        print(f"Erreur sur le port {port} : {e}")

#simule une requete http get
def requete_http_get(nom_de_domaine):
    
    # Tentative de connexion au port 80 (HTTP)
    try:
        print(f"\n➡️ Connexion à {nom_de_domaine} sur le port 80...\n")
        connexion = http.client.HTTPConnection(nom_de_domaine, 80, timeout=10)
        
        # Envoi d'une requête GET sur la racine
        connexion.request("GET", "/")
        reponse = connexion.getresponse()

        print(f"✅ Statut de la réponse : {reponse.status} {reponse.reason}")
        print("📄 En-têtes de réponse :")
        for header, value in reponse.getheaders():
            print(f"  {header}: {value}")

        print("\n🧾 Début du contenu (premiers 500 caractères) :\n")
        contenu = reponse.read().decode('utf-8', errors='replace')
        print(contenu[:500])
        rapport.append(f"Réponse HTTP (port 80): {contenu [:500]}")#

        connexion.close()

    except Exception as e:
        print(f"❌ Une erreur s'est produite : {e}")

#scan les sous domaines connus
def scan_sous_domaines(nom_de_domaine):
   
    sous_domaines = ['www', 'mail', 'ftp', 'admin', 'test', 'webmail']

    print(f"\n🔍 Scan des sous-domaines de {nom_de_domaine}...\n")

    for sous_domaine in sous_domaines:
        nom_complet = f"{sous_domaine}.{nom_de_domaine}"
        try:
            connexion = http.client.HTTPConnection(nom_complet, 80, timeout=5)
            connexion.request("GET", "/")
            reponse = connexion.getresponse()
            print(f"✅ {nom_complet} répond avec le code HTTP {reponse.status} ({reponse.reason})")
            connexion.close()
            rapport.append(f"{nom_complet} répond avec le code HTTP {reponse.status} ({reponse.reason})")#

        except Exception as e:
            print(f"❌ {nom_complet} ne répond pas ({e.__class__.__name__})")


def save_report(nom_de_domaine, rapport):
    chemin_dossier = r"C:\Users\Manou\cyberscanpro"
    nom_fichier = f"rapport_{nom_de_domaine}.txt"
    chemin_complet = os.path.join(chemin_dossier, nom_fichier)
    with open(chemin_complet, "w", encoding="utf-8") as f:
        f.write(rapport)

def ascii_ports(open_ports):
    print("\nGraphique des ports ouverts :")
    for port in open_ports:
        bar = "#" * (port // 10)  # Échelle visuelle
        print(f"{port:>5} | {bar}")


def analyser_domaine(nom_de_domaine):
  
    # Choix de la commande selon le système d'exploitation

    param = '-n' if platform.system().lower() == 'windows' else '-c'
    i=0
    reussite = 0

    #ping 3 fois et affiche le taux de reussite
    for i in range(0,3):

        try:
            print(f"ping {i+1} vers {nom_de_domaine}")
            result = subprocess.run(
                ['ping', param, '1',nom_de_domaine ],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
                
            )

            if result.returncode == 0:
                print(f"Ping réussi vers {nom_de_domaine}")
                print(result.stdout)
                reussite +=1
                rapport.append(f"{reussite}/3 Ping réussis")
            else:
                print(f"Échec du ping vers {nom_de_domaine}")
                print(result.stderr)

        except Exception as e:
                print(f"Erreur : {e}")
                break
        taux_reussite = (reussite / 3) * 100
        print(f"Taux de réussite : {taux_reussite:.0f}%")
        rapport.append(f"Analyse du domaine : {nom_de_domaine}")#
        rapport.append(f"Date : {now}")#


def main(ip_address):
    #ip = input("Entrez une adresse IP : ")
    ttl = get_ttl(ip_address)
    if ttl is not None:
        print(f"TTL : {ttl}")
        os_guess = detect_os(ttl)
        print(f"Système d'exploitation estimé : {os_guess}")
        rapport.append(f"TTL détecté : {ttl}, Système probable : {os_guess}")#
    else:
        print("Impossible d'obtenir le TTL.")


rapport =[]##  
def save_historique(entry):
    chemin_dossier = r"C:\Users\Manou\cyberscanpro"
    nom_fichier = f"historique.txt"
    chemin_complet = os.path.join(chemin_dossier, nom_fichier)
    with open(chemin_complet, "a", encoding="utf-8") as f:
        f.write(entry + "\n")

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") ##
invalid_count=0
MAX_INVALID =3

#resouds un nom de domaie en adresse ip 
while True:

    nom_de_domaine = input("Entrez votre nom de domaine ou exit pour quitter:")
    if nom_de_domaine.lower() == "exit":
            print("Au revoir !")
            break

    try:
            ip_address = socket.gethostbyname(nom_de_domaine)
            print(f"L'adresse IP de {nom_de_domaine} est {ip_address}")
            rapport.append(f"IP résolue : {ip_address}")
            
    except socket.gaierror:
            print(f"Erreur lors de la résolution DNS")
            print("domaine invalide")
            invalid_count+=1
            if invalid_count >= MAX_INVALID:
                print("trop de domaines invalide. Programme bloqué")
                break
            continue
    else:
        invalid_count=0

    rapport.clear()
    open_ports.clear()

    analyser_domaine(nom_de_domaine)
    main(ip_address)


    #analyse=analyser_domaine(nom_de_domaine)

    ttl_os = main(ip_address)

    reverse = reverse_dns(ip_address)
    print(f"Nom d'hôte pour {ip_address} : {reverse}")
    rapport.append(f"Résolution inverse : {reverse}")

    print(f"Scan de {ip_address}\n")

    for port in ports:
        scan=scan_port(ip_address, port)
    

    http = requete_http_get(nom_de_domaine)
    subdomains = scan_sous_domaines(nom_de_domaine)
    rapport_txt = "\n".join(rapport)

    save_report(nom_de_domaine, rapport_txt)
    save_historique(f"[{now}] Analyse de {nom_de_domaine} terminée.")

    print(f"Ports ouverts: {open_ports}")

    ascii_ports(open_ports)

