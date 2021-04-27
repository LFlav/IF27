import sys, os, re
from sys import platform
from pythonping import ping

def displayPortScanning(result,ip):
    from colorama import Fore,Style
    print('----------------------------------------------------')
    if len(result['scan'][ip]['hostnames'][0]['name']) != 0 :
        print('Hote : %s (%s)' % (ip, result['scan'][ip]['hostnames'][0]['name']))
    else :
        print('Hote : %s ' % (ip))
    print('Etat : %s' % result['scan'][ip]['status']['state'])
    for port in result['scan'][ip]['tcp'].keys():
        if result['scan'][ip]['tcp'][port]['state'] == 'open' :
            if len(result['scan'][ip]['tcp'][port]['product']) != 0 :
                print(Fore.GREEN + ' + Port : %s\tType : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['product']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
            elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                print(Fore.GREEN +' + Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
        elif result['scan'][ip]['tcp'][port]['state'] == 'closed' :
            if len(result['scan'][ip]['tcp'][port]['product']) != 0 :
                print(Fore.RED + ' - Port : %s\tType : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['product']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
            elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                print(Fore.RED +' - Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
        else :
            if len(result['scan'][ip]['tcp'][port]['product']) != 0 :
                print(Fore.YELLOW + ' ~ Port : %s\tType : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['product']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
            elif len(result['scan'][ip]['tcp'][port]['name']) != 0 :
                print(Fore.YELLOW + ' ~ Port : %s\tName : %s\tState : %s' % (str(port),str(result['scan'][ip]['tcp'][port]['name']), str(result['scan'][ip]['tcp'][port]['state'])) + Style.RESET_ALL)
"""
def displayDNSScanning(result):
    if not result:
        print("Aucune information dns n'est disponible")
    else:
        print(result)
"""
#Pretty banner
print("-" * 50)
print("Bienvenu dans l'outil de scanning réseaux IF27")
print("Voici les différents réseaux accèsibles depuis votre machine")
print("-" * 50)

#Collect list of network connected to actual computer
network = []
if platform == "linux" or platform == "linux2":
    #Recuperation des informations réseaux pour linux
    os.system('ifconfig | grep "inet " | tr -s "[:blank:]" | cut -d " " -f 3 > temp.txt')
    with open("temp.txt","r") as file:
        for line in file:
            ipaddr = re.search(r'((?!127)([0-9]{3})((?:\.[0-9]+){3}))',line)
            if ipaddr is not None:
                network.append(ipaddr.group(0))
    os.system("rm temp.txt")
elif platform == "darwin":
    print("Votre système d'exploitation est incompatible")
    sys.exit()
elif platform == "win32":
    #Recuperation des information réseaux pour windows
    output = os.system('ipconfig > temp.txt')
    with open("temp.txt","r") as file:
        for line in file:
            if "IPv4" in line:
                ipaddr = re.search(r'((?!127)([0-9]{3})((?:\.[0-9]+){3}))',line)
                if ipaddr is not None:
                    network.append(ipaddr.group(0))
    os.system("del temp.txt")

#Display list of network connected to user with format 192.168.1.x
availableChoise = []
i = 1
for ipaddr in network:
    splitaddr = ipaddr.split('.')
    splitaddr[3] = "x"
    print("Réseau "+str(i)+" : "+'.'.join(splitaddr))
    availableChoise.append(i)
    i += 1

#Let user choose a network and ping form x.x.x.1 to x.x.x.253
discovredDevice = []
choise = input("Choissisez un réseau : ")
if int(choise) in availableChoise :
    choosenNetwork = network[int(choise)-1]
    splitNetwork = choosenNetwork.split('.')
    for i in range(1,254):
        splitNetwork[3] = str(i)
        result = str(ping(str('.'.join(splitNetwork)),count=1,size=64,timeout=0.01))
        if "Reply" in result:
            ipaddr = re.search(r'((?!127)([0-9]{3})((?:\.[0-9]+){3}))',result)
            if ipaddr is not None:
                discovredDevice.append(ipaddr.group(0))
else:
    print("Choix non valide")
    sys.exit()

#Display list of device connected to choosen network
print("-" * 50)
availableChoise = []
i = 1
for ipaddr in discovredDevice:
    print("Appareil "+str(i)+" : "+ipaddr)
    availableChoise.append(i)
    i += 1
print("-" * 50)
choise = input("Choissisez un appareil : ")
if int(choise) in availableChoise :
    choosenDevice = discovredDevice[int(choise)-1]
else:
    print("Choix non valide")
    sys.exit()

try:
    response = 1
    import nmap
    portScanner = nmap.PortScanner()
    while response in range(1,4):
        response = input("""\nQuel action voulez vous faire
                        1)Scan DNS
                        2)Scan machine
                        3)Scan port (22-443)
                        4)Scan port
                        5)Quitter\n""")
        print("You have selected option: ", response)
        if response == '1':
            pass
        elif response == '2':
            pass
        elif response == '3':
            displayPortScanning(portScanner.scan(choosenDevice, '22-443'),choosenDevice)
        elif response == '4':
            choise = input("Choissisez un port à vérifier : ")
            displayPortScanning(portScanner.scan(choosenDevice,choise),choosenDevice)
        elif response == '5':
            print("Au revoir")
            sys.exit()
        else:
            print("Choix non valid")
        response = 1
except nmap.PortScannerError:
    print("Erreur : nmap n'est pas installé sur cet ordinateur")
    sys.exit()




