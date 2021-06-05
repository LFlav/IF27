import time
import sys
import paramiko

def connect_ssh(host, port, username, password):
    ssh = None
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        choise = ""
        exitword = ['exit','logout','exit()','logout()']
        while choise not in exitword:
            stdin, stdout, stderr = ssh.exec_command("pwd")
            while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
                time.sleep(0.1)
            stdoutstring = stdout.readlines()
            choice = input(username+'@'+host+':'+str(stdoutstring[0]).strip('\n')+'$')
            if choice in exitword:
                print("Bye Bye")
                sys.exit()
            stdin, stdout, stderr = ssh.exec_command(choice)
            while not stdout.channel.exit_status_ready() and not stdout.channel.recv_ready():
                time.sleep(0.1)

            stdoutstring = stdout.readlines()
            stderrstring = stderr.readlines()
            for stdoutrow in stdoutstring:
                if len(stdoutrow) != 0 :
                    print(stdoutrow,end="")
            for stderrrow in stderrstring:
                if len(stderrrow) != 0 :
                    print(stderrrow,end="")
    finally:
        if ssh is not None:
            # Close client connection.
            ssh.close()


if __name__ == '__main__':
    print("Le mot de passe de l'utilisateur "+sys.argv[3]+" est "+sys.argv[4])
    (stdoutstring, stderrstring) = connect_ssh(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])