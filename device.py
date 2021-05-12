import sys, os, re
from sys import platform
import argparse

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
                elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                    print(Fore.GREEN +' + Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
                else:
                    print(Fore.GREEN +' + Port : %s\tState : %s' % (str(port), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
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

def device(choosenDevice):
    try:
        response = 1
        import nmap
        portScanner = nmap.PortScanner()
        while response in range(1,4):
            response = input("""\nQuel action voulez vous faire (nmap doit être installé) :
                            1)Scan DNS (linux uniquement)
                            2)Scan machine (os + port les plus utilisé)
                            3)Scan port
                            4)Quitter\n""")
            print("You have selected option: ", response)
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
            elif response == '4':
                print("Au revoir")
                sys.exit()
            else:
                print("Choix non valide")
            response = 1
    except nmap.PortScannerError:
        print("Erreur : nmap n'est pas installé sur cet ordinateur")
        sys.exit()

parser = argparse.ArgumentParser() #parsing des arguments
parser.add_argument("choosenDevice", help="cible des scan (ip)")
args = parser.parse_args()
device(args.choosenDevice)
