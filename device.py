import sys, os, re
from sys import platform
import argparse

global pythonenv
global activatenv
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

def displayPortScanning(result,ip):
    from colorama import init,Fore,Style
    init()
    print('----------------------------------------------------')
    if len(result['scan'][ip]['hostnames'][0]['name']) != 0 :
        print('Hote : %s (%s)' % (ip, result['scan'][ip]['hostnames'][0]['name']))
    else :
        print('Hote : %s ' % (ip))
    if 'osmatch' in result['scan'][ip].keys() :
        if len(result['scan'][ip]['osmatch']) != 0 :
            print('OS : %s' % result['scan'][ip]['osmatch'][0]['name'])
    print('Etat : %s' % result['scan'][ip]['status']['state'])
    if 'tcp' in result['scan'][ip].keys():
        for port in result['scan'][ip]['tcp'].keys():
            if result['scan'][ip]['tcp'][port]['state'] == 'open' :
                if len(result['scan'][ip]['tcp'][port]['product']) != 0 :
                    print(Fore.GREEN + ' + Port : %s\tType : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['product']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                    for service in flagService:
                        if result['scan'][ip]['tcp'][port]['product'] == service[1] or int(port) == service[0]:
                            service[2] = True
                            service[0] = port
                elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                    print(Fore.GREEN +' + Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                    for service in flagService:
                        if result['scan'][ip]['tcp'][port]['name'] == service[1] or int(port) == service[0]:
                            service[2] = True
                            service[0] = port
                else:
                    print(Fore.GREEN +' + Port : %s\tState : %s' % (str(port), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                    for service in flagService:
                        if port == service[0]:
                            service[2] = True
            elif result['scan'][ip]['tcp'][port]['state'] == 'closed' :
                if len(result['scan'][ip]['tcp'][port]['product']) != 0 :
                    print(Fore.RED + ' - Port : %s\tType : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['product']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                    print(Fore.RED +' - Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                else :
                    print(Fore.RED +' - Port : %s\tState : %s' % (str(port), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
            else :
                if len(result['scan'][ip]['tcp'][port]['product']) != 0 :
                    print(Fore.YELLOW + ' ~ Port : %s\tType : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['product']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                    print(Fore.YELLOW + ' ~ Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                else:
                    print(Fore.YELLOW + ' ~ Port : %s\tState : %s' % (str(port), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
    else:
        for port in result['scan'][ip]['portused']:
            if port['state'] == 'open' :
                print(Fore.GREEN + ' + Port : %s\tProtocole : %s\tState : %s' % (str(port['portid']),str(port['proto']), str(port['state'])) + Style.RESET_ALL)
            elif port['state'] == 'closed' :
                print(Fore.RED +' - Port : %s\tProtocole : %s\tState : %s' % (str(port['portid']),str(port['proto']), str(port['state'])) + Style.RESET_ALL)
            else :
                print(Fore.YELLOW + ' ~ Port : %s\tProtocole : %s\tState : %s' % (str(port['portid']),str(port['proto']), str(port['state'])) + Style.RESET_ALL)

def launchbruteforce(choosenDevice,filename):
    user = input("Nom de l'utilisateur attaqué (laisser vide pour root) :")
    if(len(user) == 0):
        user = "root"
    if platform == "linux" or platform == "linux2":
        os.system("gnome-terminal --tab -- "+pythonenv+" "+sys.exec_prefix+"/../bruteforce.py "+choosenDevice+" "+user+" "+filename)
    elif platform == "win32":
        #ouvre un nouveau terminal qui se coupe une fois le programme fini
        os.system("start cmd /c \""+activatenv+" && "+pythonenv+" "+sys.exec_prefix+"\\..\\bruteforce.py "+choosenDevice+" "+user+" "+filename+"\"")
        #ouvre un nouveau terminal et le laisse ouvert (mode debug)
        #os.system("start cmd /k \""+activatenv+" && "+pythonenv+" "+sys.exec_prefix+"\\..\\bruteforce.py "+choosenDevice+" "+user+" "+filename+"\"")

def exploitssh(choosenDevice):
    availableResponseSSH = ['1','2','3','4','q']
    response = '1'
    while response in availableResponseSSH:
        response = input("""\nLe service ssh est ouvert, 3 type d'attaque sont possible :
                            1)Exploit CVE-2018-10993
                            2)Dictionnaire 2000 mdp
                            3)Dictionnaire 20000 mdp
                            4)Dictionnaire personnalisé
                            q)Revenir au scan\n""")
        print("Vous avez choisi l'option: ", response)
        if response == '1' :
            command = input("Commande a executé (cette expploit ne peux éxecuter qu'une seul commande)\n pour des argument utiliser les symbole \" \" :")
            if platform == "linux" or platform == "linux2":
                os.system("gnome-terminal --tab -- "+pythonenv+" "+sys.exec_prefix+"/../exploit.py "+choosenDevice+" "+str(flagService[0][0])+" "+command)
            elif platform == "win32":
                #ouvre un nouveau terminal qui se coupe une fois le programme fini
                os.system("start cmd /k \""+activatenv+" && "+pythonenv+" "+sys.exec_prefix+"\\..\\exploit.py "+choosenDevice+" "+str(flagService[0][0])+" "+command+"\"")
        elif response == '2':
            launchbruteforce(choosenDevice,"passlist.txt")
        elif response == '3':
            launchbruteforce(choosenDevice,"passlist2.txt")
        elif response == '4' :
            filename = input("Indiquer le nom du fichier qui contient le dictionnaire :")
            launchbruteforce(choosenDevice,filename)
        elif response == 'q':
            return "Retour au menu principal"
        else:
            return "Choix non valide"

def exploitftp(choosenDevice):
    return "non implémenté"

def exploit(choosenDevice):
    serviceFunction = {}
    availableService = []
    print("-" * 50)
    print("Liste des services exploitable découvert :")
    for service in flagService:
        if service[2] :
            availableService.append(service[1])
            serviceFunction[service[1]] = eval(str('exploit'+service[1]))
            print("\t - "+service[1])
    resp = input("Veuillez choisir un service :")
    if resp in availableService:
        return serviceFunction[resp](choosenDevice)
    else:
        return "Service non disponible"
    
        

def device(choosenDevice):
    try:
        availableResponse = ['1','2','3','q']
        response = '1'
        import nmap
        portScanner = nmap.PortScanner()
        while response in availableResponse:
            flag = False
            for service in flagService:
                flag = (flag or service[2])
            if flag:
                availableResponse.append('4')
                response = input("""\nQuel action voulez vous faire (nmap doit être installé) :
                                1)Scan DNS (linux uniquement)
                                2)Scan machine (os + port les plus utilisé)
                                3)Scan port
                                4)Exploit kit
                                q)Quitter\n""")
                print("Vous avez choisi l'option: ", response)
            else:
                response = input("""\nQuel action voulez vous faire (nmap doit être installé) :
                                1)Scan DNS (linux uniquement)
                                2)Scan machine (os + port les plus utilisé)
                                3)Scan port
                                q)Quitter\n""")
                print("Vous avez choisi l'option: ", response)
            if response == '1':
                if platform == "linux" or platform == "linux2":
                    print(os.system('dig -x '+choosenDevice+' | grep -v ";"'))
                else:
                    print("Votre système d'exploitaiton n'est pas compatible")
            elif response == '2':
                displayPortScanning(portScanner.scan(choosenDevice,arguments='-O'),choosenDevice)
            elif response == '3':
                choise = input("Choissisez un port à vérifier : ")
                displayPortScanning(portScanner.scan(choosenDevice,choise),choosenDevice)
            elif (response == '4' and flag) :
                print(exploit(choosenDevice))
            elif response == 'q':
                print("Au revoir")
                sys.exit()
            else:
                print("Choix non valide")
            response = '1'
    except nmap.PortScannerError:
        print("Erreur : nmap n'est pas installé sur cet ordinateur")
        sys.exit()

global flagService
flagService = [[22,"ssh",False],[21,"ftp",False]]
parser = argparse.ArgumentParser() #parsing des arguments
parser.add_argument("choosenDevice", help="cible des scan (ip)")
args = parser.parse_args()
device(args.choosenDevice)
