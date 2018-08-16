'''Sigma auth
Just import and in theory your will keep acess to your files
->for convinience install getpass
'''

import getpass
import os
import time
import subprocess
import threading

CHECK_RATE = 2  # keeps cheking every N seconds

# get pass
# input subprocess is in bytes
passwd = getpass.unix_getpass("Sigma Password:").encode()


def sigma_auth():
    while(True):
        time.sleep(CHECK_RATE)
        if(not got_permissions()):
            os.system("kinit -R")
            if(not got_permissions()):
                try:
                    p = subprocess.Popen(
                        ['kinit'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
                    stdout, stderr = p.communicate(input=passwd)
                    os.system('aklog')
                    time.sleep(2)  # litle pause
                    if(not got_permissions()):
                        print(
                            "Sigma Auth Error After Kinit -R Error Not getting permissions\n", stdout, '\n', stderr)
                except Exception as e:
                    print("Sigma Auth Kinit Error", e)


def got_permissions():
    return os.access('.', os.R_OK) & os.access('.', os.W_OK) & os.access('.', os.X_OK)


thread = threading.Thread(target=sigma_auth, args=())
thread.daemon = True  # for when main process exits this also exits
thread.start()  # Starts the new process
