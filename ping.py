import time
import os
import argparse

def check_ping(ip):
    response = os.system("ping -c 3 " + ip)
    # and then check the response...
    if response == 0:
        pingstatus = "Network Active"
    else:
        pingstatus = "Network Error"
    
    return pingstatus

def main():
    parser = argparse.ArgumentParser(description = "Check Ping")
    parser.add_argument('-t', '--target', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    
    arg = parser.parse_args()
    ip = arg.target

    print(check_ping(ip))

if __name__ == '__main__':
    main()


