#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys
import time

if __name__=='__main__':
    if len(sys.argv) < 4:
        print('{0} <BindIP><Server IP><Message>'.format(sys.argv[0]))
        # sys.exit()

    bindIP = '127.0.0.1' #sys.argv[1]
    serverIP = '127.0.0.1' #sys.argv[2]

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # SOCK_STREAM은 TCP socket을 뜻함
    sock.bind((bindIP, 0))

    sock.connect((serverIP, 5425)) # 서버에 연결 요청

    while True:
        # 서버로 부터 수신
        rbuff = sock.recv(1024) # 메시지 수신
        received = str(rbuff)
        print('수신:{0}'.format(received))

        center_str = received.split('SM')[1].split('SE')[0]
        print(center_str)

        if  center_str == 'Q':
            break

    sock.close()

    # try:

    #     # 서버로 송신
    #     sbuff = bytes(message)
    #     sock.send(sbuff) # 메시지 송신
    #     print('송신:{0}'.format(message))


    #     # 서버로 부터 수신
    #     rbuff = sock.recv(1024) # 메시지 수신
    #     received = str(rbuff)
    #     print('수신:{0}'.format(received))

    # finally:
    #     sock.close()
