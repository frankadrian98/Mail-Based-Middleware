import socket
import sys
import argparse
from src.core_modules.smtp.custom_smtp import is_valid_port, VALID_PORT_RANGE, SimpleMailServer
from src.core_modules.exeptions.custom_exeptions import CustomConnectionError
from src.core_modules.pop3.custom_pop3 import SimplePop3Server


def Main():
    ''' Main function to interact with user via commandline '''

    parser = argparse.ArgumentParser(description='Command Line Interface to accept port number on which server runs.')
    parser.add_argument('-ip', '--ip_address', help='The ip address to be used by server', type=str, required=True)
    parser.add_argument('-p', '--port', help='The port number to be used by server', type=int, required=True)

    # Extract arguments passed from user, and verify the arguments are as expected
    args = parser.parse_args()

    # if user doesn't enter a valid port number
    if not is_valid_port(args.port):
        print(f'\tThe port number is not valid.\n\tExpecting a valid port number in range: {str(VALID_PORT_RANGE)}.\n\tPlease try again.')
        sys.exit(1)

    pop3_server = SimplePop3Server(args.ip_address,args.port)
    pop3_server.connect()
    pop3_server.accept()



if __name__ == '__main__':
    Main()
