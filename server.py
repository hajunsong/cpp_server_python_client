import SocketServer
import sys

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        print('Connected client : {0}'.format(self.client_address[0]))
        sock = self.request

        rbuff = sock.recv(1024)
        received = str(rbuff)
        print('Receive : {0}'.format(received))

        sock.send(rbuff)
        print('Transmit : {0}'.format(received))
        sock.close()


if __name__=='__main__':
    if len(sys.argv) < 2:
        print('{0}<Bind IP>'.format(sys.argv[0]))
        sys.exit()

    bindIP = sys.argv[1]
    bindPort = 5425

    server = SocketServer.TCPServer((bindIP, bindPort), MyTCPHandler)

    print('Start server..')

    server.serve_forever()