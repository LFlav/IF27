import sys, os, re
from sys import platform
from pythonping import ping


#Pretty banner
print("-" * 50)
print("Bienvenu dans l'outil de scanning réseaux IF27")
print("Voici les différents réseaux accèsibles depuis votre machine")
print("-" * 50)

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

#Collect list of network connected to actual computer
network = []
if platform == "linux" or platform == "linux2":
    #Recuperation des informations réseaux pour linux
    os.system('ifconfig | grep "inet " | tr -s "[:blank:]" | cut -d " " -f 3 > temp.txt')
    with open("temp.txt","r") as file:
        for line in file:
            ipaddr = re.search(r'(([0-9]+)((?:\.[0-9]+){3}))',line)
            if ipaddr is not None:
                if(ipaddr.group(0).split('.')[0]) != 127 :
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
                ipaddr = re.search(r'(([0-9]+)((?:\.[0-9]+){3}))',line)
                if ipaddr is not None:
                    network.append(ipaddr.group(0))
    os.system("del temp.txt")

#Display list of network connected to user with format 192.168.1.x
availablechoice = []
i = 1
for ipaddr in network:
    splitaddr = ipaddr.split('.')
    splitaddr[3] = "x"
    print("Réseau "+str(i)+" : "+'.'.join(splitaddr))
    availablechoice.append(i)
    i += 1

#Let user choose a network and ping form x.x.x.1 to x.x.x.253
discovredDevice = []
choice = input("Choissisez un réseau : ")
if int(choice) in availablechoice :
    choosenNetwork = network[int(choice)-1]
    splitNetwork = choosenNetwork.split('.')
    for i in range(1,254):
        splitNetwork[3] = str(i)
        result = str(ping(str('.'.join(splitNetwork)),count=1,size=64,timeout=0.01))
        if "Reply" in result:
            ipaddr = re.search(r'(([0-9]+)((?:\.[0-9]+){3}))',result)
            if ipaddr is not None:
                discovredDevice.append(ipaddr.group(0))
else:
    print("Choix non valide")
    sys.exit()

#Display list of device connected to choosen network
print("-" * 50)
availablechoice = []
i = 1
for ipaddr in discovredDevice:
    print("Appareil "+str(i)+" : "+ipaddr)
    availablechoice.append(i)
    i += 1
choice = 1
while choice in availablechoice:
    print("-" * 50)
    choice = input("Choissisez un appareil : ")
    if int(choice) in availablechoice :
        choosenDevice = discovredDevice[int(choice)-1]
        if platform == "linux" or platform == "linux2":
            os.system("gnome-terminal --tab -- "+pythonenv+" "+sys.exec_prefix+"/../device.py "+choosenDevice+" ")
        elif platform == "win32":
            os.system("start cmd /c \""+activatenv+" && "+pythonenv+" "+sys.exec_prefix+"\\..\\device.py "+choosenDevice+"\"")
        availablechoice.remove(int(choice))
        discovredDevice.remove(choosenDevice)
        if len(availablechoice) == 0 :
            print("-" * 50)
            print("Aucun appareil disponible")
        else:
            print("-" * 50)
            availablechoice = []
            i = 1
            for ipaddr in discovredDevice:
                print("Appareil "+str(i)+" : "+ipaddr)
                availablechoice.append(i)
                i += 1
            choice = availablechoice[0]
    else:
        print("Choix non valide")
        sys.exit()



